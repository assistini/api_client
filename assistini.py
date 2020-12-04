#!/usr/bin/env python3

"""
Copyright 2020 Assistini - All rights reserved.

An API client for uploading a VMware vSphere® ESXi™ support log bundle to the Support Assistini.
Visit us at https://assistini.com

General workflow:
    * Test for write permissions in the current working directory.
    * Evaluate arguments, a .tgz or .tar.gz file must be provided.
    * On first run:
        * Query for API credentials.
        * Write '.assistini' file with additional options in home directory.
    * If the config file is present, use credentials, else first run.
    * Upload the tgz file to 'assistini.com'.
    * Query the REST API every n seconds for status updates & progress.
    * On success:
        * Download the .7z file, extract into the current working directory.
    * On failure:
        * Print detailed failure reason and exit.

Install the requirements anv venv:
    python3 -m venv venv_3.8.5
    source venv_3.8.5/bin/activate
    pip install -r requirements.txt
"""

import sys
import os
import uuid
import argparse
import configparser
import getpass
import requests
import json
import time
import pytz
import datetime
import py7zr
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter
from termcolor import colored
from tqdm import tqdm

version = '0412.2143'


def cprint(text, color=None, newline=True):
    """
    Print to stdout with a timestamp and in color. Clear the line first.
    Colors are defined at https://pypi.org/project/termcolor
    """

    rows, columns = os.popen('stty size', 'r').read().split()
    timestamp = colored((datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'), 'cyan')
    payload = text if color is None else colored(text, color)
    end = '\n' if newline else '\r'

    print(' ' * int(columns), end='\r')
    print(timestamp + '  ' + payload, end=end)


def cwd_write_perm():
    """
    Test the current working directory for write permissions. This is required to extract the .7z file later.
    :return bool: True or False
    """

    f = str(uuid.uuid4())

    try:
        with open(f, 'w'):
            pass
        os.remove(f)
        return True

    except IOError:
        return False


def get_filename():
    """
    Get the file name from the arguments list (positional parameter) from argparse.
    :return: The filename, or False if none was given.
    """

    try:
        epilog = 'For details, please visit https://assistini.com'
        parser = argparse.ArgumentParser(description='Support Assistini API Client', epilog=epilog)
        parser.add_argument('filename',
                            help=('The path to the ESXi support bundle. Must be a .tgz or .tar.gz file. '
                                  'Only complete and compressed vm-support bundle are accepted.'))
        parser.add_argument('--version', action='version', version=version)
        args = parser.parse_args()

        # ensure the file is readable
        with open(args.filename, 'rb'):
            pass
        return args.filename

    except:
        return False


def get_config():
    """
    The username and password for the 'assistini.com' API are stored in the home directory '.assistini' file.
    On first run, this file does not exist. Ask the user to provide the credentials.
    For every subsequent run, simply read the file. Shall the password ever change, the user needs to edit the file.
    :return dict: The user credentials, e.g.
        {'username': 'user123',
         'password': 'pass123',
         'url_upload': 'https://assistini.com/api/v1/file',
         'url_status': 'https://assistini.com/api/v1/file?progress=',
         'url_download': 'https://assistini.com/api/v1/file?download='}
    """

    config_file = os.path.join(os.getenv('HOME'), '.assistini')
    cfg = configparser.ConfigParser()

    # file exist, read the content, return values
    try:
        cfg.read(config_file)
        val = {'username': cfg.get('credentials', 'username'), 'password': cfg.get('credentials', 'password'),
               'url_upload': cfg.get('options', 'url_upload'), 'url_status': cfg.get('options', 'url_status'),
               'url_download': cfg.get('options', 'url_download')}
        if len(val) >= 1:
            return val
        else:
            raise

    # file does not exist, create it, set permissions to 600, exit
    except:
        cprint('Config file "{}" is missing. Let\'s create one.'.format(config_file), color='yellow')
        username = input('Username: ')
        password = getpass.getpass()
        cfg.add_section('credentials')
        cfg.set('credentials', 'username', username)
        cfg.set('credentials', 'password', password)
        cfg.add_section('options')
        cfg.set('options', 'url_upload', 'https://assistini.com/api/v1/file')
        cfg.set('options', 'url_status', 'https://assistini.com/api/v1/file?progress=')
        cfg.set('options', 'url_download', 'https://assistini.com/api/v1/file?download=')

        try:
            with open(config_file, 'w') as f:
                cfg.write(f)
            os.chmod(config_file, 0o600)
            cprint('Config file was written successfully. Please re-run {} now.'.format(__file__), color='green')
            sys.exit(0)

        except Exception as e:
            cprint('ERROR, unable to write the config "{}", reason = {}'.format(config_file, e), color='red')
            sys.exit(1)


def upload_file(*args):
    """
    Upload the vm-support bundle to 'assistini.com' via POST.
    :param args: The filename, e.g. 'vsan-esx-01.vsphere.local-vm2020-25-1111-49-38.tgz'.
    :return dict: The API response in JSON format, e.g.
        {'details': [{'avg_proc_time': '1 minute and 55 seconds (115sec)',
            'backlog': 0, 'credits': 0, 'txn': 'a1b2c3d4e5'}], 'status': 'success'}
    """

    cprint('Upload "{}" now'.format(filename))
    header = {'accept': 'application/json', 'User-Agent': 'API-client' + '_' + version}
    r = requests.post(config['url_upload'], auth=(config['username'], config['password']),
                      headers=header, timeout=300, files={'file': open(args[0], 'rb')})
    cprint('API response:')
    print(highlight(json.dumps(r.json(), indent=4, sort_keys=True), JsonLexer(), TerminalFormatter()))

    try:
        return r.json()

    except Exception as e:
        cprint('ERROR, unable to upload the file, reason = {}'.format(e), color='red')
        sys.exit(1)


def query_status(*args):
    """
    Query the status of the processing with the txn ID.
    :param args: The txn ID, e.g. 'a1b2c3d4e5'.
    :return dict: The complete details of the transaction, e.g.
        {"details":
          [{"arc": "ESXi70",
            "finish": "Fri, 27 Nov 2020 23:55:00 GMT",
            "hostname": "vsan-esx-01.vsphere.local",
            "progress": "DONE",
            "start": "Fri, 27 Nov 2020 23:50:00 GMT",
            "url": "https://assistini.com/api/v1/file?download=a1b2c3d4e5"}],
         "status": "success"}
    """

    header = {'accept': 'application/json', 'User-Agent': 'API-client' + '_' + version}
    r = requests.get(config['url_status'] + args[0], auth=(config['username'], config['password']),
                     headers=header, timeout=30)

    try:
        return r.json()

    except Exception as e:
        cprint('ERROR, unable to query the status for transaction {}, reason = {}'.format(args[0], e))
        sys.exit(1)


def query_progress(*args):
    """
    Query the upload status and print it to the console. This function is blocking until:
        * The progress is 'DONE'.
        * The bundle was not picked up from the queue within 60 minutes.
        * Processing has failed with an error, e.g. not a tgz file, file corrupt...

    # immediately after upload
    {"details": [{"avg_proc_time": "2 minutes and 24 seconds (144sec)", "backlog": 0, "credits": 0,
                  "txn": "a1b2c3d4e5"}], "status": "success"}

    # query too early
    {"error": "no progress data for a1b2c3d4e5 found", "status": "failed"}

    # bad file ext
    {"status": "failed", "error": "file extension not allowed, accept only .tgz or .tar.gz"}

    # invalid permissions
    {"status": "failed", "error": "not allowed"}

    # during processing, but not 'DONE' yet
    {"status": "success", "details": [{"progress": "START extracting the tgz file"}]}

    # finished processing
    {"details":[{"arc":"ESXi67","finish":"Thu, 01 Dec 2020 23:00:00 GMT","hostname":"esx01.vsphere.local",
                 "progress":"DONE","start":"Thu, 01 Dec 2020 22:55:00 GMT",
                 "url":"https://assistini.com/api/v1/file?download=a1b2c3d4e5"}],"status":"success"}

    :param args: The txn ID, e.g. 'a1b2c3d4e5'.
    :return: The download URL, e.g. 'https://assistini.com/api/v1/file?download=a1b2c3d4e5'. Exit on failure.
    """

    # to avoid an instant 'no progress data for a1b2c3d4e5 found', we wait 10 sec, no performance impact
    time.sleep(10)
    loop_counter = 1

    while True:
        progress = query_status(args[0])

        # API response 'failed'
        if progress['status'] == 'failed':

            # waiting for the bundle to be picked from the queue
            if 'no progress data for' in progress['error']:

                if loop_counter < 60:
                    cprint('[{}/60] The bundle is still in the queue, please wait...'.format(loop_counter))
                    time.sleep(10)
                    loop_counter = loop_counter + 1
                    continue

                else:
                    cprint('[{}/60] Final timeout.'.format(loop_counter), color='red')
                    sys.exit(1)

            else:
                cprint('ERROR, the API responded with:', color='red')
                print(highlight(json.dumps(progress, indent=4, sort_keys=True), JsonLexer(), TerminalFormatter()))
                sys.exit(1)

        # API response 'success'
        if progress['details'][0]['progress'] == 'DONE':
            cprint('\nAPI response:')
            print(highlight(json.dumps(progress, indent=4, sort_keys=True), JsonLexer(), TerminalFormatter()))
            # return the download URL to indicate success
            return progress['details'][0]['url']

        else:
            if 'No vsish for vmkernel' in progress['details'][0]['progress']:
                cprint('ERROR, the API responded with:', color='red')
                print(highlight(json.dumps(progress, indent=4, sort_keys=True), JsonLexer(), TerminalFormatter()))
                sys.exit(1)

            cprint('Status: {}'.format(progress['details'][0]['progress']), color='white', newline=False)
            time.sleep(5)
            continue


def download_file(*args):
    """
    Download the .7z file. The txn ID is also being used as the local file name.
    :param args: The download URL, e.g. 'https://assistini.com/api/v1/file?download=a1b2c3d4e5'.
    :return: On success, the file name, e.g. 'a1b2c3d4e5.7z'. On failure, exit.
    """

    fn = args[0].split('=')[-1] + '.7z'
    cprint('Downloading "{}" now'.format(fn))
    header = {'accept': 'application/json', 'User-Agent': 'API-client' + '_' + version}

    try:
        r = requests.get(args[0], stream=True, auth=(config['username'], config['password']),
                         allow_redirects=True, headers=header)
        total_size = int(r.headers.get('content-length'))
        initial_pos = 0

        with open(fn, 'wb') as f:
            with tqdm(total=total_size, unit='B', unit_scale=True, desc=fn, initial=initial_pos, ascii=True) as pbar:
                for ch in r.iter_content(chunk_size=1024):
                    if ch:
                        f.write(ch)
                        pbar.update(len(ch))

        return fn

    except Exception as e:
        cprint('ERROR, downloading "{}" to "{}" has failed, reason = {}'.format(args[0], fn, e))
        sys.exit(1)


def extract_7z(*args):
    """
    Extract the 7-zip file into the current working directory.
    :param args: The file name, e.g. 'a1b2c3d4e5.7z'.
    :return: On success True, on failure exit.
    """

    try:
        with py7zr.SevenZipFile(args[0], mode='r') as z:
            z.extractall()
        return True

    except Exception as e:
        cprint('ERROR, extraction failed, reason = {}'.format(e), color='red')
        sys.exit(1)


if __name__ == '__main__':

    # test for write permissions
    if not cwd_write_perm():
        cprint('ERROR, we have no write permissions here!', color='red')
        sys.exit(1)

    # evaluate options/filename
    filename = get_filename()
    if not filename:
        cprint('ERROR, require an existing and readable file!', color='red')
        sys.exit(1)

    # read credentials
    config = get_config()
    if not config:
        cprint('ERROR, reading or writing the config file', color='red')
        sys.exit(1)

    # upload the file
    uf = upload_file(filename)
    if uf['status'] != 'success':
        cprint('ERROR, the upload failed, because:')
        print(highlight(json.dumps(uf, indent=4, sort_keys=True), JsonLexer(), TerminalFormatter()))
        sys.exit(1)
    txn = uf['details'][0]['txn']

    # blocking status query, every 5 seconds, expect the download url as final return value
    url = query_progress(txn)

    # download .7z file, expect local file name as return value
    lfn = download_file(url)

    # extract .7z file
    if extract_7z(lfn):
        cprint('DONE, all finished. Files were written into "./{}/"'.format(lfn.split('.')[0]))
