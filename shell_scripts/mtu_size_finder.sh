#!/bin/bash
# Script to find optimal mtu size
echo "Finding MTU Size starting from 1500 and lowering by 2 until a successful ping transfer or a key is pressed"

mtusize=1500
rv=1

while [ -z "$key" ]; do
  echo "MTU Size: ${mtusize}"
  ping -D -s ${mtusize} -c 1 www.dslreports.com
  rv=$?
  if [ "$rv" -eq "0" ]; then
    break
  else
    ((mtusize -= 2))
  fi

  sleep 1
  read -t 1 -n 1 key
done
