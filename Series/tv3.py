# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import requests
import sys
import subprocess
import unicodedata

def contestarVeu(missatge):
	subprocess.Popen(["python","/home/pi/AleixDomo/Musica/pyvonabackground.py",missatge])

missatge = sys.argv[1]

Dades = [line.rstrip('\n') for line in open('/home/pi/AleixDomo/txt/seriestv3.txt', 'r')]
capitul = None

series = [['39+1', '/tv3/alacarta/39mes1/'], ['Amb C maj\xc3\xbascula', '/tv3/alacarta/amb-c-majuscula/'], ['Arr\xc3\xb2s covat', '/tv3/alacarta/arroscovat/'], ['Being human', '/tv3/alacarta/being-human/'], ['Bola de Drac', '/tv3/alacarta/bola-de-drac/'], ['Bola de Drac GT', '/tv3/alacarta/un-mite-de-lanime/'], ['Bola de drac Z', '/tv3/alacarta/bola-de-drac-z/fitxa-programa/49176/'], ['Boulevard du Palais', '/tv3/alacarta/boulevard-du-palais/'], ['Cites', '/tv3/alacarta/cites/'], ['Dues dones divines', '/tv3/alacarta/divines/'], ['El crac', '/tv3/alacarta/el-crac/'], ['El Faro, cru\xc3\xaflla de camins', '/tv3/alacarta/el-faro-cruilla-de-camins/'], ['Infidels', '/tv3/alacarta/infidels/'], ['John Adams', '/tv3/alacarta/john-adams/'], ['Julie Lescaut', '/tv3/alacarta/julie-lescaut/'], ['Kubala, Moreno i Manch\xc3\xb3n', '/tv3/alacarta/kubala-moreno-i-manchon/'], ['La mem\xc3\xb2ria dels Cargols', '/tv3/alacarta/lamemoriadelscargols/'], ['La Riera', '/tv3/alacarta/la-riera/'], ['Merli', '/tv3/alacarta/merli/'], ['One piece', '/tv3/alacarta/one-piece/fitxa-programa/201374971/'], ['Pere i J\xc3\xbalia', '/tv3/alacarta/pere-i-julia/'], ['Pop R\xc3\xa0pid', '/tv3/alacarta/pop-rapid/'], ['Riviera', '/tv3/alacarta/riviera/'], ['Sitges', '/tv3/alacarta/sitges/'], ["Unitat d'investigaci\xc3\xb3", '/tv3/alacarta/unitat-investigacio/'], ['Vent del pla', '/tv3/alacarta/ventdelpla/'], ['Xooof', '/tv3/alacarta/xooof/']]

for i in xrange(len(series)):
	serieactual = series[i][0].lower()
	serieactual = missatge.decode('utf-8') #ho passa de ASCII A utf-8 perque no doni error.
	serieactual = unicodedata.normalize('NFKD', serieactual).encode('ASCII', 'ignore') # li treu els accents i ho guarda com a ASCII
	if missatge in serieactual:
		parturl = series[i][1]
		break
try:
	capitul = sys.argv[2]
except:
	for i in Dades:
		i = i.split("/")
		if serieactual == i[0]:
			try:
				if i[2]:
					capitul = int(i[1])
					minutsave = int(i[2])
			except:
				capitul = int(i[1]) + 1
				minutsave = None

url = "http://www.ccma.cat" + parturl + "/cercador/?text=" + str(capitul) + "&data_publicacio=SEMPRE&profile=videos&items_pagina=1&ordre=-data_publicacio&programa_id=43405"

headers = { 'User-Agent' : 'Mozilla/5.0' }
req = urllib2.Request(url, None, headers)
html = urllib2.urlopen(req).read()
try:
	soup = BeautifulSoup("".join(html))
	urlfinallist = soup.findAll("a", { "class" : "F-capsaImatge" })

	idvideo = str(urlfinallist).split("/video/")[1].split("/")[0]

	url = "http://dinamics.ccma.cat/pvideo/media.jsp?media=video&version=0s&idint=" + idvideo +"&profile=mobil"
	r = requests.get(url).json()

	urlvideo = r['media']['url']

	try:
		minutsave = minutsave/1000000/60
		hora = "00:" + str(minutsave) + ":00"
		process = subprocess.Popen(["omxplayer", "-g","-l" ,hora, "--user-agent" ,"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36",  urlvideo])
	except:
		process = subprocess.Popen(["omxplayer", "-g", "--user-agent" ,"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36",  urlvideo])

	process.wait()

	if 'SubmitEOS' in open('/home/pi/omxplayer.log').read():
		f2 = open("/home/pi/AleixDomo/txt/seriestv3.txt",'a')
	  	f2.write(missatge + "/" + str(capitul) + "\n")
	   	f2.close()		
	else:
		for line in reversed(open("/home/pi/omxplayer.log").readlines()):
			line = line.rstrip()
			if "cur:" in line:
				linia = line.split('cur:')[1].split(',')[0]
				break
		f2 = open("/home/pi/AleixDomo/txt/seriestv3.txt",'a')
		f2.write(missatge + "/" + str(capitul) + "/" + linia + "\n")
		f2.close()
	file = open("/home/pi/AleixDomo/txt/escoltar.txt", "w")
	file.write("0")
	file.close()	
except:
	contestarVeu("Ha habido un error, pruebe otra vez.")
	file = open("/home/pi/AleixDomo/txt/escoltar.txt", "w")
	file.write("0")
	file.close()	
	sys.exit(1)