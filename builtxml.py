import os

# os.system("rm xml/*.xml")
os.system("python gensitemap-xsl.py > xml/all.xml")
os.system("python splitter.py")
os.system("python gensitemap-index.py > xml/index.xml")
