from bs4 import BeautifulSoup
from collections import Counter
import urllib
import urllib2
import sys
import re
import subprocess
import os
import time
import requests
from subprocess import check_output

def contestarVeu(missatge):
	subprocess.Popen(["python","/home/pi/AleixDomo/Videos/pyvonabackground.py",missatge])

def cargarWeb(url):
	global html
	headers = { 'User-Agent' : 'Mozilla/5.0' }
	r = requests.get(url, headers=headers)
	return r

capitulos = []
listalinks = []
listaservers = []

missatge = sys.argv[1]
Dades = [line.rstrip('\n') for line in open('/home/pi/AleixDomo/txt/series.txt', 'r')]
temporadasave = None
capitulsave = None

if missatge == "los simpsons":
	missatge = "los simpson"

global linkbo
global linkantic

try:
	temporadasave = sys.argv[2]
	capitulsave = sys.argv[3]
	temporadasave = int(temporadasave)
	capitulsave = int(capitulsave)
except:
	for i in Dades:
		i = i.split("/")
		if missatge == i[0]:
			temporadasave = int(i[1])
			try:
				if i[3]:
					capitulsave = int(i[2])
					minutsave = int(i[3])
			except:
				capitulsave = int(i[2]) + 1
				minutsave = None

subprocess.Popen(["sudo", "python", "/home/pi/AleixDomo/Series/SerieActual/caratula.py", missatge])

def TrobarLinkSiFalla():
	global minutsave
	global linkbo
	global process
	listalinks2 = []
	capitulosx = []
	url = 'http://www.seriesblanco.com/finder.php'
	values = {'query' : missatge}
	headers = { 'User-Agent' : "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36" }
	data = urllib.urlencode(values)
	req = urllib2.Request(url, data, headers)
	response = urllib2.urlopen(req)
	the_page = response.read().split("<a href='")[1].split("'>")[0]

	url = "http://seriesblanco.com" + the_page

	soup = BeautifulSoup("".join(cargarWeb(url)))
	urlfinallistx = soup.findAll('a', href=re.compile('/capitulo'))

	for i in urlfinallistx:
		i = str(i).split('href="')[1].split('">')[0]
		capitulosx.append(i)

	temporadasx = capitulosx[-1].split("/temporada-")[1].split("/")[0]

	listacompletax = []

	for x in xrange(int(temporadasx)):
		listacompletax.append([])

	for i in capitulosx:
		temporada = i.split("/temporada-")[1].split("/")[0]
		temporada = int(temporada)
		listacompletax[temporada - 1].append(i)
	try:
		url = "http://seriesblanco.com" + listacompletax[temporadasave - 1][capitulsave - 1]
	except:
		contestarVeu("No hay links disponibles para su episodio, lo sentimos mucho")
		file = open("/home/pi/AleixDomo/txt/escoltar.txt", "w")
		file.write("0")
		file.close()	
		sys.exit()

	soup = BeautifulSoup("".join(cargarWeb(url)))

	llistabruta = soup.findAll('td', attrs = {'class' : 'tam12'})
	sionox = False
	for i in llistabruta:
		i = str(i)
		if "/servidores/" in i:
			if "<center>" in i:
				servidores = i.split("servidores/")[1].split(".")[0]
				link = i.split('href="')[1].split('"')[0]
				if servidores == "streamcloud":
					sionox = True
			else:
				break
		elif "/banderas/" in i:
			if sionox == True:
				if "/banderas/es.png" in i:
					listalinks2.append(link)
			sionox = False
	listalinks2 = listalinks2[:-1]	

	for i in listalinks2:
		i = "http://seriesblanco.com" + i
		soup = BeautifulSoup("".join(cargarWeb(i)))
		linkfinal = soup.find('input', {'type': 'button'})
		linkfinal = str(linkfinal).split('window.open("')[1].split('"')[0]
		pageFile = urllib.urlopen(linkfinal)
		pageHtml = pageFile.read()
		pageFile.close()
		soup = BeautifulSoup("".join(pageHtml))
		ola = soup.find('input')
		if ola != None:
			linkbo = linkfinal
			break
		else:
			pass
	try:	
		if linkbo:
			contestar = "Poniendo: " + missatge + "Temporada: " + str(temporadasave) + "Capitulo: " + str(capitulsave)
			contestarVeu(contestar) 
			out = check_output(["youtube-dl", "-g", linkbo])
			out = out.rstrip('\n')
			try:
				minutsave = minutsave/1000000/60
				hora = "00:" + str(minutsave) + ":00"
				process = subprocess.Popen(["omxplayer", "-g","-l" ,hora, "--user-agent" ,"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36",  out])
			except:
				process = subprocess.Popen(["omxplayer", "-g", "--user-agent" ,"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36",  out])
	except:
		contestarVeu("No hay links disponibles para su episodio, lo sentimos mucho")
		os.system("sudo pkill -f caratula.py")
		file = open("/home/pi/AleixDomo/txt/escoltar.txt", "w")
		file.write("0")
		file.close()	
		sys.exit()
		
	process.wait()
	if 'SubmitEOS' in open('/home/pi/omxplayer.log').read():
		f2 = open("/home/pi/AleixDomo/txt/series.txt",'a')
	  	f2.write(missatge + "/" + str(temporadasave) + "/" + str(capitulsave) + "\n")
	   	f2.close()		
	else:
		for line in reversed(open("/home/pi/omxplayer.log").readlines()):
			line = line.rstrip()
			if "cur:" in line:
				linia = line.split('cur:')[1].split(',')[0]
				break
		f2 = open("/home/pi/AleixDomo/txt/series.txt",'a')
		f2.write(missatge + "/" + str(temporadasave) + "/" + str(capitulsave) +  "/" + linia + "\n")
		f2.close()
	file = open("/home/pi/AleixDomo/txt/escoltar.txt", "w")
	file.write("0")
	file.close()	


url = 'http://www.seriesflv.net/api/search'
values = {'q' : missatge}
headers = { 'User-Agent' : "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36" }
r = requests.get(url, params = values, headers= headers).text
soup = BeautifulSoup("".join(r))
urlfinallist = soup.findAll('a', href=re.compile('/serie/'))

urlfinallist = str(urlfinallist[0]).split('href="')[1].split('">')[0]

soup = BeautifulSoup("".join(cargarWeb(urlfinallist)))
urlfinallist = soup.findAll('a', href=re.compile('/ver/'))

for i in urlfinallist:
	i = str(i).split('href="')[1]
	capitulos.append(i.split('">')[0])

temporadas = capitulos[-1].split("/")[4]
temporadas = re.findall(r'\d+',temporadas)[0]

listacompleta = []

for x in xrange(int(temporadas)):
	listacompleta.append([])

for i in capitulos:
	temporada = i.split("/")[4]
	temporada = re.findall(r'\d+',temporada)[0]
	temporada = int(temporada)
	listacompleta[temporada - 1].append(i)
try:
	url = listacompleta[temporadasave - 1][capitulsave - 1]
except:
	try:
		url = listacompleta[temporadasave][0]
		temporadasave = temporadasave + 1
		capitulsave = 1
	except:
		contestarVeu("La temporada o el capitulo no existe, vuelve a decir la temporada y el capitulo")
		sys.exit(1)

soup = BeautifulSoup("".join(cargarWeb(url)))

llistabruta = soup.find_all('tr')[1:]

for i in xrange(len(llistabruta)):
	#try:
	print llistabruta[i]
	if 'class="e_server"' in str(llistabruta[i]):
		servers = str(llistabruta[i]).split('width="16"> ')[1].split('</img>')[0]
		links = str(llistabruta[i]).split('href="')[1].split('"')[0]
		idioma = str(llistabruta[i]).split('/lang/')[1].split('.png')[0]
		if servers == "nowvideo" or servers == "streamcloud":
			if idioma == "es":
				listaservers.append(servers)
				listalinks.append(links)
	else:
		break
		
listacompletaservers = []

for x in xrange(len(listaservers)):
	listacompletaservers.append([])

for i in xrange(len(listaservers)):
	listacompletaservers[i].append(listaservers[i])
	listacompletaservers[i].append(listalinks[i])

SORT_ORDER = {"streamcloud": 0, "nowvideo": 1}
listacompletaservers.sort(key=lambda val: SORT_ORDER[val[0]])
def TrobarLink(linkanticono):
	global minutsave
	global linkbo
	global process
	for i in xrange(len(listacompletaservers)):
		if listacompletaservers[i][0] == "streamcloud":
			soup = BeautifulSoup("".join(cargarWeb(listacompletaservers[i][1])))
			linkfinal = soup.find_all('a', id="continue")
			linkfinal = str(linkfinal).split('<a href="')[1].split('"')[0]
			pageFile = urllib.urlopen(linkfinal)
			pageHtml = pageFile.read()
			pageFile.close()
			soup = BeautifulSoup("".join(pageHtml))
			ola = soup.find('input')
			if ola != None:
				if linkanticono == "si":
					if linkbo != linkfinal:
						linkbo = linkfinal
						break
				else:
					linkbo = linkfinal 
					break 
					
		elif listacompletaservers[i][0] == "nowvideo":
			soup = BeautifulSoup("".join(cargarWeb(listacompletaservers[i][1])))
			linkfinal = soup.find_all('a', id="continue")
			linkfinal = str(linkfinal).split('<a href="')[1].split('"')[0]
			pageFile = urllib.urlopen(linkfinal)
			pageHtml = pageFile.read()
			pageFile.close()
			soup = BeautifulSoup("".join(pageHtml))
			ola = soup.find('<h3>')
			if ola == None:
				if linkanticono == "si":
					if linkbo != linkfinal:
						linkbo = linkfinal
						break
				else:
					linkbo = linkfinal 
					break 
	try:	
		if linkbo:
			contestar = "Poniendo: " + missatge + "Temporada: " + str(temporadasave) + "Capitulo: " + str(capitulsave)
			contestarVeu(contestar) 
			out = check_output(["youtube-dl", "-g", linkbo])
			out = out.rstrip('\n')
			try:
				minutsave = minutsave/1000000/60
				hora = "00:" + str(minutsave) + ":00"
				process = subprocess.Popen(["omxplayer", "-g","-l" ,hora, "--user-agent" ,"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36",  out])
			except:
				process = subprocess.Popen(["omxplayer", "-g", "--user-agent" ,"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36",  out])
	except:
		contestarVeu("No hay links disponibles en este servidor, buscando en otro servidor, espere porfavor")
		TrobarLinkSiFalla()

TrobarLink("")
segons = 0
while True:
	if segons > 25:
		contestarVeu("Ha habido un error, deja que intente arreglarlo...")
		TrobarLink("si")
		break
	segons = segons + 1
	try:
		out = check_output(["/home/pi/AleixDomo/Musica/dbuscontrol.sh", "status"])
		if "Duration:" in out:
			break
		time.sleep(1)
	except:
		time.sleep(1)
process.wait()
if 'SubmitEOS' in open('/home/pi/omxplayer.log').read():
	f2 = open("/home/pi/AleixDomo/txt/series.txt",'a')
  	f2.write(missatge + "/" + str(temporadasave) + "/" + str(capitulsave) + "\n")
   	f2.close()		
else:
	for line in reversed(open("/home/pi/omxplayer.log").readlines()):
		line = line.rstrip()
		if "cur:" in line:
			linia = line.split('cur:')[1].split(',')[0]
			break
	f2 = open("/home/pi/AleixDomo/txt/series.txt",'a')
	f2.write(missatge + "/" + str(temporadasave) + "/" + str(capitulsave) +  "/" + linia + "\n")
	f2.close()
file = open("/home/pi/AleixDomo/txt/escoltar.txt", "w")
file.write("0")
file.close()	