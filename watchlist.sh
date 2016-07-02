#!/bin/bash

while [ -z "$key" ]; do
    clear
    echo -e "This is a check of the $(pwd) directory.\n"
    echo -e "There are $(ls -a | wc -l) lines.\n"
    df -h
    du -cksh
    sleep 2

    read -t 1 -n 1 key
#    if [[ -z "$key" ]]
#    then
#        break
#    fi 
done 
