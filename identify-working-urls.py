import psutil
import subprocess

subp = subprocess.Popen('access-url.py', shell=True)
import psutil, time

TIMEOUT = 60 # 1 hour
try:
    p = psutil.Process(subp.pid)
    while 1:
        v =time.time()
        x = p.create_time()
        l= v-x
        if (time.time() - p.create_time()) > TIMEOUT:
            p.kill()
        # the idea here could be to introduce somethign to check if the process was successsful!
        else:
            print('keep going')
except psutil.NoSuchProcess:
    print('No Such Process error')