# CSDashboard: Phase 4 - Group 2

![image](https://user-images.githubusercontent.com/78966342/229600175-89ff804f-fcbd-40a9-89a9-eb103eb0bbdf.png)

## Table of Contents

1. [Database Server Installation Instructions](#database-server-installation-instructions)
2. [Web Server Installation Instructions](#web-server-installation-instructions)
3. [Usage](#usage)

## Database Server Installation Instructions

1. Set up the Docker repository with the following [commands](https://docs.docker.com/engine/install/ubuntu/)
* Update the apt package index and install packages to allow apt to use a repository over HTTPS:
```
sudo apt-get update
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg
```
* Add Docker’s official GPG key:
```
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```
* Use the following command to set up the repository:
```
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

2. Install Docker by executing the following command in your terminal:
```
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

3. Create a docker network by executing the following command in the terminal:
```
sudo docker network create --subnet=192.168.56.0/24 dockernetwork
```

3. Navigate to dbsrv/docker-container in the terminal and build the dockerfile.
```
sudo docker build -t dockerfile:latest .
```

4. Start up the database docker container with the following command:
```
sudo docker run -d --network dockernetwork --ip 192.168.56.20 -p 5432:5432 --restart=always dockerfile:latest
```
* The defined dockernetwork network and static IP address are to allow ease of access to the database with our Flask server below. We expose port 5432 to allow our host to connect to PostgreSQL.

5. After several minutes, setup should be complete and you should be able to communicate with the docker container. The dockerfile is configured such that the setup process will only be required on the first launch, and subsequent launches will load the database immediately. This will allow persistent changes to be made to the database, if necessary.

## Web Server Installation Instructions

1. Install Apache2 as per the [official Ubuntu tutorial](https://ubuntu.com/tutorials/install-and-configure-apache#1-overview) using the following command:
```
sudo apt install apache2
```

2. Copy the web server configuration files with these commands:
```
cp -r /websrv/config/etc/. /etc/
cp -r /websrv/html/. /var/
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

6. A logs folder may be required in the csdashboard folder copied over in step 2. You can create the folder with the following command.
'''
sudo touch /var/www/html/csdashboard/logs
'''

7. Restart Apache2:
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

During this phase, we implemented a Docker container that would allow us to more quickly build, test, and deploy the dashboard application. 
