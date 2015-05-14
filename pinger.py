"""
ngeping secara random 100x
jeda antara 5 sampai 7 menit
sehingga selesai dalam ~ 10 jam                        
"""

import urllib2
import sys
import re
import time
import logging
import random


url = "http://%s/xml/" % sys.argv[1]
xml = urllib2.urlopen(url).read()
pattern = re.compile(r"\"([ai].*?\.xml)")
xmls = re.findall(pattern, xml)

# config
logging.basicConfig(filename="pinger.log",
                   level=logging.INFO,
                   format='%(asctime)s %(message)s',
                   datefmt='%m/%d/%Y %H:%M:%S %p')

count = 0
while count < 100:
    for xml in xmls:
        fullxml = "http://%s/xml/%s" % (sys.argv[1], xml)
        goping_url = "http://www.google.com/webmasters/sitemaps/" \
                     "ping?sitemap="
        resp3 = urllib2.urlopen("%s%s" % (goping_url, fullxml))
        if resp3.code == 200:
            logging.info("%s submitted!" % xml)
        else:
            logging.info("%s gagal!" % xml)
            continue
    count +=1
    time.sleep(random.randint(300, 420))
