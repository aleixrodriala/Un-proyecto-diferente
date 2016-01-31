from bs4 import BeautifulSoup
from collections import Counter
import urllib
import urllib2
import sys
import re
import subprocess
from subprocess import check_output
import difflib
import requests

def contestarVeu(missatge):
	subprocess.Popen(["python","/home/pi/AleixDomo/Musica/pyvonabackground.py",missatge])

missatge = sys.argv[1]
respuesta = []
listalinks = []
listaservers = []
listacompletaservers = []
Dades = [line.rstrip('\n') for line in open('/home/pi/AleixDomo/txt/pelis.txt', 'r')]


url = 'http://www.newpct1.com/buscar'
values = {'q' : missatge}

#request GET
data = urllib.urlencode(values)
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)
the_page = response.read()

soup = BeautifulSoup("".join(the_page))
urlfinallist = soup.findAll('a', href=re.compile('^http://www.newpct1.com/pelicula/'))

#busca 
for i in range(2,len(urlfinallist)):
	respuesta.append(str(urlfinallist[i]).split('/')[4])
respuesta = respuesta[:3]

respuesta = sorted(respuesta, key=lambda x: difflib.SequenceMatcher(None, x, missatge).ratio(), reverse=True)
pelicula = respuesta[0]
peliculacontestar = pelicula.replace ("-", " ")

for i in Dades:
	i = i.split("/")
	if peliculacontestar == i[0]:
		try:
			if i[1]:
				minutsave = int(i[1])
		except:
			minutsave = None


subprocess.Popen(["sudo", "python", "/home/pi/AleixDomo/Series/PeliActual/caratula.py", peliculacontestar])
peliculacontestar2 = "Poniendo: " + peliculacontestar
contestarVeu(peliculacontestar2)

url = "http://www.newpct1.com/descarga-torrent/pelicula/" + pelicula + "/"
pageFile = urllib.urlopen(url)
pageHtml = pageFile.read()
pageFile.close()
soup = BeautifulSoup("".join(pageHtml))

#part buscar links
urlfinallist = soup.findAll('div',attrs={'id':'tab3'});

for i in urlfinallist:
	ola = i.findAll('a', href=True)

for i in ola:
	link = str(i).split('href="')[1].split('"')[0]
	try:
		server = str(i).split('://www.')[1].split('.')[0]
		if server == "videoweed":
			listalinks.append(link)
			listaservers.append(server)
	except:
		try:
			server = str(i).split('://')[1].split('.')[0]
			if server == "videomega" or server == "streamcloud":
				listalinks.append(link)
				listaservers.append(server)
		except:
			pass

for x in xrange(len(listaservers)):
	listacompletaservers.append([])

for i in xrange(len(listaservers)):
	listacompletaservers[i].append(listaservers[i])
	listacompletaservers[i].append(listalinks[i])

SORT_ORDER = {"streamcloud": 0, "videoweed": 1, "videomega": 2}
listacompletaservers.sort(key=lambda val: SORT_ORDER[val[0]])

for i in xrange(len(listacompletaservers)):
		if listacompletaservers[i][0] == "streamcloud":
			pageFile = urllib.urlopen(listacompletaservers[i][1])
			pageHtml = pageFile.read()
			pageFile.close()
			soupa = BeautifulSoup("".join(pageHtml))
			ola = soupa.find('input')
			if ola != None:
				linkbo = listacompletaservers[i][1]
				break
		elif listacompletaservers[i][0] == "videoweed":
			pageFile = urllib.urlopen(listacompletaservers[i][1])
			pageHtml = pageFile.read()
			pageFile.close()
			soupa = BeautifulSoup("".join(pageHtml))
			ola = soupa.find('h3')
			if ola == None:
				linkbo = listacompletaservers[i][1]
				break
		elif listacompletaservers[i][0] == "videomega":
			linkbo = listacompletaservers[i][1]
			break
try:
	if linkbo:
		out = check_output(["youtube-dl", "-g", linkbo])
		out = out.rstrip('\n')
		try:
			minutsave = minutsave/1000000/60
			hora = "00:" + str(minutsave) + ":00"
			process = subprocess.Popen(["omxplayer", "-b", "-g","-l" ,hora, "--user-agent" ,"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36",  out])
		except:
			process = subprocess.Popen(["omxplayer", "-b ", "-g", "--user-agent" ,"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36",  out])
		process.wait()
		if 'SubmitEOS' in open('/home/pi/omxplayer.log').read():
			pass		
		else:
			for line in reversed(open("/home/pi/omxplayer.log").readlines()):
				line = line.rstrip()
				if "cur:" in line:
					linia = line.split('cur:')[1].split(',')[0]
					break
			f2 = open("/home/pi/AleixDomo/txt/pelis.txt",'a')
			f2.write(peliculacontestar + "/" + linia + "\n")
			f2.close()	
except:
	try:
		params = {'limit': 1 , 'keywords': missatge}
		r = requests.get('http://pelismag.net/api', params=params).json()
		print r
		i = r[0]
		try:
			if i['magnets']['M1080']['magnet']:
				subprocess.Popen(["peerflix", i['magnets']['M1080']['magnet'], "-o", "--", "-b"])
			else:
				subprocess.Popen(["peerflix", i['magnets']['M720']['magnet'], "-o", "--", "-b"])
		except:
			try:
				subprocess.Popen(["peerflix", i['magnets']['M720']['magnet'], "-o", "--", "-b"])
			except:
				contestarVeu("La pelicula seleccionada no existe o no esta disponible")
	except:
		contestarVeu("La pelicula seleccionada no existe o no esta disponible")
file = open("/home/pi/AleixDomo/txt/escoltar.txt", "w")
file.write("0")
file.close()
