import nmap    
import socket
import fcntl
import struct

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

def ObtenirIP():
	nm = nmap.PortScanner()
	nm.scan('10.0.0.1/24', '22') 
	nm.scaninfo()  

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