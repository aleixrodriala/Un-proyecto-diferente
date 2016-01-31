# -*- coding: utf-8 -*-
import threading
import telegram
import unicodedata
import urllib
import re
import subprocess
import infopoble

class ControladorTelegram(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		self.status = None
		self.missatgeready = threading.Event()


	def contestarTelegram(self, missatge):
		self.bot.sendMessage(chat_id=self.chat_id,text=missatge)
		
	def run(self):
		self.bot = telegram.Bot(token='132678505:AAEKAQDPlB4P7D10jbWwY_UbRccmzAejTmw')

		LAST_UPDATE_ID = None

		contractivada = False

		Cola = open('/home/pi/AleixDomo/txt/colatelegram.txt', 'r').read()
		AntigaCola = Cola

		Llistachatid = [int(line.rstrip('\n')) for line in open('/home/pi/AleixDomo/txt/llistachatidtelegram.txt', 'r')]

		contrassenya = open('/home/pi/AleixDomo/txt/contrassenya.txt', 'r').read()

		while True:
			for update in self.bot.getUpdates(offset=LAST_UPDATE_ID, timeout=10):
				self.chat_id = update.message.chat_id
				if update.message.photo:
					if self.chat_id in Llistachatid:
						photo = update.message.photo[-1].file_id	
						url = self.bot.getFile(photo)['file_path']
						nom = url.split("/")[-1]
						urllib.urlretrieve(url, "/home/pi/AleixDomo/Fotos/fitxers/" + nom)
						fentActualmentModificar("fotos")
						try:
							if process:
								if process.poll() == 0:
									process = subprocess.Popen(["sudo", "python","/home/pi/AleixDomo/Fotos/mostrarimatges.py"])
							else:
								process = subprocess.Popen(["sudo", "python","/home/pi/AleixDomo/Fotos/mostrarimatges.py"])
						except:
							process = subprocess.Popen(["sudo", "python","/home/pi/AleixDomo/Fotos/mostrarimatges.py"])
					else:
						self.bot.sendMessage(chat_id=self.chat_id,text="Porfavor introduce la contraseña.")
					LAST_UPDATE_ID = update.update_id + 1
				if update.message.location:
					if self.chat_id in Llistachatid:
						latitude = update.message.location['latitude']
						longitude = update.message.location['longitude']
						try:
							self.bot.sendMessage(chat_id=self.chat_id,text=infopoble.obtenirInfo(str(latitude) + "," + str(longitude), "posicio"))
						except:
							self.bot.sendMessage(chat_id=self.chat_id,text="Ha habido un error.")
					else:
						self.bot.sendMessage(chat_id=self.chat_id,text="Porfavor introduce la contraseña.")
					LAST_UPDATE_ID = update.update_id + 1
				try:
					message = update.message.text
					if (message):
						if self.chat_id in Llistachatid:
							if "tareas" not in message.lower():
								message = message.lower()
							if contractivada == True:
								f = open('/home/pi/AleixDomo/txt/contrassenya.txt', 'w')
								f.write(message)
								f.close()
								self.bot.sendMessage(chat_id=self.chat_id, text="Contraseña cambiada correctamente.")
								contractivada = False
								LAST_UPDATE_ID = update.update_id + 1
							else:
								if  message == "ayuda" or message == "/start":
									custom_keyboard = [[ "Videos (Youtube)", "Musica"],[ "Pon (Series y Peliculas)", "Lo mejor de (Top 10 Canciones de un artista)" ],[ "Tareas", "Prevision del tiempo"]]
									reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard = False)
									self.bot.sendMessage(chat_id=self.chat_id, text="Estas son las funciones principales:", reply_markup=reply_markup)
								elif message == "lo mejor de (top 10 canciones de un artista)":
									self.bot.sendMessage(chat_id=self.chat_id,text="Ejemplo: Lo Mejor De Alejandro Sanz")
								elif message == "videos (youtube)":
									self.bot.sendMessage(chat_id=self.chat_id,text="Ejemplo: Video David Bisbal Ave Maria")
								elif message == "musica":
									self.bot.sendMessage(chat_id=self.chat_id,text="Ejemplo: Musica David Bisbal Ave Maria")
								elif message == "Tareas" or message == "tareas":
									self.bot.sendMessage(chat_id=self.chat_id,text="Ejemplo: Recuerdame que tengo que comprar leche el viernes a las 7:00")
								elif message == "prevision del tiempo":
									self.bot.sendMessage(chat_id=self.chat_id,text="Ejemplos: Que tiempo hara hoy?, Que tiempo hara el viernes?")
								elif message == "pon (series y peliculas)":
									self.bot.sendMessage(chat_id=self.chat_id,text="Ejemplos: Pon Los simpsons, Pon Big Hero 6")
								elif message == u"cambiar contraseña":
									self.bot.sendMessage(chat_id=self.chat_id,text="Escribe tu nueva contraseña.")
									contractivada = True
								else:
									self.missatge = message
									self.missatgeready.set()
									self.missatgeready.clear()
								LAST_UPDATE_ID = update.update_id + 1
						else: 
							contrassenya = open('/home/pi/AleixDomo/txt/contrassenya.txt', 'r').read()
							if message.lower() == contrassenya:
								f = open('/home/pi/AleixDomo/txt/llistachatidtelegram.txt', 'a')
								f.write(str(self.chat_id) + "\n")
								f.close()
								self.bot.sendMessage(chat_id=self.chat_id,text="Usuario agregado correctamente, si quiere cambiar la contraseña para futuros usuarios escriba: Cambiar Contraseña.")
								Llistachatid = [int(line.rstrip('\n')) for line in open('/home/pi/AleixDomo/txt/llistachatidtelegram.txt', 'r')]
							else:
								self.bot.sendMessage(chat_id=self.chat_id,text="Porfavor introduce la contraseña.")
							LAST_UPDATE_ID = update.update_id + 1
				except:
					LAST_UPDATE_ID = update.update_id + 1