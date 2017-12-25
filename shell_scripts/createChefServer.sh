#!/bin/bash
# CHEF SERVER BUILDER SCRIPT - OpenStack -- by Sean OHaver
# USAGE: You can either set this with an IP address afterwards and it will pull
# the argument, ie: . createChefServer.sh 10.148.0.5, or if no IP address is
# given, it will be asked in the beginning
# Things to do:
# the ipAddress variable does not verify that it is a valid IP address.

ipAddress=""

# Asking User to input IP Address - Will be used to add the api_fqdn line in the chef-server.rb file later
if [ -z "$1" ]; then
	echo "What is the IP address for the Chef Server? ";
	read ipAddress
else
	ipAddress="$1"
fi

echo $ipAddress

# Update the /etc/hosts file with the following:
# 127.0.0.1 localhost chef-server-01
# x.x.x.x   chef-server-01                  *(Replace the x's with the IP of the Chef server)
# sed -i 'Ns/.*/replacement-line/' file.txt
sed -i '1s/.*/127.0.0.1 localhost chef-server-01/' /etc/hosts
sed -i "2s/.*/$ipAddress chef-server-01/" /etc/hosts

# Create a swapfile -- this is intended for micro instances where memory is an issue.
sudo dd if=/dev/zero of=/swapfile bs=1M count=1024
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
swapon -s
sleep $[ ( $RANDOM % 8 ) + 3 ]s

# Update and install build-essential
sudo apt-get update
sleep $[ ( $RANDOM % 8 ) + 3 ]s
sudo apt-get install build-essential
sleep $[ ( $RANDOM % 8 ) + 3 ]s

# Install Ruby
# Installing From 3rd Party Repo - Changing /etc/opscode/chef-server.rb
# sudo apt-add-repository ppa:brightbox/ruby-ng
# sudo apt-get update
# sudo apt-get install ruby2.2 ruby2.2-dev
# ruby -v
wget http://ftp.ruby-lang.org/pub/ruby/2.2/ruby-2.2.2.tar.gz
sleep $[ ( $RANDOM % 5 ) + 2 ]s
tar -xzf ruby-2.2.2.tar.gz
sleep $[ ( $RANDOM % 5 ) + 2 ]s
cd ruby-2.2.2/
./configure
make
sudo make install
cd ~

# Download and Install Chef Server
wget https://web-dl.packagecloud.io/chef/stable/packages/ubuntu/trusty/chef-server-core_12.0.5-1_amd64.deb
sleep $[ ( $RANDOM % 5 ) + 2 ]s
sudo dpkg -i chef-server-core_12.0.5-1_amd64.deb

# Appends the line "api_fqdn "ipAddress"" recalled from the IP address asked in the beginning
echo "api_fqdn \"$ipAddress\"" >> /etc/opscode/chef-server.rb
sudo chef-server-ctl reconfigure

# Print out the Ruby version
ruby -v
knife --version

exit 0
