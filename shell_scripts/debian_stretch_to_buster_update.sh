#!/bin/bash
#

function check_root() {
  if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root"
    exit 1
  fi
}

function update_upgrade() {
  apt-get update
  apt-get upgrade --yes
}

check_root
update_upgrade
sed -ie 's/stretch/buster/' /etc/apt/sources.list
update_upgrade
apt full-upgrade
