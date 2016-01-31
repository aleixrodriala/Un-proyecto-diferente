import os
import time
from subprocess import check_output

time.sleep(30)

try:
	out = check_output(["ping","-c", "4", "google.com"])
	lines = file('/home/pi/.bashrc', 'r').readlines() 
	del lines[-1] 
	del lines[-1] 
	del lines[-1] 
	file('/home/pi/.bashrc', 'w').writelines(lines) 
except:
	os.system("omxplayer /home/pi/AleixDomo/Beep/Badnetwork.mp3")
	#torna el .bashrc original
	lines = file('/home/pi/.bashrc', 'r').readlines() 
	lines.pop(-1)
	lines.pop(-1)
	lines.pop(-1)
	lines.pop(-1)
	lines.append("sudo service apache2 start")
	file('/home/pi/.bashrc', 'w').writelines(lines) 

	#networks/interfaces
	f = open("/etc/network/interfaces", "w")
	f.write("auto lo\n")
	f.write("iface lo inet loopback\n")
	f.write("\n")
	f.write("#auto eth0\n")
	f.write("#allow-hotplug eth0\n")
	f.write("#iface eth0 inet dhcp\n")
	f.write("\n")
	f.write("iface wlan0 inet static\n")
	f.write("address 10.0.0.1\n")
	f.write("network 10.0.0.0\n")
	f.write("netmask 255.255.255.0\n")
	f.write("broadcast 10.0.0.255\n")
	f.write("\n")
	f.close()

	#default/hostapd
	f3 = open("/etc/default/hostapd", "w")
	f3.write('DAEMON_CONF="/etc/hostapd/hostapd.conf"\n')
	f3.write("#\n")
	f3.close()


	#ultimes coses i reboot
	os.system("sudo update-rc.d hostapd defaults")
	os.system("sudo update-rc.d dnsmasq defaults")
	os.system("sudo reboot")