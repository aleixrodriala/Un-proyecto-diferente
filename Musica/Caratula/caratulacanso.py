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
nomartistatextrect.centerx = 800
nomartistatextrect.centery = 860
cansotextrect.centerx = 800
cansotextrect.centery = 790
ballrect.centerx = 800
ballrect.centery = 420
screen.fill(black)

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
		for event in pygame.event.get():
			if event.type == QUIT: ## defined in pygame.locals
				pygame.quit()
				sys.exit()
		time.sleep(1)
	except:
		pygame.quit()
		sys.exit()