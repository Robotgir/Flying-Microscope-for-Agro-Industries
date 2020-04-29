from time import sleep
from picamera import PiCamera

camera = PiCamera()
camera.start_preview()
sleep(2)
for pictures in camera.capture_continuous('img{counter:03d}.jpg'):
    print('Captured %s' % pictures)
    sleep(10) # wait 10 secs
