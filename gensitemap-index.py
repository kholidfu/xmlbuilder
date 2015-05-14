"""
 gensitemap.py - generate a site map based on googles SiteMap specification
 Protocol:  https://www.google.com/webmasters/sitemaps/docs/en/protocol.html


 variations of note:  metadata (such as how often to index the file) will be in
  filename.metadata.  If you want to override the default frequency and priority,
  create a file called "whatever-the-filename-was".metadata with the xml lines:
  
<changefreq>whatever</changefreq>
<priority>whatever</priority>

 Output is to stdout.  Redirect to a file if you want to save the output.  Pipe
 through gzip if you want it gzipped.

"""

import os
import string
import time
import pytz
import xml.sax.saxutils
import datetime
import sys


#
# Document extentions we are interested in generating data for.
#
EXTENSIONS = (".xml")

DOMAIN = "http://%s.com/" % sys.argv[1]

# The default default is "Never"
DEFAULT_FREQ = "always"
DEFAULT_PRIORITY = "1.0"


def recurse_directories ( rootdir="" ):
    container = []
    for file in os.listdir( os.getcwd() + os.sep + rootdir):
        if os.path.isdir(os.getcwd() + os.sep + rootdir + os.sep + file):
            recurse_directories(rootdir + os.sep + file)
        else:
            found = False
            for each in EXTENSIONS:
                if string.find(file, each) > -1 and string.find(file, ".metadata") == -1 and string.find(file, "~") == -1 and string.find(file, ".bak") == -1:
                    found = True
                    break
               
            if found == True and file != "index.xml" and file != "all.xml" and not ".xsl" in file:


                modtime = os.path.getmtime(os.getcwd() + os.sep + rootdir + os.sep + file)

                # iso_time = time.strftime( "%Y-%m-%dT%H:%M:%S", time.localtime(modtime) )
                iso_time = datetime.datetime.fromtimestamp(modtime).replace(tzinfo=pytz.utc).isoformat()
                # iso_time = time.strftime( "%Y-%m-%d", time.localtime(modtime) )                
                url = xml.sax.saxutils.escape( DOMAIN + string.replace(rootdir, os.sep, "/") + "/" + file)


                print "<url>"
                print "  <loc>" + url +"</loc>"
                print "  <lastmod>" + str(iso_time) + "</lastmod>"

                # if there is a filename.metadata file, include that now
                try:
                    f = open(os.getcwd() + os.sep + rootdir + os.sep + file + ".metadata")
                    lines = f.readlines()

                    for line in lines:
                        print "  " + line

                except:
                    print "  <changefreq>" + DEFAULT_FREQ + "</changefreq>"
                    print "  <priority>" + DEFAULT_PRIORITY + "</priority>"
                
                print "</url>";


print """<?xml version="1.0" encoding="UTF-8"?>"""
print """<?xml-stylesheet type="text/xsl" href="/sitemap.xsl"?>"""
print """<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">"""

recurse_directories("xml")

print "</urlset>"

