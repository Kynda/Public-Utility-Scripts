import datetime
import argparse
import tarfile
import os
import glob

# Parse Command Line Arguments
description = '''
This script generates a tarball of a specified destination and copies it to a specified local directory. Include trailing '/' on directory paths!
'''
parser = argparse.ArgumentParser(description)
parser.add_argument('-s', required=True, dest='src', help='Path to directory to backup.')
parser.add_argument('-d', required=True, dest='dest', help='Path to directory to put backup.')
parser.add_argument('-f', required=False, dest='file', help='Alternative prefix for tar file.')
parser.add_argument('-u', required=False, dest='user', help='User to chmod tarball to on completion.')
parser.add_argument('--remove', required=False, dest='remove', help='Remove existing backups if found in destination.')

args = parser.parse_args()

# Get ymd
now = datetime.datetime.now();
ymd = str(now.year) + '-' + str( now.month ) + '-' + str( now.day )

# Generate file name parts
pre = 'backup-'
ext = '.tgz'

if args.file:
	pre = args.file

# Full dest name
dest_path =  args.dest + pre + ymd + ext

# Remove existing if flag is set.
if args.remove:
	print "Removing old backups"
	for filename in glob.glob( args.dest + pre + '*' + ext ):
		print "Removing "+filename
		os.remove( filename )


# Create Archive
print "Creating archive for " + args.src
print "Putting archive in " + dest_path

with tarfile.open( dest_path, mode="w:gz") as tarball:
	tarball.add( args.src, arcname=os.path.basename( args.src ) )

print "Tarball created"

if args.user:
	print 'Changing ownership of backup to '+args.user
	os.system('chown '+args.user+' '+dest_path)
