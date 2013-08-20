#! /usr/bin/env python

import paramiko
from scp import SCPClient
import argparse

#Parse Command Line Arguments
parser = argparse.ArgumentParser("Automated Remote Folder Backup")
parser.add_argument('-o', required=True, dest='host',   help="SSH Host")
parser.add_argument('-r', required=True, dest='path',	help="Path on remote host to folder to copy. Include trailing /")
parser.add_argument('-port', required=False, dest='port', 	default=22,	help="MySQL Port" )
parser.add_argument('-u', required=True, dest='user', 	help="MySQL user name" )
parser.add_argument('-p', required=True, dest='passwd', help="MySQL password" )

args = parser.parse_args()

# Get List of files to compress
ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.connect(args.host, args.port, args.user, args.passwd )

ssh_stdin, ssh_stdout, ssh_stdrr = ssh.exec_command('ls -1A '+args.path)
folders = ssh_stdout

scp = SCPClient(ssh.get_transport())

# Loop through list. (1) tar file, (2) download file, (3) delete tar file
for folder in folders:
	folder = folder.strip()

	ssh_stdin, ssh_stdout, ssh_stdrr = ssh.exec_command('tar -czvf ' + args.path + folder + '.tgz ' + args.path + folder )
	print ssh_stdout.read();
	print "Created " + folder + '.tgz'

	scp.get(args.path+folder+'.tgz')
	print "Copied to local"
	
	ssh_stdin, tar_stdout, ssh_stdrr = ssh.exec_command('rm ' + args.path + folder + '.tgz' )	
	print "Removed remote copy"

print "All Files Have Been Copied" 
