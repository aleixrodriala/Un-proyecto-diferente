import pygame
import glob
import time
import os
import sys
from pygame.locals import *

def updateImg(numero):
	screen.fill(black)
	screen.blit(listrender[numero], listrect[numero])
	clock.tick(1)
	pygame.display.flip()

def Siguiente():
	f1 = open('/home/pi/AleixDomo/txt/fentActualment.txt', 'r')
	if f1.read() == "siguiente":
		return True
	else: 
		return False
	f1.close()

def exit():
	llistafitxers = glob.glob("/home/pi/AleixDomo/Fotos/fitxers/*.jpg")
	for f in llistafitxers:
		os.remove(f)

Actiu = False
listrender = []
listrect = []
llistaborrats = []
count = 0

llistafitxers = glob.glob("/home/pi/AleixDomo/Fotos/fitxers/*.jpg")

pygame.init()

size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
black = 0, 0, 0
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

screen.fill(black)

for i in xrange(len(llistafitxers)):
	listrender.append(pygame.image.load(llistafitxers[0]))
	llistaborrats.append(llistafitxers[0])
	del llistafitxers[0]
	listrect.append(listrender[i].get_rect())
	size = (int(listrect[i].size[0] * 0.8), int(listrect[i].size[1] * 0.8))
	listrender[i] = pygame.transform.scale(listrender[i], size)
	listrect[i].centerx = 1000
	listrect[i].centery = 600

screen.blit(listrender[0], listrect[0])

clock.tick(1)
pygame.display.flip()

while True:
	llistafitxers = glob.glob("/home/pi/AleixDomo/Fotos/fitxers/*.jpg")
	for x in llistaborrats:
		llistafitxers.remove(x)
	if len(llistafitxers) > 0:
		for i in xrange(len(llistafitxers)):
			listrender.append(pygame.image.load(llistafitxers[0]))
			llistaborrats.append(llistafitxers[0])
			del llistafitxers[0]
			listrect.append(listrender[-1].get_rect())
		for i in xrange(len(listrender)):
			size = (int(listrect[i].size[0] * 0.8), int(listrect[i].size[1] * 0.8))
			listrender[i] = pygame.transform.scale(listrender[i], size)
			listrect[i].centerx = 1000
			listrect[i].centery = 600
	for event in pygame.event.get():
		if event.type == QUIT: ## defined in pygame.locals
			exit()
			pygame.quit()
			sys.exit()# Feel free to experiment with any FPS setting.
	if Siguiente() == True:
		count = count + 1
		try:
			updateImg(count)
		except:
			count = 0
			updateImg(count)
		file = open("/home/pi/AleixDomo/txt/fentActualment.txt", "w")
		file.write("fotos")
		file.close()
	time.sleep(1)
exit()
pygame.quit()
sys.exit()