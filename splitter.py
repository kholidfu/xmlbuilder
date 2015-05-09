"""
split giant xml into small chunk with max num of url tag 
per xml is lim

steps:
1. run python gensitemap-xsl.py > index.xml
2. run python splitter.py
"""
from math import ceil
import re
import os


with open("xml/all.xml") as f:
    xmlstr = f.read()

with open("xml/all.xml") as f:
    allxml = f.readlines()

pre = allxml[:3]
main = allxml[3:-1]
back = allxml[-1]

lim = 400

numofpdffiles = sum([len(f) for r, d, f in os.walk("assets")])

numofxmlfile = int(ceil(numofpdffiles/float(lim)))  # 6

allurltag = re.findall("<url>.*?</url>\\n", xmlstr, re.DOTALL)

for i in range(numofxmlfile):
    with open("xml/archive-%s.xml" % i, "w") as f:
        f.write("".join(pre))
        f.write("".join(allurltag[i*lim:(i+1)*lim]))
        f.write("".join(back))
