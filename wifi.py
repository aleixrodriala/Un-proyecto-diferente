import os
from wificonfigIP import ObtenirIP
import requests 

Dades = [line.rstrip('\n') for line in open('/var/www/Dades/wifi.txt', 'r')]
SSID = Dades[0]
Password = Dades[1]

try:
	ip = ObtenirIP()
	url = "http://" + ip + '/wifi.php?ssid=' + SSID + '&pwd=' + Password
	requests.get(url)
except:
	pass
#crea arxiu contrasenya
f = open("/etc/wpa_supplicant/wpa_supplicant.conf", "w")
f.write("ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n")
f.write("update_config=1\n")
f.write("\n")
f.write("network={\n")
f.write('ssid=' + '"' + SSID + '"\n')
f.write('psk=' + '"' + Password + '"\n')
f.write("}\n")
f.close()
#primer esborrar linees
f2 = open("/etc/network/interfaces",'w')
f2.write("auto lo\n")
f2.write("iface lo inet loopback\n")
f2.write("auto wlan0\n")
f2.write("allow-hotplug wlan0\n")
f2.write("iface wlan0 inet dhcp\n")
f2.write("wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf\n")
f2.close()
#esborra linea que obra apache cada cop                                   ====================>>Falta /etc/default/hostapd 
lines = file('/home/pi/.bashrc', 'r').readlines() 
del lines[-1] 
file('/home/pi/.bashrc', 'w').writelines(lines) 
#edita hostapd
f3 = open("/etc/default/hostapd", "w")
f3.write("# Defaults for hostapd initscript\n")
f3.write("#\n")
f3.close()
#posa el que s'ha d'obrir automaticament (whats i veu)
f1 = open("/home/pi/.bashrc",'a')
f1.write("\n")
f1.write("sudo python /home/pi/AleixDomo/boto.py &\n")
f1.write("/home/pi/Whatsapp &\n")
f1.write("sudo python /home/pi/AleixDomo/wificonfigtest.py &\n")
f1.write("sudo python /home/pi/AleixDomo/contrassenya.py &\n")
f1.write("sudo python /home/pi/AleixDomo/scriptdetectar.py &\n")
f1.close()
#treure de l'inici
os.system("sudo update-rc.d hostapd remove")
os.system("sudo update-rc.d dnsmasq remove")
os.system("sudo reboot")