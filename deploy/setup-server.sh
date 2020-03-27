#!/bin/sh

# This script accepts the following arguments:
#   1. Public DNS name of the server instance
#   2. SSH key file to authenticate the connection

user=ec2-user
hostname=$1
key_file=$2

if [ -z "$hostname" ]
then
    echo "Host DNS name: \c"
    read hostname
fi

if [ -z "$key_file" ]
then
    echo "SSH key filename: \c"
    read key_file
fi

if [ -z "$hostname" ]
then
    echo "ERROR: A public DNS name must be specified for the remote host"
    exit 1
elif [ -z "$key_file" ]
then
    echo "ERROR: A key file must be specified for public key authentication"
    exit 1
elif [ ! -f "$key_file" ]
then
    echo "ERROR: The specified key file ($key_file) does not exist"
    exit 1
fi

echo "Packaging up code files..."
zip --junk-paths app-files.zip ../*.py

echo "Copying code and configuration files to remote host..."
scp -i $key_file setup.sh $user@$hostname:setup.sh
scp -i $key_file app-files.zip $user@$hostname:app-files.zip
scp -i $key_file supervisord.conf $user@$hostname:supervisord.conf

echo "Running setup script on remote host..."
ssh -i $key_file $user@$hostname chmod +x /home/$user/setup.sh
ssh -i $key_file $user@$hostname sudo /home/$user/setup.sh
