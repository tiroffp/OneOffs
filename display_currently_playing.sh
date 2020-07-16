#! /bin/bash

while [ "true" ]
do
    currently_playing=`/usr/bin/python3 ~/workspace/oneoffs/currently_playing.py`
    echo -ne "\r\033[K${currently_playing}" >> ~/.currently_playing
done
