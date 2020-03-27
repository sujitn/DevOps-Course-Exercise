#!/bin/sh

# Enable the Extra Packages for Enterprise Linux (EPEL) repository
sudo yum-config-manager --enable epel --quiet

# Ensure package managers and installed packages are up to date
sudo yum update --assumeyes --quiet

# Unpack the app files and install dependencies
cd /home/ec2-user
unzip app-files.zip
pip install -r requirements.txt

# Install, configure and start Supervisor
pip install supervisor
sudo mv supervisord.conf /etc/supervisord.conf
sudo /usr/local/bin/supervisord --configuration=/etc/supervisord.conf
