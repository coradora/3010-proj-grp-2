# CSDashboard: Phase 3 - Group 2

![image](https://user-images.githubusercontent.com/78966342/229600175-89ff804f-fcbd-40a9-89a9-eb103eb0bbdf.png)

## Table of Contents

1. [Database Server Installation Instructions](#database-server-installation-instructions)
2. [Web Server Installation Instructions](#web-server-installation-instructions)
3. [Usage](#usage)

## Database Server Installation Instructions

1. Install PostgreSQL by executing the following command in your terminal:
```
sudo apt install postgresql-12
```

2. Import the database at **'dbsrv/db04032023.sql'** with the following commands (or using pgAdmin), as well as the config files. 
```
psql student < .../dbsrv/db04032023.sql
cp /dbsrv/config/hostname /etc/
cp /dbsrv/config/hosts /etc/
```

3. Restart PostgreSQL by running:
```
sudo systemctl restart postgresql
```

## Web Server Installation Instructions

1. Install Apache2 as per the [official Ubuntu tutorial](https://ubuntu.com/tutorials/install-and-configure-apache#1-overview) using the following command:
```
sudo apt install apache2
```

2. Copy the web server configuration files with these commands:
```
cp -r /websrv/config/etc /etc/
cp -r /websrv/html /var/
```

The file structure should resemble:

```
---/etc/apache2/sites-available/csdashboard.conf
---/etc/hosts
---/etc/hostname
---/var/html/csdashboard/*
---/var/html/index.wsgi
```

3. The web server component requires Python. Ubuntu 20.04 typically comes with Python3 pre-installed. If necessary, install Python3 and pip using:
```
sudo apt install python3 &&
sudo apt install python3-pip
```

4. Install the necessary Python modules listed in /websrv/html/csdashboard/requirements.txt by executing:

```
pip install -r requirements.txt
```
For more information, consult the [Psycopg2 documentation](https://www.psycopg.org/docs/) and [Flask documentation](https://flask.palletsprojects.com/en/2.2.x/).
https://plainenglish.io/blog/how-to-securely-deploy-flask-with-apache-in-a-linux-server-environment

5. Configure the Apache server as described in [this tutorial](https://plainenglish.io/blog/how-to-securely-deploy-flask-with-apache-in-a-linux-server-environment) with the following commands:

```
sudo a2ensite csdashboard.conf
sudo a2dissite 000-default.conf
```

6. Restart Apache2:
```
sudo systemctl restart apache2
```

## Usage 
This project utilizes two hosts: a database server (dbsrv) and a web server (websrv).
1. On the database server, ensure that PostgreSQL is running with the **student** database and **csdashboard** table:
```
sudo systemctl status postgresql
```

2. On the webserver, confirm that Apache2 is running:
```
sudo systemctl status apache2
```

3. If both servers are correctly configured, access the webserver's frontend by navigating to 127.0.0.1 or localhost in a web browser. The Faculty dashboard should appear, featuring a navigation bar leading to other tables.

During this phase, we introduced a custom query page for executing user-defined SELECT queries. This temporary feature demonstrates input sanitization for forms interacting with Flask and our backend system. The custom query page returns an error for invalid, empty, or potentially harmful queries, such as DROP, UPDATE, INSERT, or DELETE.
