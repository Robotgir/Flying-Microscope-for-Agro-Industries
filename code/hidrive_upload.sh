#!/bin/sh
zip -r trailcam.zip trailcam
url="https://webdav.hidrive.ionos.com/users/dev-isis-ic/spectors/" 
filename="trailcam.zip"
# upload file
timestamp=$(date +"%Y-%m-%d_%H-%M-%S") echo $timestamp "Start upload..." 
url=$url$filename 
sudo curl -T $filename $url --basic --user dev-isis-ic:1S1SpwD3Vme1n- 
dev-isis-ic:1S1SpwD3Vme1n- timestamp=$(date +"%Y-%m-%d_%H-%M-%S") echo 
$timestamp "Upload ended"
exit
