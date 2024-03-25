#!/bin/bash

# Ensure connected to IITD_WIFI

# Remote server details
remote_user="data"
remote_host="negroni.cse.iitd.ac.in"
remote_dir="/home/data/submit/WORKING/DatasetsDH/"
# Filename
filename="IITD_campus_edited.mp4"

# Copy the main file

# Check if the filename ends with ".osa"
if [[ $filename == *.osa ]]; then
    scp "$remote_user@$remote_host:$remote_dir/" "../../Datasets"
if [[ $filename == timestamps_\d+\.txt ]]; then
    scp "$remote_user@$remote_host:$remote_dir/" "../Lab_TimeStamps.txt"
fi