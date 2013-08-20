import os
import argparse

# Parse Command Line Arguments
description = '''
This script uses mysqldump to dump each database specified in a new-line seperated file. 
'''
parser = argparse.ArgumentParser(description)
parser.add_argument('-s', required=True, dest='src', help="Path to new-line seperated file listing databases to dump.")
parser.add_argument('-u', required=True, dest='user', help="MySQL username")
parser.add_argument('-p', required=True, dest='passwd', help="MySQL password")

args = parser.parse_args()

with open( args.src ) as f:
	for line in f:
		line = line.replace("\n", '')		
		os.system( 'mysqldump -u '+args.user+' -p'+args.passwd+' '+line+' > '+line+'.sql' )