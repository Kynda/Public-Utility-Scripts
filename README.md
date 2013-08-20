#Python Utility Scripts
-------------------------------------------------------------------------------
This repository represents a small collection of stand-alone command line scripts that I have written to automate the managing of a LAMP stack server easier.

##Features

###backup.py
Create a tarball from a given source and moves it to a remote destination via SSH. Optionally removes existing backups in the destination.

###localbackup.py
Creates a tarball and moves it to a given directory. Optionally removes existing backups from destination and changes sets ownership of backup on completion.

###remotebackup.py
Given a remote host and directory, remotebackup.py will tarball each subdirectory in the given directory and move the tarball to a local directory.

###commit.py
Stages and commits all changes in a given repository with a timestamp as the message. Good as a cron job to automatically commit the day's changes in case you forgot.

###dbbackup.py
Uses the MySQLdb package to fetch a list of local MySQL databases and dumps each as individual dump files.

###dbbackup2.py
Similar to db_backup.py. Reads a new-line seperated list of database names and dumps each as an individual file.

###dig.py
Reads a new-line seperated list of domain names and returns the results of running 'host' and 'dig NS +short' against them.

###killfolders.py
Reads a new-line seperated list of directories and removes them and their subdirectories.

###mkdirs.py
Reads a new-line seperated list of directories and makes each of them.

##Requirements
- Python 2.7+
- Some scripts require the MySQLdb package
- Some scripts required configured SSH credentials and keys on remote hosts
- Scripts tested against Linux-based systems

##ChangeLog
-------------------------------------------------------------------------------

###Version 1.0.0
####August 20, 2013
- Initial Commit

##License
This code is released under the [MIT License](http://opensource.org/licenses/MIT)

