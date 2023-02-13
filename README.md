# 3010 Project Group 2

## Installation Details

The web server component of this project utilizes Python. By default, Ubuntu 20.04 has Python3 preinstalled, but can be installed via 
```
sudo apt install python3
```

The Python package installer, pip, is required to install packages for python. It can be installed with 
```
sudo apt install python3-pip
```

In order to integrate our postgresql database with python, we installed psycopg2 in accordance with https://www.psycopg.org/docs/
```
sudo apt install python3-psycopg2
```

To interface psycopg2 with our webserver, we installed Flask and utilized Jinja2, which is included with Flask.
Flask documentation can be found here: https://flask.palletsprojects.com/en/2.2.x/
To install flask via the python package installer, type in the following command
```
pip install flask
```

## Usage 
The project is configured to use two hosts -- a dbsrv for the database, and a websrv for the web server.
On the database server, ensure that postgresql is running with the student database and csdashboard table. On the web server, navigate to the websrv directory and run the following command. 
```
python3 websrv.py
```
If both servers are configured properly, you should be able to access the webserver's front end by accessing 127.0.0.1:5000 via a web browser.

![image](https://user-images.githubusercontent.com/78966342/218595023-1d01f122-24ee-40eb-b56c-93482d5dad1a.png)

