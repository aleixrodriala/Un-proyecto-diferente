# -*- coding: utf-8 -*-
from subprocess import check_output
import json
import requests
import urllib
import urllib2 

def Temps(geolocation, requested):
    url = "http://api.wunderground.com/api/a318d295409d51f7/forecast10day/lang:SP/q/" + geolocation + ".json"
    r = requests.get(url).json()
    if requested == "miercoles":
        requested = u"miércoles"
    elif requested == "sabado":
        requested = u"sábado"
    if requested == "manana" or requested == u"mañana":
        frasedia = r['forecast']['txt_forecast']['forecastday'][2]['fcttext_metric']
        frasenoche = r['forecast']['txt_forecast']['forecastday'][3]['fcttext_metric']
    elif requested == "hoy" or requested == "tarde":
        frasedia = r['forecast']['txt_forecast']['forecastday'][0]['fcttext_metric']
        frasenoche = r['forecast']['txt_forecast']['forecastday'][1]['fcttext_metric']
    elif requested == "noche":
        frasedia = ""
        frasenoche = r['forecast']['txt_forecast']['forecastday'][1]['fcttext_metric']
    else:
        for i in xrange(14):
            ractual = r['forecast']['txt_forecast']['forecastday'][i]
            if requested == ractual['title'].lower():
                frasedia = ractual['fcttext_metric']
            try:
                if requested == ractual['title'].lower().split('noche del ')[1]:
                    frasenoche = ractual['fcttext_metric']
            except:
                pass

    return frasedia.replace("C.", "grados.").replace("probab.", "probabilidades") + " y por la noche: " + frasenoche

def check():
    try:
        geolocation = open('/home/pi/AleixDomo/txt/ubicacio.txt', 'r').read()
        if len(geolocation) > 3:
            return geolocation
        else:
            return False
    except:
        return False
    
def TempsUbicacio(lloc, missatge):
    try:
        dies = ['hoy', 'manana', 'lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']
        url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + lloc + "&key=AIzaSyBE3mF21iLRYxHUgwtkC3YI9V8x3RjseFE"
        coordenades = requests.get(url).json()['results'][0]['geometry']['location']
        latitude = coordenades['lat']
        longitude = coordenades['lng']
    except:
        return('No se ha podido enontrar tu ubicacion')

    dia = False
    for x in missatge.split():
        for i in dies:
            if x == i:
                dia = x
    if dia != False:
        return Temps(str(latitude) + "," + str(longitude), dia)
    else:
        return Temps(str(latitude) + "," + str(longitude), 'hoy')
        

def AconseguirTemps(requested):
    if check() != False:
        return Temps(check(), requested)
    else:
        out = check_output(["sudo", "iwlist", "wlan0", "scan"])
        out = out.split('\n')

        data = {}
        data['wifiAccessPoints'] = []

        Count = 0

        for i in out:
            if "Cell" in i:
                macaddress = i.split("Address: ")[1]
                data["wifiAccessPoints"].append({})
                data['wifiAccessPoints'][Count]['macAddress'] = macaddress
                data['wifiAccessPoints'][Count]['age'] = 0
            if "Frequency" in i:
                channel = i.split("(Channel ")[1].split(")")[0]
                data['wifiAccessPoints'][Count]['channel'] = channel
                Count = Count + 1

        url = "https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyBE3mF21iLRYxHUgwtkC3YI9V8x3RjseFE"
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(data), headers=headers).json()
        try:
            latitude = r['location']["lat"]
            longitude = r['location']["lng"]
            file = open("/home/pi/AleixDomo/txt/ubicacio.txt", "w")
            file.write(str(latitude) + "," + str(longitude))
            file.close()
   
        except:
            return "No se ha podido encontrar su ubicacion, porfavor diga donde se encuentra ahora mismo."

        return Temps(str(latitude) + "," + str(longitude), requested)
