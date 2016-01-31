import sys
import pyvona

missatge = sys.argv[1]

def escriureFitxer(missatge):
    file = open("/home/pi/AleixDomo/txt/escoltar.txt", "w")
    file.write(missatge)
    file.close()

escriureFitxer("4")
v = pyvona.create_voice("GDNAIOIEYJ4TLER6BWMQ", "0keM4rjAabbuEsVXMM9+/C+Ewn8af/ZokV5/BzwI")
v.speak(missatge)
escriureFitxer("1")