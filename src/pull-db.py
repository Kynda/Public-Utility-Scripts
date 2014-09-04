#! /usr/bin/env python

from scp import SCPClient
import paramiko
import argparse
import os

# Parse Command Line Arguments
description = '''
Drop a local database and pull a remote copy to replace the local copy.
'''
parser = argparse.ArgumentParser(description)
parser.add_argument('-o', required=True, dest='host', help="Remote host to pull DB.")
parser.add_argument('-u', required=True, dest='user', help="Remote MySQL Client User.")
parser.add_argument('-p', required=False, dest='passwd', help="RemoteMySQL Password.")
parser.add_argument('-lu', required=False, dest='luser', help="Local MySQL Client User.")
parser.add_argument('-lp', required=False, dest='lpasswd', help="Local MySQL Passwd")
parser.add_argument('-P', required=False, dest='port', type=int, default=22, help="Remote host port")
parser.add_argument('-d', required=True, dest='db', help="Database to pull.")

args = parser.parse_args()

# Open SSH Client
print 'Opening SSH Connection'
ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.connect( args.host, args.port )

# Dumping Remote DB
print 'Dumping Remote DB'
ssh_stdin, ssh_stdout, ssh_stdrr = ssh.exec_command('mysqldump -u ' + args.user + ' -p' + args.passwd + ' --add-drop-table ' + args.db + ' > ' + args.db + '.sql' )
print ssh_stdout.read();
print ssh_stdrr.read();

# Copying to Local
print 'Copying Dump to Local'
scp = SCPClient( ssh.get_transport() )
scp.get( args.db + '.sql' )

if not args.luser:
    args.luser = args.user
    
if not args.lpasswd:
    args.lpasswd = args.passwd

os.system('mysql -u ' + args.luser + ' -p' + args.lpasswd + ' --database=' + args.db + ' < ' + args.db + '.sql' )

# Remove local copy.
os.unlink('./' + args.db + '.sql' )

# Remove remote copy.
ssh_stdin, ssh_stdout, ssh_stdrr = ssh.exec_command('rm ' + args.db + '.sql' )
print ssh_stdout.read();
print ssh_stdrr.read();
