"""
split giant xml into small chunk with max num of url tag 
per xml is lim

sesuaikan folder "assets"

steps:
1. run python gensitemap-xsl.py > index.xml
2. run python splitter.py
"""
from math import ceil
import re
import os


LIM = 5000

with open("xml/all.xml") as f:
    xmlstr = f.read()

with open("xml/all.xml") as f:
    allxml = f.readlines()

pre = allxml[:3]
main = allxml[3:-1]
back = allxml[-1]

numofpdffiles = sum([len(f) for r, d, f in os.walk("books")])
numofxmlfile = int(ceil(numofpdffiles/float(LIM)))  # 6
allurltag = re.findall("<url>.*?</url>\\n", xmlstr, re.DOTALL)

for i in range(numofxmlfile):
    with open("xml/archive-%s.xml" % i, "w") as f:
        f.write("".join(pre))
        f.write("".join(allurltag[i*LIM:(i+1)*LIM]))
        f.write("".join(back))
