# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
import threading
import time
import spotify
import urllib
import pymongo
import datetime
import subprocess
import requests
import os
from difflib import SequenceMatcher

def ratio (nom1, nom2):
	nom1 = nom1.lower()
	nom2 = nom2.lower()
	return SequenceMatcher(None, nom1, nom2).ratio()

class Spotipy:
	def __init__(self):
		self.playing = False
		self.logged_in = threading.Event()
		self.session = None
		self.trackend = False
		self.container = False
		self.lasttrack = False
		self.end_of_track = threading.Event()
		self.startspoticlient()

	def on_end_of_track(self, session):
		self.trackend = True
		self.session.player.play(False)

	def on_connection_state_changed(self, session):
		if session.connection.state is spotify.ConnectionState.LOGGED_IN:
			self.logged_in.set()
		elif session.connection.state is spotify.ConnectionState.LOGGED_OUT:
			self.logged_in.clear()

	def startspoticlient(self):
		self.session = spotify.Session()
		self.session.on(spotify.SessionEvent.CONNECTION_STATE_UPDATED, self.on_connection_state_changed)
		self.session.on(spotify.SessionEvent.END_OF_TRACK, self.on_end_of_track)
		audio_driver = spotify.AlsaSink(self.session)
		event_loop = spotify.EventLoop(self.session)
		event_loop.start()
		self.session.login('user', 'password', remember_me=True)
		self.logged_in.wait()

	def getTrack(self, track_uri):
		track = self.session.get_track(track_uri).load()
		self.reproduir(track)

	def reproduir(self, track):
		self.lasttrack = track
		self.session.player.load(self.lasttrack)
		self.session.player.play()

	def playPlaylist(self,nomplaylist):
		if not self.container:
			self.container = self.session.playlist_container
			self.container.load()
		playlistfinal = False
		for i in self.container:
			playlist = i.load()
			nom = playlist.name
			if nomplaylist.lower() in nom.lower():
				playlistfinal = playlist
		if playlistfinal != False:
			tracks = playlistfinal.tracks
			self.parar = False
			for i in xrange(len(tracks)):
				track = tracks[i].load()
				if not self.parar:
					self.reproduir(track)
					album = track.album.load()
					nomalbum = album.name.encode('utf8')
					cover = album.cover(spotify.ImageSize.LARGE).load()
					canso = track.name
					nomartista = track.artists[0].load().name.encode('utf8')
					nomfitxer = "/home/pi/AleixDomo/Musica/Caratula/"
					extensio = ".jpg"
					nomfitxer = nomfitxer + canso.replace(" ","-").replace('/','-').lower() + extensio
					open(nomfitxer, 'w+').write(cover.data)
					myfile = open("/home/pi/AleixDomo/txt/pasarcanso.txt", "w")
					myfile.write(canso.encode('utf8'))
					myfile.write("+")
					myfile.write(nomfitxer.encode('utf8'))
					myfile.write("+")
					myfile.write(nomartista)
					myfile.close()
					self.trackend = False
					if i == 0:
						open('/home/pi/AleixDomo/txt/cansons.txt', 'w').close()
						myfile = open("/home/pi/AleixDomo/txt/cansons.txt", "a")
						for i in tracks:
							myfile.write(i.load().name.encode('utf8'))
							myfile.write('\n')
						myfile.close()
						subprocess.Popen(["sudo", "python", "/home/pi/AleixDomo/Musica/Caratula/caratula.py", canso, nomartista, nomfitxer])
					while not self.trackend:
						time.sleep(1)
			myfile = open("/home/pi/AleixDomo/txt/pasarcanso.txt", "w")
			myfile.write("ABOOOOOOOOOOOO")
			myfile.close
			return True
		else:
			return False
		
	def llistaAgregar(self, nomplaylist):
		playlistfinal = False
		if not self.container:
			self.container = self.session.playlist_container
			self.container.load()
		for i in self.container:
			playlist = i.load()
			nom = playlist.name
			if nomplaylist.lower() == nom.lower():
				playlistfinal = playlist
		if playlistfinal == False:
			playlistfinal = self.container.add_new_playlist(nomplaylist)
		if self.lasttrack != False:
			playlistfinal.add_tracks(self.lasttrack)
			return True
		else:
			return False
				
	def play(self, missatge):
		try:
			ultimo = False
			if "lo ultimo" in missatge:
				missatge = missatge.split('lo ultimo')[1]
				ultimo = True
			url = "https://api.spotify.com/v1/search?q=" + missatge.replace(' ','+') + "&type=track,artist&limit=1"
			r = requests.get(url).json()
			try:
				artista = r['artists']['items'][0]['id']
				nomartista = r['artists']['items'][0]['name']
				if ratio(nomartista,missatge) < 0.84:
					print abookkks
				if ultimo:
					url = "https://api.spotify.com/v1/artists/" + artista + "/albums?market=ES&limit=1"
					album = requests.get(url).json()['items'][0]
					album_id = album['id']
					url = "https://api.spotify.com/v1/albums/" + str(album_id) + "/tracks"
					tracks = requests.get(url).json()['items']
				else:
					url = "https://api.spotify.com/v1/artists/" + artista + "/top-tracks?country=ES"
					tracks = requests.get(url).json()['tracks']
				self.parar = False
				for i in xrange(len(tracks)):
					if not self.parar:
						self.getTrack(tracks[i]['uri'])
						if ultimo:
							nomalbum = album['name'].encode('utf8')
							linkalbum = album['images'][0]['url']
						else:
							linkalbum = tracks[i]["album"]["images"][0]["url"]
							nomalbum = tracks[i]["album"]["name"].encode('utf8')
						canso = tracks[i]["name"]
						nomartista = tracks[i]["artists"][0]["name"].encode('utf8')
						nomfitxer = "/home/pi/AleixDomo/Musica/Caratula/" + canso.replace(" ","-").replace('/','-').lower() + ".jpg"
						urllib.urlretrieve(linkalbum, nomfitxer)
						myfile = open("/home/pi/AleixDomo/txt/pasarcanso.txt", "w")
						myfile.write(canso.encode('utf8'))
						myfile.write("+") 
						myfile.write(nomfitxer.encode('utf8'))
						myfile.write("+")
						myfile.write(nomartista)
						myfile.close()
						self.trackend = False
						if i == 0:
							open('/home/pi/AleixDomo/txt/cansons.txt', 'w').close()
							myfile = open("/home/pi/AleixDomo/txt/cansons.txt", "a")
							for i in tracks:
								myfile.write(i["name"].encode('utf8'))
								myfile.write('\n')
							myfile.close()
							subprocess.Popen(["sudo", "python", "/home/pi/AleixDomo/Musica/Caratula/caratula.py", canso, nomartista, nomfitxer])
						while not self.trackend:
							time.sleep(1)
				myfile = open("/home/pi/AleixDomo/txt/pasarcanso.txt", "w")
				myfile.write("ABOOOOOOOOOOOO")
				myfile.close
			except:
				self.trackend = False
				track = r['tracks']['items'][0]
				nomartista = track['artists'][0]['name'].encode('utf8')
				canso = track['name']
				linkalbum = track['album']['images'][0]['url']
				track_uri = track['uri']
				self.getTrack(track_uri)
				nomfitxer = "/home/pi/AleixDomo/Musica/Caratula/" + canso.replace(" ","-").replace('/','-').lower() + ".jpg"
				urllib.urlretrieve(linkalbum, nomfitxer)
				myfile = open("/home/pi/AleixDomo/txt/pasarcanso.txt", "w")
				myfile.write(canso.encode('utf8'))
				myfile.write("+") 
				myfile.write(nomfitxer.encode('utf8'))
				myfile.write("+")
				myfile.write(nomartista)
				myfile.close()
				subprocess.Popen(["sudo", "python", "/home/pi/AleixDomo/Musica/Caratula/caratulacanso.py", canso, nomartista, nomfitxer])
				while not self.trackend:
					time.sleep(1)
				myfile = open("/home/pi/AleixDomo/txt/pasarcanso.txt", "w")
				myfile.write("ABOOOOOOOOOOOO")
				myfile.close
			return True
		except:
			return False

	def pause(self):
		self.session.player.play(False) 

	def siguiente(self):
		self.session.player.play(False)
		self.session.player.unload()
		self.trackend = True

	def resume(self,):
		self.session.player.play()

	def stop(self):
		self.session.player.play(False)
		self.session.player.unload()
		self.trackend = True
		self.parar = True
