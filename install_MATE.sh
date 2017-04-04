#!/bin/bash
# installs the MATE Desktop for rhel based systems

echo "installing epel-release.."
yum install -y epel-release
echo "group installing X Window System.."
yum groupinstall -y "X Window System"

#Install MATE Desktop
echo "about to install MATE Desktop, outputting information"
yum groupinfo "MATE Desktop"
sleep 5
yum groupinstall -y "MATE Desktop"

#set the GUI on boot
systemctl set-default graphical.target
mv /etc/systemd/system/default.target /tmp/
echo "Moved /etc/systemd/system/default.target to /tmp for backup purposes"
ln -s '/usr/lib/systemd/system/graphical.target' '/etc/systemd/system/default.target'
echo "Set /usr/lib/systemd/system/graphical.target as the default.target for boot up purposes"

echo "starting up MATE Desktop in 5 seconds"
sleep 5
systemctl isolate graphical.target
