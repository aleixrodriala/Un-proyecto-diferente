import nmap    
import socket
import fcntl
import struct
import pymongo
import time

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

def GetIP():
	nm = nmap.PortScanner()
	nm.scan('192.168.1.1/24', '22') 
	nm.scaninfo()  
	hostelegido = False
	for host in nm.all_hosts():
		for proto in nm[host].all_protocols():
			print ("")
		lport = nm[host][proto].keys()
		lport.sort()
		for port in lport:
			if (nm[host][proto][port]['state']) == "open":
				if host != get_ip_address('wlan0'):
					hostelegido = host
	return hostelegido

hostelegido = False
count = 0

while hostelegido == False:
	if count > 10:
		break
	try:
		hostelegido = GetIP()
		if hostelegido != False:
			client = pymongo.MongoClient("localhost", 27017)
			db = client['ProjectDB']
			dbpelis	= db['Config']
			dbpelis.update({'idioma': None}, {'ip': hostelegido}, upsert=True)
	except:
		pass
	time.sleep(100)
	count = count + 1