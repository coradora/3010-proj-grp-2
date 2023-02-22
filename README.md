# 3010 Project Group 2

## Database Server Installation Details

Install postgresql with the following command in the terminal
```
sudo apt install postgresql-12
```

Import the database at 'dbsrv/db02132023.sql' with the following commands (or using pgAdmin), as well as the config files. 
```
psql student < .../dbsrv/db02132023.sql
cp /dbsrv/config/hostname /etc/
cp /dbsrv/config/hosts /etc/
```

Restart postgresql by running the following command in the terminal:
```
sudo systemctl restart postgresql
```

## Web Server Installation Details

Install Apache2 (in accordance with https://ubuntu.com/tutorials/install-and-configure-apache#1-overview) by typing the following command in the terminal.
```
sudo apt install apache2
```

Import the web server config files with the following commands
```
cp -r /websrv/config/etc /etc/
cp -r /websrv/html /var/
```

The file structures should look like this:

```
---/etc/apache2/sites-available/csdashboard.conf
---/etc/hosts
---/etc/hostname
---/var/html/csdashboard/*
---/var/html/index.wsgi
```

The web server component of this project utilizes Python. By default, Ubuntu 20.04 has Python3 preinstalled, but can be installed via 
```
sudo apt install python3 &&
sudo apt install python3-pip
```

All required python modules can be found in /websrv/html/csdashboard/requirements.txt. You can install these requirements in terminal using the following command

```
pip install -r requirements.txt
```

Psycopg2 documentation can be found here: https://www.psycopg.org/docs/
Flask documentation can be found here: https://flask.palletsprojects.com/en/2.2.x/

We configured our Apache server (in accordance with https://plainenglish.io/blog/how-to-securely-deploy-flask-with-apache-in-a-linux-server-environment) with the following commands:

```
sudo a2ensite csdashboard.conf
sudo a2dissite 000-default.conf
```

Restart apache2 with the following command
```
sudo systemctl restart apache2
```

## Usage 
The project is configured to use two hosts -- a dbsrv for the database, and a websrv for the web server.
On the database server, ensure that postgresql is running with the student database and csdashboard table. 
```
sudo systemctl status postgresql
```

On the webserver, ensure apache2 is running with the following command
```
sudo systemctl status apache2
```

If both servers are configured properly, you should be able to access the webserver's front end by accessing 127.0.0.1 or localhost via a web browser. You should see a webpage displaying the csdashboard database.

![image](https://user-images.githubusercontent.com/78966342/220711291-ac363cce-d649-434d-bebc-e583dc6a98f3.png)

