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
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
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
This project is not related to any 3rd party company of whose support log bundle it processes.
* A typical bundle contains thousands of files and is difficult to read or troubleshoot.
* Simply upload a support log bundle, and we generate a settings, configuration and health overview. 

This git project contains only the API client to send us the support log bundle and receive the generated reports and files.
Please visit our main page for all details.
<br /><br />

<!-- GETTING STARTED -->
## Getting Started

Clone this git repository to your local machine.
```ssh
git clone https://github.com/assistini/api_client.git
```

### Installation

We recommend using a virtual environment, but it is not mandatory.
* create a venv
  ```sh
  python3 -m venv venv_3.8.5
  ```
  
* install requirements
  ```sh
  source venv_3.8.5/bin/activate
  pip install -r requirements.txt
  ```

* run the tool 
  ```ssh
  venv_3.8.5/bin/python3 assistini.py <vmsupport.tgz file>
  ```
<br />

<!-- CONTACT -->
## Contact

Contact us at 'support@assistini.com'.

Project Link: [https://github.com/assistini/api_client](https://github.com/assistini/api_client)
