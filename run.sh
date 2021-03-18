#!/bin/bash
while :
do
    git fetch
    git pull origin main
    python3.8 bot.py
    echo "Press [Ctrl + C] to stop..."
    sleep 2
done