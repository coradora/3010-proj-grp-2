#!/bin/sh

CONTAINER_ALREADY_STARTED="CONTAINER_ALREADY_STARTED_PLACEHOLDER"

if [ ! -e $CONTAINER_ALREADY_STARTED ]; then
	# Non-interactive mode necessary to handle postgresql prompts during install.
	export DEBIAN_FRONTEND=noninteractive
	apt-get -y install wget
	touch $CONTAINER_ALREADY_STARTED
    # PostgreSQL install
    sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
    apt-get -y update
    apt-get -y install postgresql

    service postgresql start
    # Create databases, import data.
    # pagila database needs to be included until pg backup is cleaned.
    su postgres -c "psql -c 'CREATE DATABASE pagila;'" 
    su postgres -c "psql -c 'CREATE DATABASE student;'"
    su postgres -c "psql -c 'CREATE USER webuser1 WITH PASSWORD '\''ECUpirate1'\'';'"
    su postgres -c "psql -c 'GRANT ALL PRIVILEGES ON DATABASE student TO webuser1;'"
    su postgres -c "psql -d student -f ./db.sql"

    # PostgreSQL config changes required to allow remote connections to access the database.
    echo "host all all    0.0.0.0/0    md5" >> /etc/postgresql/14/main/pg_hba.conf 
    echo "listen_addresses = '*'" >> /etc/postgresql/14/main/postgresql.conf
    echo "First run setup"
    # Finally, restart the postgresql service.
    service postgresql restart
    # Keep docker container alive.
    while true; do sleep 1; done
else
	echo "Loaded Database"
    # Finally, restart the postgresql service.
    service postgresql restart

    # Keep docker container alive.
    while true; do sleep 1; done
fi
