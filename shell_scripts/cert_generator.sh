#!/bin/bash
# Desc: Create a self signed cert

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi
old_dir=$(pwd)
initial_dir=/usr/share/certs
hostname=$(hostname -f)

if [ ! -d "$initial_dir" ]; then
  mkdir -p $initial_dir
fi

cd $initial_dir
echo "Running in directory: $(pwd)"

# Generate private key
openssl genrsa -out ${hostname}.key 2048

# Generate CSR
openssl req -new -key ${hostname}.key -out ${hostname}.csr

# Generate Self Signed Key
openssl x509 -req -days 365 -in ${hostname}.csr -signkey ${hostname}.key -out ${hostname}.crt

# Copy the files to the correct locations
cp ${hostname}.crt /etc/pki/tls/certs
cp ${hostname}.key /etc/pki/tls/private/ca.key
cp ${hostname}.csr /etc/pki/tls/private/ca.csr

cd $old_dir
