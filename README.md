<!-- LOGO -->
<br />
<p align="center">
  <a href="https://assistini.com/" target="_blank">
    <img src="https://assistini.com/static/logo_transparent.png" alt="ASSISTINI" width="80" height="80">
  </a>

  <h3 align="center">Support Assistini™</h3>

  <p align="center">
    An API client to automate the support log bundle upload to assistini.com.
    <br />
    <a href="https://assistini.com/#videos" target="_blank"><strong>Explore the videos »</strong></a>
    <br />
    <br />
  </p>
</p>


<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#result">Result</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>
<br />

<!-- ABOUT THE PROJECT -->
## About The Project

<p align="center">
  <a href="https://assistini.com/" target="_blank">
    <img src="https://assistini.com/static/steps.png" alt="4STEPS" width="800" height="391">
  </a>
</p>
<br />

The Support Assistini™ is a FREE web service to process or analyze VMware vSphere® ESXi™ support log bundle.
Assistini is not related to any 3rd party company of whose support log bundle it processes.
* A typical bundle contains thousands of files and is difficult to read or troubleshoot.
* Simply upload a support log bundle, and we generate a settings, configuration and health overview. 

This git project contains only the API client to send us the support log bundle and receive the generated reports and files.
Please visit our main page for all details.
<br />
<br />

<!-- GETTING STARTED -->
## Getting Started

Clone this git repository to your local machine.
  ```ssh
  git clone https://github.com/assistini/api_client.git
  cd api_client
  ```

<!-- INSTALLATION -->
### Installation

We recommend using a virtual environment, but it is not mandatory.
* create a venv
  ```sh
  python3 -m venv venv_assistini
  ```
  
* install requirements
  ```sh
  source venv_assistini/bin/activate
  pip install -r requirements.txt
  deactivate
  ```

* run the tool 
  ```sh
  venv_assistini/bin/python3 assistini.py <vmsupport.tgz file>
  ```
  Hint: On first run, the tool will ask for API credentials. You can create a free account on our website.
<br />

<!-- RESULT -->
## Result
  ```sh
  $ git clone https://github.com/assistini/api_client.git
  Cloning into 'api_client'...
  remote: Enumerating objects: 30, done.
  remote: Counting objects: 100% (30/30), done.
  remote: Compressing objects: 100% (22/22), done.
  remote: Total 30 (delta 6), reused 0 (delta 0), pack-reused 0
  Unpacking objects: 100% (30/30), done.
    
  $ cd api_client
  $ python3 -m venv venv_assistini
  $ source venv_assistini/bin/activate
  (venv_assistini) $ pip install -r requirements.txt
  Collecting certifi (from -r requirements.txt (line 1))
  Collecting chardet (from -r requirements.txt (line 2))
  Collecting idna (from -r requirements.txt (line 3))
  ...
  Successfully installed Pygments-2.7.2 certifi-2020.11.8 chardet-3.0.4 idna-2.10 importlib-metadata-3.1.1 py7zr-0.11.0 ...
  (venv_assistini) $ deactivate
    
  $ venv_assistini/bin/python3 assistini.py
  usage: assistini.py [-h] [--version] filename
  assistini.py: error: the following arguments are required: filename
  2020-12-04T13:47:12.898Z  ERROR, require an existing and readable file!
    
  $ venv_assistini/bin/python3 assistini.py vsan-esx-01.vsphere.local-vm@2020-25-1111-49-38.tgz
  2020-12-04T13:48:49.326Z  Upload "vsan-esx-01.vsphere.local-vm@2020-25-1111-49-38.tgz" now
  2020-12-04T13:48:59.036Z  API response:
  {
      "details": [
          {
              "avg_proc_time": "3 minutes and 28 seconds (208sec)",
              "backlog": 0,
              "credits": 0,
              "txn": "a1b2c3d4e5"
          }
      ],
      "status": "success"
  }
  2020-12-04T14:10:02.221Z
  API response:
  {
      "details": [
          {
              "arc": "ESXi7",
              "finish": "Fri, 04 Dec 2020 22:06:49 GMT",
              "hostname": "vsan-esx-01",
              "progress": "DONE",
              "start": "Fri, 04 Dec 2020 21:49:00 GMT",
              "url": "https://assistini.com/api/v1/file?download=a1b2c3d4e5"
          }
      ],
      "status": "success"
  }
  2020-12-04T14:10:02.226Z  Downloading "a1b2c3d4e5.7z" now
  a1b2c3d4e5.7z: 100%|#########################################| 23.0M/23.0M [00:00<00:00, 36.9MB/s]
  2020-12-04T14:10:08.465Z  DONE, all finished. Files were written into "./a1b2c3d4e5/"
  ```
<br />

<!-- CONTACT -->
## Contact

Contact us at 'support@assistini.com'.

Project Link: [https://github.com/assistini/api_client](https://github.com/assistini/api_client)
