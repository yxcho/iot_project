iot_project
===========


Table of Contents
------------

| S/NO | Section |
| --- | --- |
| 1. | [About this Project](#1) | 
| 2. | [Setup Environment](#2) | 
| 3. | [Running the Program](#3) | 

About this Project <a name="1"></a>
------------
This project contains the code used for IS614 Internet of Things group project. The details of the project can be found on https://medium.com/@iotteamhexagon/project-trainspot-find-your-spot-on-the-train-99f06f9e93b.  


Setup Environment <a name="4"></a>
------------
Prerequisites: Git, Postgresql, Python 3.8 and above, Dbeaver, WSL1 (for Windows users).  
Keep the micro:bit dongle plugged in to your machine when this program is running.  
Create .env.  

Running the Program <a name="3"></a>
------------
For Windows users, open the program in WSL1.  
To create database tables, run `cd src/data` followed by `python create_table.py`.  

To start the program and keep the gateway running, run `python main.py` for macOS or `python main.py /dev/ttyS5` for Windows.  