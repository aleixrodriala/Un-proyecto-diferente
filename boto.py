import RPi.GPIO as GPIO
import time
import requests
import os
import pymongo
import datetime

blue = 17
red = 27
green = 22

url = "http://api.timezonedb.com"
params = {'zone':'Europe/London', 'key':'OJU31JHPCCL0', 'format':'json'}
data = requests.get(url, params).json()['timestamp']

os.system("sudo date -s @" + str(data))

os.system("sudo rm /var/lib/mongodb/mongod.lock")
os.system("sudo service mongod start")

clientmongo = pymongo.MongoClient("localhost", 27017)
db = clientmongo['ProjectDB']
statusdb = db['BotoStatus']

try:
	db['Status'].drop()
except:
	pass
	
p = {}
p['playing'] = False
p['timestamp'] = datetime.datetime.now()
db['Status'].insert(p)

pinlist = [23,12,21, 5, 11, 18]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

for i in pinlist:
	GPIO.setup(i, GPIO.OUT)
	GPIO.output(i, 1)

while True:
	estat = db['Status'].find().sort("timestamp", -1).limit(1)[0]['playing']
	if estat == True:
		GPIO.output(red, 1)
		GPIO.output(green, 0)
		GPIO.output(blue, 0)
		for i in xrange(len(pinlist)):
			GPIO.output(pinlist[i], 0)
			if i > 2:
				GPIO.output(pinlist[i-3], 1)
			else:
				GPIO.output(pinlist[i+3], 1)
			time.sleep(0.1)
	elif estat == "Parlan":
		GPIO.output(red, 0)
		GPIO.output(green, 1)
		GPIO.output(blue, 0)
		for i in pinlist:
			GPIO.output(i, 0)
	elif estat == "Parlar":
		GPIO.output(red, 0)
		GPIO.output(green, 0)
		GPIO.output(blue, 1)
		for i in pinlist:
			GPIO.output(i, 0)
	elif estat == False:
		GPIO.output(red, 0)
		GPIO.output(green, 0)
		GPIO.output(blue, 0)
		for i in pinlist:
			GPIO.output(i, 1)
	if GPIO.input(16) == False:
		statusdb.update({'id': None}, {'status': True}, upsert=True)
		time.sleep(3)
	time.sleep(0.1)