#! /usr/bin/env python

from scp import SCPClient
import datetime
import paramiko
import argparse
import tarfile
import os

# Parse Command Line Arguments
description = '''
This script creates a tarball of a specified destination and copies it to a remote destination
using ssh on the destination. Requires configured ssh keys on remote host to work. Include
trailing '/' on directory paths!
'''
parser = argparse.ArgumentParser(description)
parser.add_argument('-s', required=True, dest='src', help="Path to directory to backup.")
parser.add_argument('-d', required=True, dest='dest', help="Path to directory to put backup. (Note previous backups in this destination will be deleted!)")
parser.add_argument('-r', required=True, dest='host', help="Remote host to put backup on." )
parser.add_argument('-u', required=True, dest='user', help="Remote host user name")
parser.add_argument('-p', required=False, dest='port', type=int, default=22, help="Remote host port")
parser.add_argument('-f', required=False, dest='file', help="Alternative prefix for resulting tar file.")
parser.add_argument('--remove', required=False, dest='rm', help="Attempt to unlink any existing backup files in destination.")

args = parser.parse_args()

# Get ymd
now = datetime.datetime.now();
ymd = str(now.year) + '-' + str( now.month) + '-' + str(now.day)

# Generate file name parts
pre = 'backup-'
ext = '.tgz'

if args.file:
    pre = args.file

# Local tarball filename
tgz = '/tmp/'+pre+'-'+ymd+ext

# Create Archive
print 'Creating archive for ' + tgz

with tarfile.open( tgz, mode='w:gz') as tarball:
    tarball.add( args.src, arcname=os.path.basename( args.src ) )

# Open SSH Client
print 'Opening SSH Connection'
ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.connect( args.host, args.port, args.user )

# If RM remove pre-existing backup files
if args.rm:
    print 'Removing files with pattern ' + args.dest + pre + '*' + ext
    ssh.exec_command('rm ' + args.dest + pre + '*' + ext )    

# SCP tarfile to Remote
print 'Copying tarball to remote destination'
scp = SCPClient( ssh.get_transport() )
scp.put( tgz, args.dest )

# Remove the local tarball
print 'Removing local copy of tarball'
os.unlink( tgz )
