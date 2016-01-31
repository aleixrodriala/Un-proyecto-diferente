import random
import string

randompassword = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))

randompassword = randompassword.replace("y","x").replace("i","x").replace("d","t")

f = open("/home/pi/AleixDomo/txt/contrassenya.txt", "w")
f.write(randompassword)
f.close()