import os
import argparse

# Parse Command Line Arguments
parser = argparse.ArgumentParser("Creates Folders For a Given List")
parser.add_argument('-s', required=True, dest='src', help="Path to folders to Make")
parser.add_argument('-d', required=True, dest='dest', help="Path to directory to Make in")

args = parser.parse_args()

with open( args.src ) as f:
    for line in f:
        line = line.replace("\n", '' )
        os.makedirs( args.dest + line )
        
        
        