# -*- coding: utf-8 -*-
from subprocess import check_output
import json
import requests
import urllib
import urllib2 
import googlesearch

def Temps(geolocation):
	url = "http://api.wunderground.com/api/a318d295409d51f7/forecast10day/lang:SP/q/" + geolocation + ".json"
	r = requests.get(url).json()
	frasedia = r['forecast']['txt_forecast']['forecastday'][0]['fcttext_metric'].encode('utf8')
	frasenoche = r['forecast']['txt_forecast']['forecastday'][1]['fcttext_metric'].encode('utf8')
	return frasedia + "\n" + "🌙 " + frasenoche

def obtenirInfo(geolocation, missatge):
	
	url = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + geolocation
	r = requests.get(url).json()
	poble = r["results"][0]["address_components"][2]["long_name"].encode('utf8')
	
	if missatge == "posicio":
		tipusele = "museum|amusement_park|aquarium|art_gallery|hindu_temple|library|movie_theater|night_club|park|place_of_worship|shopping_mall|spa|stadium|zoo"
	else:
		tipusele = []
		missatge = missatge.split()
		tipus = ['restaurantes', 'museos', 'cines' , 'supermercados', 'hospitales', 'hoteles', 'farmacias', 'sitio para comer', 'sitios para comer']
		types = ['restaurant', 'museum', 'movie_theater', 'supermarket', "grocery_or_supermarket", 'hospital', 'hotel', 'pharmacy', 'food', 'food']
		for i in missatge: 
			for x in xrange(len(tipus)):
				if tipus[x] in i:
					tipusele.append(types[x])
		tipusele = "|".join(tipusele)

	url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
	data = {'key': 'AIzaSyAO6Ur6n6ouFVm-LZ1fbS3fFtTAzsliy1M','location' : geolocation,'radius' : '5000','language' : 'es','types' : tipusele}
	r = requests.get(url, params=data).json()
	frase = ""
	for i in xrange(6):
		frase = frase + "\n" + "→  " + r['results'][i+1]['name'].encode('utf8')
	temps = Temps(geolocation)
	descripcio = googlesearch.aconseguirResposta(poble)

	return "               🌐" + poble + "\n" + 'ℹ Descripción: ' + descripcio + "\n" +'🎯 Actividades Cerca: ' + frase +  "\n" + '☀ ' + temps
	 
