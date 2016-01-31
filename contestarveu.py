import sys
import pyvona

def escriureFitxer(missatge):
    file = open("/home/pi/AleixDomo/txt/escoltar.txt", "w")
    file.write(missatge)
    file.close()


def contestarVeu(missatge):
	#escriureFitxer("4")
	v = pyvona.create_voice("GDNAIOIEYJ4TLER6BWMQ", "0keM4rjAabbuEsVXMM9+/C+Ewn8af/ZokV5/BzwI")
	v.speak(missatge)
	#escriureFitxer("1")