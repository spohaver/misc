#!/bin/bash
# This was created when I couldn't run the watch command

# The loop will exit when a key is pressed
while [ -z "$key" ]; do
    clear
    echo -e "This is a check of the $(pwd) directory.\n"
    echo -e "There are $(ls -a | wc -l) lines in the directory.\n"
    echo -e "Running 'df -h'"
    df -h
    echo -e "\nRunning 'du -cksh'"
    du -cksh
    sleep 2

    read -t 1 -n 1 key
done 
