# -*- coding: utf-8 -*-
#*/5 * * * * python /sh/checkPort.py >> /var/checkPort/checkPort_$(date +\%Y\%m\%d).log 2>&1
#定时5分钟一次
import socket
import sys
from optparse import OptionParser
import traceback
import pexpect
import time
from configparser import ConfigParser

cf = ConfigParser()
cf.read('./hostPort.conf')
password = cf.get("hostPort", "passwordss")
dbPort = cf.get("db", "dbPort")
dbUser = cf.get("db", "dbUser")
dbPass = cf.get("db", "dbPass")
dbName = cf.get("db", "dbName")
email = cf.get("base", "email")

print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) )
port = {
    '51234': "ssh -NfL *:51234:192.xxx.xxx.xxx:3306 nxlai@180.xxx.xxx.xxx -p48xxx",
    '3000': "ssh -NfL *:3000:192.xxx.xxx.xxx:3000 nxlai@180.xxx.xxx.xxx -p48xxx",
    '80': "sudo ssh -NfL *:80:192.xxx.xxx.xxx:80 nxlai@180.xxx.xxx.xxx -p48xxx",
    '474': "sudo ssh -NfL *:474:192.xxx.xxx.xxx:474 nxlai@180.xxx.xxx.xxx -p48xxx",
    '55142': "ssh -NfL *:55142:192.xxx.xxx.xxx:55142 nxlai@180.xxx.xxx.xxx -p48xxx",
    '55143': "ssh -NfL *:55143:192.xxx.xxx.xxx:55143 nxlai@180.xxx.xxx.xxx -p48xxx",
    '55212': "ssh -NfL *:55212:192.xxx.xxx.xxx:55212 nxlai@180.xxx.xxx.xxx -p48xxx",
}

#执行重新连接命令
def scpCon(cmd,passord) :
    scp = pexpect.spawn(cmd)
    try:
        i = scp.expect(['nxlai@180.167.105.22\'s password:', pexpect.EOF], timeout=10)
        if i == 0:
            scp.sendline(passord)
            j = scp.expect(['nxlai@180.167.105.22\'s password:', pexpect.EOF], timeout=10)
            if j == 0:
                print("password wrong...")

    except:
        traceback.print_exc()
    scp.close()

def detect_port(ip,port):

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        s.connect((ip,int(port)))
        s.shutdown(2)
        #print('{0} is open'.format(port))
        return True
    except:
        #print('{0} is close'.format(port))
        return False

for key in port :
    result = detect_port('localIp', key)
    if result:
        continue
    else:
        print("Port %s is not open" % key)
        scpCon(port[key], 'password')