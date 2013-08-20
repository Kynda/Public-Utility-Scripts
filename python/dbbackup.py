#! /usr/bin/env python

import MySQLdb
import subprocess
import datetime
import os
import argparse

#Parse Command Line Arguments
parser = argparse.ArgumentParser("Database Backup Automation")
parser.add_argument('-u', required=True, dest='user',   help="MySQL User with SELECT and LOCK TABLE privileges")
parser.add_argument('-p', required=True, dest='passwd', help="MySQL User password")
parser.add_argument('-d', required=True, dest='dumpdir',    help="Directory to store backups. Include trailing /")
args = parser.parse_args()

user = args.user
passwd = args.passwd
dumpdir = args.dumpdir

# Create dumpdir/Y-m-d if not exists
now = datetime.datetime.now();
ymd = str(now.year) + '-' + str( now.month) + '-' + str(now.day)
if not os.path.exists(dumpdir+ymd):
	os.makedirs(dumpdir+ymd)

# Connect to DB and get database list
db = MySQLdb.connect("localhost", user, passwd)
c = db.cursor()
c.execute("show databases")
databases = c.fetchall()

# Loop through DB list, call mysql dump, gzip results and write to dumpdir
for database in databases:
	dumpfile = dumpdir+ymd+'/'+ymd+'_'+database[0]+'.sql.gz'; 
	p1 = subprocess.Popen(["mysqldump", "-u"+user, "-p"+passwd, database[0]], stdout=subprocess.PIPE)
	p2 = subprocess.Popen(["gzip"], stdin=p1.stdout, stdout=subprocess.PIPE)
	p1.stdout.close();
	output = p2.communicate()[0]
	write_file = open(dumpfile, "w")
	write_file.write(output)
	write_file.close()	
	
