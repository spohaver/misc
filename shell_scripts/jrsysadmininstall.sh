
#!/bin/bash
#
echo "*****************************"
echo "* Basic Intstallation Setup *"
echo "*      By Sean O'Haver      *"
echo "*****************************"
#
echo "Installing dependencies..."
cd ~
sudo apt-get update
sleep 3
sudo apt-get install -y --fix-missing build-essential gcc g++ automake libreadline-dev libxml2-dev libxslt-dev libghc-zlib-dev libssl-dev git python-dev python-pip tree
echo "dependencies completed."
sleep 5
#
echo "Ruby 2.2 Installation starting..."
wget http://ftp.ruby-lang.org/pub/ruby/2.2/ruby-2.2.2.tar.gz
sleep 5
tar -xzvf ruby-2.2.2.tar.gz
cd ruby-2.2.2/
./configure
make
sudo make install
ruby -v
echo "Ruby 2.2 Install Complete."
cd ~
sleep 5
#
echo "Chef 12 Client Installation starting..."
curl -L https://www.opscode.com/chef/install.sh | sudo bash
sleep 5
knife -v
echo "Chef 12 Client complete."
cd ~
sleep 5
#
echo "Mercurial 3.x Installation starting..."
sudo pip install mercurial
hg --version
touch ~/.hgrc
echo "Mercurial 3.x complete."
cd ~
sleep 5
#
# Configure Mercurial:  Mercurial
# Ignore the installation instructions
# Create an .hgrc file
# Follow the Keyring Extension instructions
#
echo "Gems knife-ec2: (I-Ming's version) Starting..."
# We use the knife-ec2 chef plugin to create, show, delete, etc. instances in AWS EC2
git clone https://github.com/Roddd/knife-ec2.git
sleep 5
cd knife-ec2
git checkout enhanced
gem build knife-ec2.gemspec
sudo gem install --local knife-ec2-0.6.2.gem
cd ~
sleep 5
#
echo "knife-openstack plugin installation starting..."
# We use the knife-openstack plugin to create, show, delete, etc. instances in OpenStack
sudo gem install knife-openstack --no-ri --no-rdoc
cd ~
sleep 5
#
echo "spiceweasel: (Nick's version) git clone starting..."
# We use spiceweasel to generate instance create commands for both AWS and Openstack environments
git clone https://github.com/nickryand/spiceweasel.git
cd spiceweasel
git checkout master
gem build spiceweasel.gemspec
sudo gem install --local spiceweasel-1.1.2.gem
cd ~
echo "Gems Installed..."
sleep 5
