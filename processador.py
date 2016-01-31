# -*- coding: utf-8 -*-
import subprocess
import re
from layer import enviarWhats
import pyvona
from subprocess import check_output
from bs4 import BeautifulSoup
import requests
import time
import datetime
import unicodedata
import geolocation
import recordatoris
from googlesearch import aconseguirResposta 
from spoticlient import Spotipy
from Veu import ControladorVeu
from telegrambot import ControladorTelegram
import threading
import pymongo
from temperatura import TemperaturaActual
import processador1
import os

class Processador:
	def __init__(self):
		self.status = None
		self.ipprocc = False
		self.especial = False
		self.veu = ControladorVeu()
		self.telegram = ControladorTelegram()
		self.events = None
		self.entrada = None
		self.missatge = None
		self.spoticanso = None
		self.ultimissatge = None
		self.domoconfig = False
		self.clientmongo = pymongo.MongoClient("localhost", 27017)
		self.db = self.clientmongo['ProjectDB']
		self.funcions = self.db['Funcions'].find(no_cursor_timeout=True).sort("id", 1)
		self.inici()

	def on_message(self, entrada, e):
		e.wait()		
		self.entrada = entrada		
		if entrada == 1:
			self.missatge = self.veu.missatge
		elif entrada == 2:
			self.missatge = self.telegram.missatge
		self.setEvents(entrada)
		if self.especial:
			self.especial = False
		else:
			self.processarparaula()

	def on_whats(self, selfwhats, missatge, sender):
		self.entrada = 3
		self.selfwhats = selfwhats
		self.missatge = missatge
		self.sender = sender
		self.processarparaula()

	def inici(self):
		self.veu.start()
		self.telegram.start()
		self.setEvents(1)
		self.setEvents(2)

	def setEvents(self, entrada):
		if entrada == 1:
			threading.Thread(target=self.on_message, args=(1, self.veu.missatgeready)).start()
		elif entrada == 2:
			threading.Thread(target=self.on_message, args=(2, self.telegram.missatgeready)).start()

	def contestarVeu(self, missatge):
		self.updateStatus("Parlan")
		funciona = False
		while funciona == False:
			try:
				v = pyvona.create_voice("GDNAIOIEYJ4TLER6BWMQ", "0keM4rjAabbuEsVXMM9+/C+Ewn8af/ZokV5/BzwI")
				v.speak(missatge)
				time.sleep(0.5)
				funciona = True
			except: 
				time.sleep(1)
		if not self.veu.playing:
			self.updateStatus(False)
		else:
			self.updateStatus(True)

	def enviarTelegram(self, missatge):
		self.telegram.contestarTelegram(missatge)		

	def contestar(self, missatge):
		if self.entrada == 1:
			self.updateStatus("Parlan")
			self.contestarVeubackground(missatge)
			if not self.veu.playing:
				self.updateStatus(False)
			else:
				self.updateStatus(True)
		elif self.entrada == 2:
			self.enviarTelegram(missatge)
		elif self.entrada == 3:
			enviarWhats(missatge, self.sender, self.selfwhats)

	def contestarVeubackground(self,missatge):
		process = subprocess.Popen(["python","/home/pi/AleixDomo/pyvonabackground.py",missatge])
		process.wait()

	def getParaula(self):
		self.especial = True
		self.db['BotoStatus'].update({'id': None}, {'status': True}, upsert=True)
		missatgeantic = self.missatge
		while missatgeantic == self.missatge:
			time.sleep(0.5)
		return self.missatge

###########################Funcions############################
	def conversa(self):
		if self.entrada == 2 or self.entrada == 3:
			self.contestar("Hola! Para saber un poco mas sobre mi escribe Ayuda")
		elif self.entrada == 1:
			self.contestarVeu("Hola, como estas?")

	def multimedia(self):
		Musica = True
		if not self.spoticanso:
			self.spoticanso = Spotipy()
			self.veu.spoticanso = self.spoticanso
		if 'lista' in self.missatge.split():
			llista = self.missatge.split('lista ')[1]
			self.updateStatus(True)
			if self.entrada == 2 or self.entrada == 3:
				self.contestar('Poniendo musica...')
			if not self.spoticanso.playPlaylist(llista):
				self.contestar('No se ha encontrado su lista')
				self.updateStatus(False)
		else:
			missatge = self.missatge.split(' ', 1)[1].replace('un poco ', '').replace('lo mejor ', '')
			if "de" in missatge.split():
				missatge = re.sub(r'\bde\b','', missatge)
			self.updateStatus(True)
			if self.entrada == 2 or self.entrada == 3:
				self.contestar('Poniendo musica...')
			if not self.spoticanso.play(missatge):
				self.contestar('No he podido econtrar su lista')
				Musica = False
			if not Musica:
				self.updateStatus(False)

	def setupDomo(self):
		try:
			self.db['ConfigDomo'].drop()
		except:
			pass
		try:
			passar = False
			passar2 = False
			while not passar:
				try:
					self.contestar('En que posiciones del rele has conectado tus dispositivos? Di el numero de cada uno.')
					preNumero = self.getParaula()
					print preNumero
					numero = re.findall('\d+', preNumero)
					for i in xrange(len(numero)):
						if len(numero[i]) > 1:
							numero[i] = list(numero[i])

					self.contestar('Son estas tus posiciones del rele? ' + '...'.join(numero))
					while not passar2:
						try:
							resposta = self.getParaula()
							if "si" in resposta:
								passar = True
								passar2 = True
							else:
								self.contestar('Parece que hemos empezado con mal pie, mejor si volvemos a empezar.') 
								passar2 = True
						except:
							self.contestar('Vuelve a decirlo')
				except:
					self.contestar('Ha habido un error, volvamos a empezar')
			p = {}
			for i in numero:
				passar = False
				while not passar:
					try:
						self.contestar('Que has conectado en el rele ' + str(i) + ' ?')
						cosaconectada = self.getParaula()
						if len(cosaconectada.split(' ',1)[0]) <= 3:
							cosaconectada = cosaconectada.split(' ',1)[1]
						p[cosaconectada] = int(i) - 1
					   	passar = True
				   	except:
				   		pass
	   		self.db['ConfigDomo'].insert(p)
	   		self.contestar('Domotica configurada correctamente')
   		except:
   			self.contestar('Ha habido un error, vuelva a empezar.')
			   

	def chisteAleatorio(self):
		req = urllib2.Request("http://pagina-del-dia.euroresidentes.es/chiste-del-dia/gadget-chiste-del-dia.php?modo=2")
		response = urllib2.urlopen(req)
		the_page = response.read()
		the_page = the_page.split('<td colspan="4" bgcolor="#FFFFFF">')[1].split('</td>')[0]
		if "<br>" in the_page:
			the_page = the_page.replace("<br>", "...")
		return the_page

	def guardarSerie(self, serie):
		file = open("/home/pi/AleixDomo/txt/seriemobils.txt", "w")
		file.write(serie)
		file.close()

	def checkCapitul(self, serie, TV3):
		serietrobada = 0
		if TV3 == True:
			Dades = [line.rstrip('\n') for line in open('/home/pi/AleixDomo/txt/seriestv3.txt', 'r')]
		else:
			Dades = [line.rstrip('\n') for line in open('/home/pi/AleixDomo/txt/series.txt', 'r')]
		for i in Dades:
			i = i.split("/")
			if serie in i[0]:
				if TV3 == True:
					subprocess.Popen(["python","/home/pi/AleixDomo/Series/tv3.py", serie])
				else:
					subprocess.Popen(["python","/home/pi/AleixDomo/Series/obtenirseriesflv.py", serie])
				serietrobada = 1
				break
		if serietrobada != 1:
			if TV3 == True:
				self.contestar("No has visto nunca esta serie, que capitulo quieres ver?")
				if self.entrada == 1:
					self.db['BotoStatus'].update({'id': None}, {'status': True}, upsert=True)
				self.guardarSerie(serie)
			else:
				self.contestar("No has visto nunca esta serie, que temporada y que capitulo quieres ver?")
				if self.entrada == 1:
					self.db['BotoStatus'].update({'id': None}, {'status': True}, upsert=True)
				self.guardarSerie(serie)
			return True
		else:
			return True

	def checkSerieTV3(self, serie):
	    seriestv3 = [['39+1', '/tv3/alacarta/39mes1/'], ['Amb C maj\xc3\xbascula', '/tv3/alacarta/amb-c-majuscula/'], ['Arr\xc3\xb2s covat', '/tv3/alacarta/arroscovat/'], ['Being human', '/tv3/alacarta/being-human/'], ['Bola de Drac', '/tv3/alacarta/bola-de-drac/'], ['Bola de Drac GT', '/tv3/alacarta/un-mite-de-lanime/'], ['Bola de drac Z', '/tv3/alacarta/bola-de-drac-z/fitxa-programa/49176/'], ['Boulevard du Palais', '/tv3/alacarta/boulevard-du-palais/'], ['Cites', '/tv3/alacarta/cites/'], ['Dues dones divines', '/tv3/alacarta/divines/'], ['El crac', '/tv3/alacarta/el-crac/'], ['El Faro, cru\xc3\xaflla de camins', '/tv3/alacarta/el-faro-cruilla-de-camins/'], ['Infidels', '/tv3/alacarta/infidels/'], ['John Adams', '/tv3/alacarta/john-adams/'], ['Julie Lescaut', '/tv3/alacarta/julie-lescaut/'], ['Kubala, Moreno i Manch\xc3\xb3n', '/tv3/alacarta/kubala-moreno-i-manchon/'], ['La mem\xc3\xb2ria dels Cargols', '/tv3/alacarta/lamemoriadelscargols/'], ['La Riera', '/tv3/alacarta/la-riera/'], ['Merli', '/tv3/alacarta/merli/'], ['One piece', '/tv3/alacarta/one-piece/fitxa-programa/201374971/'], ['Pere i J\xc3\xbalia', '/tv3/alacarta/pere-i-julia/'], ['Pop R\xc3\xa0pid', '/tv3/alacarta/pop-rapid/'], ['Riviera', '/tv3/alacarta/riviera/'], ['Sitges', '/tv3/alacarta/sitges/'], ["Unitat d'investigaci\xc3\xb3", '/tv3/alacarta/unitat-investigacio/'], ['Vent del pla', '/tv3/alacarta/ventdelpla/'], ['Xooof', '/tv3/alacarta/xooof/']]
	    seriefinal = False
	    for i in xrange(len(seriestv3)):
	        serieactual = seriestv3[i][0].lower()
	        serieactual = serieactual.decode('utf-8') #ho passa de ASCII A utf-8 perque no doni error.
	        serieactual = unicodedata.normalize('NFKD', serieactual).encode('ASCII', 'ignore') # li treu els accents i ho guarda com a ASCII
	        if serie in serieactual:
	            seriefinal = serieactual
	            break
	    return seriefinal

	def serie(self):
		missatgesplit = self.missatge.split()
		try:
			serie = missatgesplit[1:]
			serie = ' '.join(serie)
			if serie == "marley":
				serie = "merli"
			if len(serie) <= 3:
				self.contestar("Ha habido un error con la serie, porfavor, prueba otra vez.")
				return False
		except:
			self.contestar("Ha habido un error con la serie, porfaor, prueba otra vez.")
			return False
		if self.checkSerieTV3(serie) != False:
			checkCapitulx = self.checkCapitul(serie, True)	
		else:
			if self.checkSerie(serie) == True:
				checkCapitulx = self.checkCapitul(serie, False)

	def checkSerie(self, serie):
		if serie == "los simpsons": 
			serie = "los simpson"
		url = 'http://www.seriesflv.net/api/search'
		values = {'q' : serie}
		headers = { 'User-Agent' : "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36" }
		r = requests.get(url, params = values, headers= headers).text
		soup = BeautifulSoup("".join(r))
		urlfinallist = soup.findAll('a', href=re.compile('/serie/'))
		try:
			urlfinallist = str(urlfinallist[0]).split('href="')[1]
			return True
		except:
			subprocess.Popen(["python","/home/pi/AleixDomo/Series/obtenirtorrent.py", serie])
			file = open("/home/pi/AleixDomo/txt/escoltar.txt", "w")
			file.write("1")
			file.close()
			return False

	def pararMusica(self):
		if self.spoticanso:
			self.spoticanso.stop()
		os.system("sudo pkill -f mostrarimatges.py")
		os.system("kill `pgrep omxplayer`")
		os.system('sudo sh -c "TERM=linux setterm -foreground black -clear >/dev/tty0"')
		if self.entrada == 2 or self.entrada == 3:
			self.contestar('Parando...')

	def siguienteMusica(self):
		if self.spoticanso:
			self.spoticanso.siguiente()

	def pausaMusica(self):
		if self.spoticanso:
			self.spoticanso.pause()

	def reanudarMusica(self):
		if self.spoticanso:
			self.spoticanso.resume()

	def agregarLlistaMusica(self):
		if len(self.missatge.split('lista')[1]) > 0:
			nomllista = self.missatge.split('lista ')[1]
			if "de" in nomllista.split():
				nomllista = re.sub(r'\bde\b','', nomllista)
		else:
			nomllista = False
		if self.spoticanso:
			if self.spoticanso.llistaAgregar(nomllista):
				self.contestar('Agregado correctamente')
			else:
				self.contestar('Ha habido un error con su lista')

	def updateStatus(self, playing):
		if playing == True or playing == False:
			self.veu.playing = playing
		self.updateLog(playing)

	def domoControl(self):
		if self.ipprocc == False:
			try:
				self.ipprocc = self.db['Config'].find_one()['ip']
			except:
				pass
		if self.ipprocc == False:
			self.contestar('No puedo encontrar la otra Raspberry, compruebe las conexiones.')
		else:
			numerorele = False
			if self.domoconfig == False:
				self.domoconfig = self.db['ConfigDomo'].find_one()
			if 'temperatura' in self.missatge or 'temperatura' in self.ultimissatge:
				for i in self.domoconfig:
					if 'caldera' in i or 'termostato' in i or 'calentador' in i:
						numerorele = self.domoconfig[i]
						break
				if numerorele != False:
					numero = False
					numero = int(re.search(r'\d+', self.missatge).group())
					if numero != False:
						if numero < 15:
							client = pymongo.MongoClient(self.ipprocc, 27017)
							db = client['ProjectDB']
							dblog = db['HLog']
							temperatura = dblog.find({"type": 'temperature'}).sort("_id", -1).limit(1)[0]['data']['temperature']
							if 'sube' in self.missatge:
								numero = int(temperatura) + numero
							elif 'baja' in self.missatge:
								numero = int(temperatura) - numero
						self.temperaturaSet(numerorele, numero)
					else:
						self.contestar('No se ha especificado una temperatura')
			else:
				if "enciende" in self.missatge:
					status = "1"	
					missatge = 'Encendiendo '
				elif "apaga" in self.missatge:
					status = "0"
					missatge = 'Apagando '
				elif self.missatge == "apaga todo":
					status = "2"
					missatge = 'Apagando todos los aparatos.'
				for i in self.domoconfig:
					for x in self.missatge.split():
						if i == x:
							objecte = i
							numerorele = self.domoconfig[i]	
				if numerorele != False:
					self.encendreRele(numerorele, status)
					self.contestar(missatge + objecte)
				
	def encendreRele(self, numerorele, status):
		data = {"numerorele": numerorele, "status": status}
		resp = requests.get('http://' + self.ipprocc + '/control.php', params=data).text
		if resp != 'Ok':
			self.contestar('Ha habido un error.')

	def temperaturaSet(self, numerorele, temp):
		try:
			client = pymongo.MongoClient(self.ipprocc, 27017)
			db = client['ProjectDB']
			db['DomoConfig'].update_one({"id": None },{"$set": {"reletemp": numerorele}})
			db['DomoConfig'].update_one({"id": None },{"$set": {"temperatura": temp}})
			self.contestar('De acuerdo.')
			self.contestar('Temperatura actual: ' + str(temp) + ' Grados.') 
		except:
			self.contestar('Ha habido un error.')

	def updateLog(self, playing):
		p = {}
		p['playing'] = playing
		p['timestamp'] = datetime.datetime.now()
		p['missatge'] = self.missatge
		try:
			p['accio'] = self.accio
		except:
			pass
		try:
			p['ultimissatge'] = self.ultimissatge
		except:
			pass
		self.db['Status'].insert(p)

	def processarfuncions(self):
		i = self.accioid
		if i == 0:
			self.conversa()
		elif i == 1:
			self.multimedia()
			self.updateStatus(False)
		elif i == 2:
			self.missatge = self.missatge.replace("?", "")
			if "en" in self.missatge.split():
				lloc = self.missatge.split()[-1]
				self.contestar(geolocation.TempsUbicacio(lloc, self.missatge))
			else:
				requested = self.missatge.split()[-1]
				self.contestar(geolocation.AconseguirTemps(requested))
		elif i == 3:
			self.pararMusica()
			self.updateStatus(False)
		elif i == 4:
			self.siguienteMusica()
		elif i == 5:
			self.missatge = self.missatge.replace("?", "")
			self.contestar(recordatoris.ComprobarDia(self.missatge))
		elif i == 6:
			if recordatoris.AfegirRecordatori(self.missatge) == True:
				self.contestar("De acuerdo, me lo apunto.")
			else:
				self.contestar("No has configurado aun las tareas, para mas informacion, diga, o, escriba: ayuda tareas" )
		elif i == 7:
			self.domoControl()
		elif i == 8:
			usuari = self.missatgesplit[1]
			contrassenya = self.missatgesplit[2]
			if recordatoris.RegistrarUsuari(usuari,contrassenya) == True:
				resposta = "Usuario registrado correctamente, ya puede usar las tareas, pruebe con recuerdame, y lo que quiera que le recuerde."
				self.contestar(resposta)
			else:
				resposta = "No se ha podido autenticar, compruebe su contraseña y usuario"
				self.contestar(resposta)
		elif i == 9:
			if self.ipprocc == False:
				try:
					self.ipprocc = self.db['Config'].find_one()['ip']
				except:
					pass
			self.contestar(TemperaturaActual(self.ipprocc))
		elif i == 10:
			self.contestar(self.chisteAleatorio())
		elif i == 11:
			missatge = self.missatge.split('video')[1]
			subprocess.Popen(["python", "/home/pi/AleixDomo/Videos/youtube.py",missatge])
		elif i == 12:
			contrassenya = open('/home/pi/AleixDomo/txt/contrassenya.txt', 'r').read()
			contrassenya = "... ".join(list(contrassenya))
			self.contestarVeu("Mi contraseña es... " + contrassenya)
			self.contestarVeu(contrassenya)
		elif i == 13:
			self.updateStatus(True)
			self.reanudarMusica()
		elif i == 14:
			self.updateStatus(False)
			self.pausaMusica()
		elif i == 15:				 
			self.agregarLlistaMusica()
		elif i == 16:
			if "en que ano fue uno mas uno" in self.missatge or "en que ano fue 1 + 1" in self.missatge:
				resposta = "La respuesta es: el fantastico Ralph!"
			else:
				if "define" in self.missatge:
					self.missatge = self.missatge.split("define")[1]
				resposta = aconseguirResposta(self.missatge)
			self.contestar(resposta)
		elif i == 17:
			self.setupDomo()
		elif i == 18:
			resposta = "Registrese en https://todoist.com/Users/showRegister"
			resposta1 = "Y luego, envie su usuario i contraseña del siguiente modo, Tareas X Y Donde X es su usuario y Y su contraseña"
			if self.entrada == 2 or self.entrada == 3:
				self.contestar(resposta)
				self.contestar(resposta1)
			else:
				self.contestar("Para usar el modulo de tareas, debe crearse una cuenta en todoist, una vez creada debe enviarla por Whatsapp o Telegram, para mas informacion, escriba ayuda tareas en el movil.")
		elif i == 19:
			self.serie()

			
	def processarparaula(self):
		try:
			print self.ultimissatge
		except:
			pass
		if "tareas" not in self.missatge.lower():
			self.missatge = self.missatge.lower()
		ielegida = False
		try:
			self.missatge = self.missatge.decode('utf8')
			self.missatge = unicodedata.normalize('NFKD', self.missatge).encode('ASCII', 'ignore') # li treu els accents i ho guarda com a ASCII
		except:
			pass	
		self.missatgesplit = self.missatge.split()
		self.funcions.rewind()
		for i in self.funcions:
			try:
				if not ielegida:
					for x in i['paraules']:
						if x[1] >= 0:
							if i['in']:
								if x[0] in self.missatgesplit[x[1]]:
									ielegida = i
									break
							else:
								if x[0] == self.missatgesplit[x[1]]:
									ielegida = i
									break
						else:
							if i['in']:
								if x[0] in self.missatge:
									ielegida = i
									break
							else:
								if x[0] == self.missatge:
									ielegida = i
									break
				else:
					break
			except:
				pass
		if ielegida:
			self.accio = ielegida['nom']
			self.accioid = ielegida['id']
			self.processarfuncions()
		else:
			if "temporada" in self.missatgesplit[0]:
				processador1.temporada(self.missatge)
			elif "capitulo" in self.missatgesplit[0]:
				processador1.capitulo(self.missatge)
			else:
				if self.entrada == 2 or self.entrada == 3:
					self.contestar("Comando erronio, si necesita ayuda, escriba: Ayuda.")
				elif self.entrada == 1:
					self.contestarVeu(self.missatge + " " + "no existe, pruebe otra vez")
		
		self.ultimissatge = self.missatge