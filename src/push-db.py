#! /usr/bin/env python

from scp import SCPClient
import paramiko
import argparse
import os

# Parse Command Line Arguments
description = '''
Pushes a local copy of a database to a remote host.
'''
parser = argparse.ArgumentParser(description)
parser.add_argument('-o', required=True, dest='host', help="Remote host to push DB.")
parser.add_argument('-u', required=True, dest='user', help="Remote MySQL Client User.")
parser.add_argument('-p', required=False, dest='passwd', help="RemoteMySQL Password.")
parser.add_argument('-lu', required=False, dest='luser', help="Local MySQL Client User.")
parser.add_argument('-lp', required=False, dest='lpasswd', help="Local MySQL Passwd")
parser.add_argument('-P', required=False, dest='port', type=int, default=22, help="Remote host port")
parser.add_argument('-d', required=True, dest='db', help="Database to push.")

args = parser.parse_args()

# Open SSH Client
print 'Opening SSH Connection'
ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.connect( args.host, args.port )

if not args.luser:
    args.luser = args.user
    
if not args.lpasswd:
    args.lpasswd = args.passwd
    
# Dump local copy.
print 'Dumping Local Copy of DB'
os.system('mysqldump -u ' + args.luser + ' -p' + args.lpasswd + ' --add-drop-table ' + args.db + ' > ' + args.db + '.sql' )

# Copying to Remote
print 'Copying Dump to Remote'
scp = SCPClient( ssh.get_transport() )
scp.put( args.db + '.sql' )

# Running Dump File
print 'Installing DB on Remote'
ssh.exec_command('mysql -u ' + args.user + ' -p' + args.passwd + ' --database=' + args.db + ' < ' + args.db + '.sql' )

# Removing Local Copy
os.unlink('./' + args.db + '.sql' )

# Removing Remote Copy
ssh.exec_command('rm ' + args.db + '.sql')