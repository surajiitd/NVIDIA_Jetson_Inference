#!/bin/bash

cd ../

# Define the filename
filename="ipAddr.txt"

# Check if the file exists
if [ ! -f "$filename" ]; then
    echo "File $filename not found."
    exit 1
fi

# Read the IP address from the file
ip_address=$(cat "$filename")

# Display the IP address
echo "The IP address read from the file is: $ip_address"

# ipAddr=10.194.15.48
ipAddr=$ip_address
portNum=8080

hostIp=$ipAddr:$portNum

url="http://$hostIp/"

# xdg-open "$url"

echo "dheritage_app" | figlet
echo "launch dheritage webapp"
cd Digital\ Heritage\ app/new_app/dheritage

python manage.py runserver $hostIp