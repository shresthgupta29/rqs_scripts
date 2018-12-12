import os
import subprocess
import time
from subprocess import Popen, PIPE
import shutil
import sys
cwd = os.getcwd()  #/current working directory
oracle_base = sys.argv[3]
oracle_home = oracle_base+'/product/12.1.0/dbhome_1'
admin_username="sys"
admin_pass='Manager1' # password for sys/system/admin accounts
cdb = sys.argv[1] #container db name
pgdb = sys.argv[2] #pluggable db name
port="1521" #port for DB
#os.chdir(client_path)
cwd = os.getcwd()
print "At "+cwd
#subprocess.call('su pgbu_apps', shell=True)

user = Popen(['whoami'], stdout=PIPE)
user = user.communicate()[0].split()
user = user[0]
#print(type(user))
if user=='root':
        print('In root user...run as pgbu_aps')
        exit(0)
elif user=='gbuora':
        os.putenv('ORACLE_HOME',oracle_home)
        os.putenv('ORACLE_SID',cdb)
        os.chdir(oracle_home+'/bin')
	
        conn = 'sys/'+admin_pass+'@'+cdb+' as sysdba'
        session = subprocess.Popen([oracle_home+'/bin/sqlplus', '-S', conn], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        session.stdin.write('shutdown immediate;')
        (stdout,stderr)=session.communicate()
        print stdout   
        subprocess.call('./lsnrctl stop',shell=True)    