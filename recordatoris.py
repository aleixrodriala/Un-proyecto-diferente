# coding=utf-8
import todoist

dias = ["lunes","martes","miercoles","jueves","viernes","sabado","domingo","hoy","manana"]

def RegistrarUsuari(usuari, contrassenya):
	try:
		api = todoist.TodoistAPI()
		token = api.login(usuari, contrassenya)['api_token']
		inboxid = api.sync(resource_types=['projects'])['Projects']
		for i in inboxid:
			if "Inbox" in i['name']:
				inboxid = i['id']
		f = open("/home/pi/AleixDomo/txt/todoistapi.txt", "w")
		f.write(str(token) + "-" + str(inboxid))
		f.close()
		return True
	except:
		return False

def LlegirToken():
    file = open('/home/pi/AleixDomo/txt/todoistapi.txt', 'r')
    return file.read()
    file.close()

def AfegirRecordatori(missatge):
	try:
		tokenbrut = LlegirToken()
		token = tokenbrut.split("-")[0]
		inboxid = tokenbrut.split("-")[1]
		api = todoist.TodoistAPI(token)
	except:
		return False
	try:
		frase = []
		missatge = missatge.split()
		for i in xrange(len(missatge)):
			for x in xrange(len(dias)):
				if dias[x] in missatge[i]:
					dia = missatge[i]
					if dia == "manana":
						dia = "mañana"
			if "tengo" in missatge[i]:
				missatgex = missatge[i:]
				for z in xrange(len(missatgex)):
					for xz in dias:
						if xz in missatgex[z]:
							frase = missatge[i:i+z]
			elif ":" in missatge[i]:
				hola = missatge[i].replace(":","")
			else:
				hola = missatge[i]
			try:
				int(hola)
				hora = missatge[i]
			except:
				pass
		if len(frase[-1]) <= 2:
			del frase[-1]
		if "tengo" in frase:
			frase.remove("tengo")
		if "para" in frase:
			frase.remove("para")
		if frase[0] == "que":
			del frase[0]
		que = ' '.join(frase).capitalize()
		item = api.items.add(que, inboxid)
		item.update(date_lang="es")
		try:
			item.update(date_string=dia + " a " + str(hora) + " pm")
		except:
			item.update(date_string=dia)
		api.commit()
		return True
	except:
		return False

def ComprobarDia(missatge):
	try:
		token = LlegirToken().split("-")[0]
		api = todoist.TodoistAPI(token)
		print token
	except:
		return "No has configurado aun las tareas, para mas informacion diga o escriba: ayuda tareas"
	missatge = missatge.split()
	for i in missatge:
		for x in dias:
			if x in i:
				diacastella = i
	try:
		if diacastella == "manana":
			diacastella = u'mañana'
		frase = "Para " + diacastella + " tienes: "
		fraseinicial = frase
		tareas = api.query([diacastella])[0]
	except:
		return "No has configurado aun las tareas, para mas informacion diga o escriba: ayuda tareas"
	try:	
		for i in tareas['data']:
			hora = ""
			tasca = i['content']
			print i['date_string']
			try:
				x = str([int(s) for s in i['date_string'].split() if s.isdigit()][0])
				if "1" in x:
					hora = " a la " + str(x)
				else:
					hora = " a las " + str(x)			
			except:
				pass
			frase = frase + " " + tasca + hora + "," 
		if fraseinicial != frase:
			return frase
		else:
			return "No tiene nada que hacer " + diacastella
	except:
		return "No tiene nada que hacer " + diacastella