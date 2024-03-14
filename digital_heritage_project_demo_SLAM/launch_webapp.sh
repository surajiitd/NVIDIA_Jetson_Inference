#!/bin/bash

# ipAddr=10.194.15.48
ipAddr=127.0.0.1
portNum=8080

hostIp=$ipAddr:$portNum

url="http://$hostIp/"

# xdg-open "$url"

echo "dheritage_app" | figlet
echo "launch dheritage webapp"
cd Digital\ Heritage\ app/new_app/dheritage

python manage.py runserver $hostIp