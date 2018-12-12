import os
import subprocess
try:
        subprocess.call('ps aux | grep /u01/app | awk \'{print $2}\' | xargs kill -9',shell=True)
except OSError as e:
        print (e)
        exit(0)
