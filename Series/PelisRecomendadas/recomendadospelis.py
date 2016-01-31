
from bs4 import BeautifulSoup
import subprocess
import urllib
import sys
import urllib2
import simplejson
import cStringIO
import re

url = "http://www.newpct1.com/"
pageFile = urllib.urlopen(url)
pageHtml = pageFile.read()
pageFile.close()

soup = BeautifulSoup("".join(pageHtml))
ola = soup.find_all(text=re.compile("var arrayMODEC"));
ola = str(ola).split("var arrayMODEC")[1].split("']];")[0]
ola = ola.split(",")

for i in range(3,len(ola),6):
	olanova = ola[i].replace("'", "")
	olanova = olanova.replace("\\", "")
	fetcher = urllib2.build_opener()
	olanova = olanova + "filmaffinity"
	olanova = olanova.replace(" ", "%20")
	searchUrl = "http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=" + olanova + "&xlarge" + "&as_sitesearch=filmaffinity.com"
	f = fetcher.open(searchUrl)
	deserialized_output = simplejson.load(f)
	imageUrl = deserialized_output['responseData']['results'][0]['unescapedUrl']
	urllib.urlretrieve(imageUrl, str(i) + ".jpg")
	