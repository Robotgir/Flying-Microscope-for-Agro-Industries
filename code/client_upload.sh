#!/bin/sh

curl \
  -F "userid=1" \
  -F "filecomment=This is an image file" \
  -F "fileToUpload=@${1}" \
  http://h2790588.stratoserver.net/spectors/upload/upload.php

