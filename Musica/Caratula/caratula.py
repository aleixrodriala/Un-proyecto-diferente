# -*- coding: utf-8 -*-
import pygame
import sys
import time
from pygame.locals import *

llistamejores = True

listrender = []
listrect = []

cansoactual = sys.argv[1]
nomartista = sys.argv[2]
nomfitxer = sys.argv[3]

global cansons
cansons = [line.rstrip('\n') for line in open('/home/pi/AleixDomo/txt/cansons.txt', 'r')]
cansons = cansons[1:]

def actualitzarCansons(canso, nomartista, nomfitxer):
	global cansons
	listrectactual = []
	listrenderactual = []
	for i in xrange(len(cansons)):
		if cansons[i] == cansoactual:
			cansonsactual = cansons[i + 1:]
			break
	ball = pygame.image.load(nomfitxer)
	ballrect = ball.get_rect()
	cansotext = fontcanso.render(canso.decode('utf-8'), 1, (255,255,255))
	cansotextrect = cansotext.get_rect()
	nomartistatext = fontartista.render(nomartista.decode('utf-8'), 1, (100,100,100))
	nomartistatextrect = nomartistatext.get_rect()
	ballrect.centerx = 450
	ballrect.centery = 420
	cansotextrect.centerx = 450
	cansotextrect.centery = 790
	nomartistatextrect.centerx = 450
	nomartistatextrect.centery = 860
	screen.fill(black)
	for i in xrange(len(cansonsactual)):
		listrenderactual.append(fontartista.render(cansonsactual[i].decode('utf-8'), 1, (255,255,255)))
		listrectactual.append(listrenderactual[i].get_rect())
		listrectactual[i].centerx = 1300 
		listrectactual[i].centery = 100 + i *100
		screen.blit(listrenderactual[i], listrectactual[i])
	screen.blit(cansotext, cansotextrect)
	screen.blit(nomartistatext, nomartistatextrect)
	screen.blit(ball, ballrect)
	clock.tick(1)
	pygame.display.flip()


pygame.display.init()
pygame.font.init()

size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
black = 0, 0, 0
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode(size)

ball = pygame.image.load(nomfitxer)
ballrect = ball.get_rect()

clock = pygame.time.Clock()

fontcanso = pygame.font.SysFont("robotocondensed", 60)
fontartista = pygame.font.SysFont("robotocondensed", 40)
cansotext = fontcanso.render(cansoactual.decode('utf-8'), 1, (255,255,255))
cansotextrect = cansotext.get_rect()
nomartistatext = fontartista.render(nomartista.decode('utf-8'), 1, (100,100,100))
nomartistatextrect = nomartistatext.get_rect()
nomartistatextrect.centerx = 450
nomartistatextrect.centery = 860
cansotextrect.centerx = 450
cansotextrect.centery = 790
ballrect.centerx = 450
ballrect.centery = 420
screen.fill(black)

for i in xrange(len(cansons)):
	listrender.append(fontartista.render(cansons[i].decode('utf-8'), 1, (255,255,255)))
	listrect.append(listrender[i].get_rect())
	listrect[i].centerx = 1300 
	listrect[i].centery = 100 + i *100
	screen.blit(listrender[i], listrect[i])

screen.blit(cansotext, cansotextrect)
screen.blit(nomartistatext, nomartistatextrect)
screen.blit(ball, ballrect)
clock.tick(1)
pygame.display.flip()

while True:
	try:
		pasar = [line.rstrip('\n') for line in open('/home/pi/AleixDomo/txt/pasarcanso.txt', 'r')][0].split("+")
		cansofitxer = pasar[0]
		nomfitxerfitxer = pasar[1]
		nomartistax = pasar[2]
		if cansoactual != cansofitxer:
			cansoactual = cansofitxer
			actualitzarCansons(cansofitxer, nomartistax, nomfitxerfitxer)
		for event in pygame.event.get():
			if event.type == QUIT: ## defined in pygame.locals
				pygame.quit()
				sys.exit()
		time.sleep(1)
	except:
		pygame.quit()
		sys.exit()