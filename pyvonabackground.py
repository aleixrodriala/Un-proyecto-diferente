import sys
import pyvona

missatge = sys.argv[1]

v = pyvona.create_voice("GDNAIOIEYJ4TLER6BWMQ", "0keM4rjAabbuEsVXMM9+/C+Ewn8af/ZokV5/BzwI")
v.speak(missatge)