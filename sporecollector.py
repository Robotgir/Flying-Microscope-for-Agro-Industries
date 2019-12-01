import time
import picamera
import os
import Adafruit_ADS1x15
import RPi.GPIO as GPIO
import sys
import threading

def ledcam():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11, GPIO.OUT)
    with picamera.PiCamera() as camera:
        os.chdir ("/home/pi/trailcam")
        camera.start_preview()

        try:
            for i, filename in enumerate(camera.capture_continuous('image{counter:03d}.jpg')):
                print(filename)
                GPIO.output(11,False)
                time.sleep(5)
                GPIO.output(11, True)
                if i == 20:
                    break
        finally:
            camera.stop_preview()
            GPIO.cleanup()

def measurmentprocess():
    adc = Adafruit_ADS1x15.ADS1115()
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(12,GPIO.OUT)
    GPIO.output(12,GPIO.HIGH)
    GAIN = 2/3
    print('Reading ADS1x15 values, press Ctrl-C to quit...')
    print('ASLPS = Accumulated standard litres/sec')
    print('SLPS  = Standard litres/sec')
    print(' ASLPS        SLPS        Volts        Time ' )
    print('Total L     [Ltr/s]        [V]         [sec]  ')
    print('-' *45  )
    import os
    z=0
    kha=0
    while True:
        values = [0]*1
        if z<=5:
            for i in range(1):
                total=0
                for j in range(1,301):
                    values[i] = adc.read_adc(i, gain=GAIN, data_rate=860)
               	    y=(values[i]*0.000187505)
                    total+=y
                    if j%300==0:
                        avg=total/300
                        x=(avg-1)*(0.0416666)
                        z+=x
                        kha=kha+1
                        print ('%.5f'%(z) , '    %.5f'%(x),'    %.5f'%(avg)    ,kha)
        else:
                GPIO.output(12,GPIO.LOW)
                GPIO.cleanup()
                sys.exit()

t1 = threading.Thread(target=ledcam)
t1.daemon = True
t1.start()


if __name__== '__main__':
    measurmentprocess()




