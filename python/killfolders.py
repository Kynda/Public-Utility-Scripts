import shutil
import argparse

# Parse Command Line Arguments
parser = argparse.ArgumentParser("Kill Folders on a Given List")
parser.add_argument('-s', required=True, dest='src', help="Path to folders to Remove")

args = parser.parse_args()

with open( args.src ) as f:
    for line in f:
        line = line.replace("\n", '')
        try:
            shutil.rmtree( line )
        except OSError as e:
            print e.strerror + ' ' + line
            
        