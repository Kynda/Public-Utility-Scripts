import os
import fnmatch
import argparse

# Parse Command Line Arguments
parser = argparse.ArgumentParser("Remove string from all *.txt files in a given folder and subfolders.")
parser.add_argument('-p', required=True, dest='src', help="Path to folders to Remove")
parser.add_argument('-f', required=True, dest='strs', help="Path to a newline seperated file of strings to remove")

args = parser.parse_args()

strings=[]
with open( args.strs ) as lines:
    for line in lines:
        strings.append( line.replace("\n", '') )    

for root, dirs, files in os.walk( args.src ):
    for filename in fnmatch.filter( files, '*.txt' ):        
        # Get path to file.
        abs_file = os.path.join( root, filename )
                                
        with open( abs_file ) as page:
            content = page.read()                    
            for string in strings:
                if( content.find( string ) != -1 ):                    
                    cleaned_content = content.replace( string, '********' )
                    with open( abs_file, 'w' ) as page:
                        page.write( cleaned_content )
                        print 'cleaned ' + abs_file
        