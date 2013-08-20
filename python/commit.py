#! /usr/bin/env python
import os
import datetime
import argparse


#Parse Command Line Arguments
parser = argparse.ArgumentParser('Automated Git Commit')
parser.add_argument('-d', required=True, dest='dir', help="Root Git Directory")
parser.add_argument('-m', required=False, dest='msg', help='Optional message to append to date')

args = parser.parse_args()

# Get today!
now = datetime.datetime.now();
ymd = str(now.year) + '-' + str( now.month ) + '-' + str( now.day )

if( args.msg ):
	msg = 'Commit for '+ymd+' '+args.msg
else:
	msg = 'Commit for '+ymd

os.system('cd '+args.dir+'; git add -A')
os.system('cd '+args.dir+'; git commit -m "'+msg+'"')
