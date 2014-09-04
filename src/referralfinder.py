import urllib2
import httplib
from bs4 import BeautifulSoup

base = 'example.com' 
crawled = []

def Crawl( path ):
	
	print( 'CRAWLING ' + path )
	
	try:
		response = urllib2.urlopen( path )
	except httplib.InvalidURL:
		print "Invalid URL " + path
		return 
	except urllib2.URLError:
		print "Invalid URL " + path
		return
		
		
	html = response.read()	
	soup = BeautifulSoup( html )
	anchors = soup.find_all('a')
		
	
	for anchor in anchors:					
		link = anchor.get('href')	
							
		if not ( link in crawled ) and link:	
			crawled.append( link )		
			print( link )
				
			if link.find( 'http' ) == -1:
				if( link.find( '/' ) == 0 ):
					Crawl( base + link )
				else:		
					Crawl( base + '/' + link )
			elif link.find( base ) is not -1:
				Crawl( link )
			else:
				print("NOT ON BASE")
				
Crawl( base )
				
				
		

		
	
