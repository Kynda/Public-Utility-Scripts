#! /usr/bin/env python

import os
import argparse

# Parse Comand Line Arguments
parser = argparse.ArgumentParser("Generate a Dig Report For a Given List of Sites")
parser.add_argument('-s', required=True, dest='src', help="Path to sites.txt")

args = parser.parse_args()

with open( args.src ) as f:
    for line in f:

        # Get Host
        os.system( 'host ' + line )
        os.system( 'dig NS +short ' + line)
        os.system( 'printf "\n\n"' )