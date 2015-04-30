#!/usr/bin/env python
#coding=utf-8

#Auther: zhouyanjiang
#Date: 2015-04-29

import os
import sys
import commands
import MySQLdb
from common import *
import wx

NO_OUT = ">/dev/null 2>&1"
MYSQLPARA = ["192.168.9.193","root","root","sws"]

def myget(cmd):return commands.getoutput()
def mysuccess():wt_print('m', 'Successed!')
def mysys(cmd):os.system('%s %s' % (cmd, NO_OUT))
def connect_db():return MySQLdb.connect(host=MYSQLPARA[0],user=MYSQLPARA[1],passwd=MYSQLPARA[2],db=MYSQLPARA[3]).cursor()
def gen_date():return time.strftime('%Y-%m-%d')
def gen_time():return time.strftime('%H:%M:%S')
def myprint(mode, message):print "===%s %s===%s: %s"%(gen_data(),gen_time(),mode,message)
def file2lines(filename):return open(filename).readlines()
def file2string(filename):return ''.join([i.strip() for i in open(filename).readlines()])
def rmquote(a):return a[1:-1] if a.startswith("'") and a.endswith("'") or a.startswith('"') and a.endswith('"') else a

if __name__ == '__main__':
    try:
        cu = connect_db()
    except Exception:
        myprint("e",u"")
    app = wx.PySimpleApp() 
    ToolFrame().Show()
    app.MainLoop()
    #cu.execute("select passwd from USER where name='zhouyanjiang'")
    #for row in cu.fetchall():  
    #    print row
