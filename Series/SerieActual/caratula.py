import sys
import urllib2
import simplejson
import urllib
import time
import os
from subprocess import check_output
import pygame
from pygame.locals import *
import pyganim
from apiclient.discovery import build
		
olanova = sys.argv[1]
count = 0

service = build("customsearch", "v1",developerKey="AIzaSyBE3mF21iLRYxHUgwtkC3YI9V8x3RjseFE")

res = service.cse().list(
    q=olanova,
    cx='014461957768202628062:ok7nfqg1pxy',
    searchType='image',
    imgSize="xlarge",
    gl='ES'
).execute()

imageUrl = res['items'][0]['link']
urllib.urlretrieve(imageUrl, "/home/pi/AleixDomo/Series/SerieActual/imatges/peliactual.jpg")

pygame.init()

size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
black = 0, 0, 0
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode(size)

ball = pygame.image.load("/home/pi/AleixDomo/Series/SerieActual/imatges/peliactual.jpg")
ball = pygame.transform.scale(ball, (2000, 1125))
ballrect = ball.get_rect()
loading = pygame.image.load("/home/pi/AleixDomo/Series/SerieActual/imatges/cargando.png")
loadingrect = loading.get_rect()

ballrect.centerx = 900
ballrect.centery = 450

loadingrect.centerx = 1200
loadingrect.centery = 300

screen.fill(black)
screen.blit(ball, ballrect)
pygame.display.flip()

pygame.display.set_caption('Pyganim Test 1')

# create the animation objects   ('filename of image',    duration_in_seconds)
boltAnim = pyganim.PygAnimation([('/home/pi/AleixDomo/Series/SerieActual/animacioloading/1.png', 0.8),
								 ('/home/pi/AleixDomo/Series/SerieActual/animacioloading/2.png', 0.8),
                                 ('/home/pi/AleixDomo/Series/SerieActual/animacioloading/3.png', 0.8),
                                 ('/home/pi/AleixDomo/Series/SerieActual/animacioloading/4.png', 0.8)])
boltAnim.play() # there is also a pause() and stop() method

mainClock = pygame.time.Clock()
while count != 10:
	screen.fill(black)
	screen.blit(ball, ballrect)
	screen.blit(loading, loadingrect)
	boltAnim.blit(screen, (1380, 260))
	pygame.display.update()
	mainClock.tick(30) 
	for event in pygame.event.get():
		if event.type == QUIT: ## defined in pygame.locals
			pygame.quit()
			sys.exit()# Feel free to experiment with any FPS setting.
	try: 
		out = check_output(["pgrep", "omxplayer"])
		out = out.rstrip('\n')
		print "Saliendo en 100"
		print count
		count = count + 1
		time.sleep(1)
	except:
		pass
pygame.quit()
sys.exit()