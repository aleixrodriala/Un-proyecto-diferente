# -*- coding: utf-8 -*-
import audioop
import pyaudio
import requests
from collections import deque
from contestarveu import contestarVeu
import os
import unicodedata
import time
import re
import threading
import pymongo
import datetime

user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'
headers = { 'User-Agent' : user_agent }


class ControladorVeu(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		self.playing = False
		self.spoticanso = None
		self.clientmongo = pymongo.MongoClient("localhost", 27017)
		self.db = self.clientmongo['ProjectDB']
		self.missatgeready = threading.Event()

	def updateStatus(self,accio):
		p = {}
		p['playing'] = accio
		p['timestamp'] = datetime.datetime.now()
		self.db['Status'].insert(p)

	def getParaula(self):
		self.updateStatus('Parlar')
		if self.playing == True:
			if self.spoticanso: 
				self.spoticanso.pause()	
		os.system("/home/pi/AleixDomo/Musica/dbuscontrol.sh pause")
		os.system("mpg123 /home/pi/AleixDomo/Beep/On.mp3 > /dev/null 2>&1 ")
		audio = self.obtenirAudioRAW(True)
		os.system("mpg123 /home/pi/AleixDomo/Beep/Off.mp3 > /dev/null 2>&1 ")
		self.updateStatus(False)
		if self.playing == True:
			if self.spoticanso: 
				self.updateStatus(True)
				self.spoticanso.resume()
		os.system("/home/pi/AleixDomo/Musica/dbuscontrol.sh pause")	
		file = open('/home/pi/AleixDomo/txt/idioma.txt', 'r')
		lang = file.read()
		file.close()
		url = 'https://www.google.com/speech-api/v2/recognize?output=json&lang=' + lang + '&key=AIzaSyBE3mF21iLRYxHUgwtkC3YI9V8x3RjseFE'
		headers = {'Content-Type': 'audio/l16; rate=16000;', 'User-Agent':'Mozilla/5.0'}
		r = requests.post(url, data=audio, headers=headers).text
		try:
			final_result = r.split('[{"transcript":"')[1].split('"')[0]
			final_result = final_result.lower() # ho fa tot minuscules
			final_result = unicodedata.normalize('NFKD', final_result).encode('ASCII', 'ignore') # li treu els accents i ho guarda com a ASCII
			self.missatge = final_result
			self.missatgeready.set()
			self.missatgeready.clear()
		except:
			contestarVeu("No te he entendido, prueba otra vez.")


	def obtenirAudioRAW(self, activat):
		print "comensanaudio"
		if activat:
			maxlen = 2
			volumax = 3000
			segonsilmax = 20
		else:
			maxlen = 0.1
			volumax = 5000
			segonsilmax = 3

		chunk = 2048
		p = pyaudio.PyAudio()
		streamx = p.open(format=pyaudio.paInt16,channels=1,rate=16000,input=True,frames_per_buffer=chunk)
		audioenviar = []
		rel = 16000/1024 #relacio bitrate i chunk, per saber quans segons d'audio agafar.
		prev_audio = deque(maxlen=maxlen * rel) 
		comensat = False
		segonsilenci = 0
		segonsilencimax = 0

		while True:
			botostatus = self.db['BotoStatus'].find_one()['status']
			if botostatus:
				break
			cur_data = streamx.read(1024)
			rmsTemp = audioop.avgpp(cur_data,2)
			if rmsTemp > volumax:
				if(not comensat):
					comensat = True
				audioenviar.append(cur_data)
				segonsilenci = 0
			elif (comensat is True):
				if segonsilenci > segonsilmax:
					data = list(prev_audio) + audioenviar
					data = ''.join(data)
					break
				else:
					audioenviar.append(cur_data)
					segonsilenci = segonsilenci + 1
			else:
				segonsilencimax = segonsilencimax + 1 
				prev_audio.append(cur_data)

			if activat:
				if segonsilencimax > 120:
					data = None
					break

		streamx.close()
		p.terminate()
		if botostatus:
			self.db['BotoStatus'].update({'id': None}, {'status': False}, upsert=True)
			self.interaccio = True
			self.getParaula()			
		else:
			return data

	def checkKeyword(self):
		try:
			audio = self.obtenirAudioRAW(False)
			url = 'https://www.google.com/speech-api/v2/recognize?output=json&lang=es&key=AIzaSyBE3mF21iLRYxHUgwtkC3YI9V8x3RjseFE'
			headers = {'Content-Type': 'audio/l16; rate=16000;', 'User-Agent':'Mozilla/5.0'}
			r = requests.post(url, data=audio, headers=headers).text
			resposta = r.split('[{"transcript":"')[1].split('"')[0]
			if resposta.lower() == "iris":
				return True
			else:
				return False
		except:
			return False

	def run(self):
		os.system('sudo sh -c "TERM=linux setterm -foreground black -clear >/dev/tty0"')

		chunk = 2048
		volumeThreshold = 9500
		missatge = "Buenos Dias! soy Iris, pero también me puedes llamar Pi."
		contestarVeu(missatge)

		while True:
			os.system('sudo sh -c "TERM=linux setterm -foreground black -clear >/dev/tty0"')
			if not self.playing:
				if self.checkKeyword():
					self.getParaula()
				else:
					time.sleep(1)
			botostatus = self.db['BotoStatus'].find_one()['status']
			if botostatus:
				self.db['BotoStatus'].update({'id': None}, {'status': False}, upsert=True)
				self.getParaula()		
			time.sleep(0.5)
