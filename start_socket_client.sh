#!/bin/bash
cd /home/pi/Documents/sporecollector/
while true
do
	python socket_client_flag_reciever.py >> sporecollector.log
	sleep 3
done

