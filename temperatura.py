import pymongo

def TemperaturaActual(ip):
	try:
		client = pymongo.MongoClient(ip, 27017)
		db = client['ProjectDB']
		dblog = db['HLog']
		resultat = dblog.find({"type": 'temperature'}).sort("_id", -1).limit(1)[0]['data']
		return 'A ' + str(int(resultat['temperature'])) + ' grados, con un ' + str(int(resultat['humidity'])) + ' % de humedad.'
	except:
		return 'No he podido encontrar ninguna temperatura en el historial.'