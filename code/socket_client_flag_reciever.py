import sys
import select
import socket
from socket import error as SocketError
import subprocess
import psutil
import time
from time import sleep

SporecollectorFile = "sporecollector1.py"

lastKeepAliveTime = 0

HOST = 'h2790588.stratoserver.net'
PORT = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.settimeout(2)
readable = [s] # list of readable sockets.  s is readable if a client is waiting


def checkIfMeasurementIsRunning():
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            #print "--- compare ---"
            #print "proccessName.lower(): "+processName.lower()
            #print "proc.cmdline().lower(): "+proc.cmdline().lower()
            cmdline = proc.cmdline()
            if "python" in cmdline and SporecollectorFile in cmdline:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZoambieProcess):
            pass
    return False;

def stopMeasuring():
    for proc in psutil.process_iter():
        #try:
            cmdline = proc.cmdline()
            #print cmdline
            if "python" in cmdline and SporecollectorFile in cmdline:
                print "try to kill process"
                #proc.send_signal(2)
                proc.kill()
                print "Stop signal send to sporecollector process"
        #except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            #pass

def cutConnection(connection, reason):
    print "Connection lost for " + format(connection.getpeername()) +", "+ reason
    readable.remove(connection)
    connection.close()

while 1:
    try:
        s.connect((HOST,PORT))
        print 'Connected to server'

        while 1:

            # [begin] try to read data from socket if available
            r,w,e = select.select(readable,[],[],0)
            # print len(r)
            if len(r) >= 1:
                try:
                    msg = s.recv(1024)
                except socket.timeout, e:
                    cutConnection(s, "recv() timed out")
                    break
                if not msg:
                    cutConnection(s, "server closed connection")
                    break
                else:
                    # got a message do something :)
                    print '[in] '+ msg

                    if msg == 'start':
                        if checkIfMeasurementIsRunning():
                            print "already running"
                        else:
                            print 'starting measurring now'
                            #execfile("sporecollector1.py")
                            subprocess.Popen(["python", SporecollectorFile])
                        print "[out] ok"
                        s.send('ok')
                    if msg == 'stop':
                        print 'stoping measurring now'
                        stopMeasuring()
                        print "[out] ok"
                        s.send('ok')

            # [end] try to read data from socket if available

            # [begin] send a keepalive if necessary
            if time.time() - 4 >= lastKeepAliveTime:
                print "[out] kpa"
                s.send('kpa')
                lastKeepAliveTime = time.time()
            # [end] send keepalive

            #print '---end of loop---'
            sleep( 1 )

    except SocketError, e:
        print "error, retry to establish connection in 3 sec"
        #print "could not connect to server, retry in 3 sec"
        sleep(3)

