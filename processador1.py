# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import urllib
import urllib2
from subprocess import check_output
from bs4 import BeautifulSoup
import re
import pyvona
import time
import unicodedata

	
global funciona
funciona = False

#def Setup(missatge):
#	contestarVeu("Que quieres usar para controlar")

def llegirSerie():
	file = open('/home/pi/AleixDomo/txt/seriemobils.txt', 'r')
	return file.read()
	file.close()

def escriureFitxer(missatge):
    file = open("/home/pi/AleixDomo/txt/escoltar.txt", "w")
    file.write(missatge)
    file.close()

def fentActualmentModificar(missatge):
	file = open("/home/pi/AleixDomo/txt/fentActualment.txt", "w")
	file.write(missatge)
	file.close()

def fentActualmentLlegir():
	file = open('/home/pi/AleixDomo/txt/fentActualment.txt', 'r')
	return file.read()
	file.close()

def seriePrimerCop(serie, temporada, capitul):
	if temporada == "TV3":
		subprocess.Popen(["python","/home/pi/AleixDomo/Series/tv3.py", serie, capitul])
	else:
		subprocess.Popen(["python","/home/pi/AleixDomo/Series/obtenirseriesflv.py", serie, temporada, capitul])
	escriureFitxer("1")
            	
def contestar(missatge, entrada, self):
	contestarVeu(missatge)

def contestarVeu(missatge):
	global funciona
	while funciona == False:
		try:
			v = pyvona.create_voice("GDNAIOIEYJ4TLER6BWMQ", "0keM4rjAabbuEsVXMM9+/C+Ewn8af/ZokV5/BzwI")
			v.speak(missatge)
			time.sleep(0.5)
			funciona = True
		except: 
			time.sleep(1)
	funciona = False

def capitul(missatge):
	capitul = missatge.split("capitulo ")[1]
	if "." in capitul:
		capitul = capitul.replace(".", "")
	serie = llegirSerie()
	seriePrimerCop(serie, "TV3", capitul)

def temporada(missatge):
	temporadabrut = missatge.split("temporada ")[1]
	temporada = temporadabrut.split(" capitulo ")[0]
	capitul = temporadabrut.split(" capitulo ")[1]
	serie = llegirSerie()
	seriePrimerCop(serie, temporada , capitul)