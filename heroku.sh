#!/bin/bash

# Create heroku configuration file
DATABASE=$(echo ${MONGOHQ_URL} | cut -d"/" -f4)
cat >heroku.ini <<EOL
[webserver]
host = 0.0.0.0
port = ${PORT}
debug = false

[storage]
type = mongodb
host = ${MONGOHQ_URL}
database = ${DATABASE}

[session]
type = redis
uri = ${REDISTOGO_URL}

[worker]
broker = ${MONGOHQ_URL}
interval = 20
EOL