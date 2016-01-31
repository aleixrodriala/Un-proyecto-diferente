# -*- coding: utf-8 -*-

from googleapiclient.discovery import build
import wikipedia

def aconseguirResposta(missatge):
	if "que sabes de" in missatge:
		missatge = missatge.split("que sabes de ")[1]
	elif "que sabes sobre" in missatge:
		missatge = missatge.split("que sabes sobre ")[1]
	try:
		service = build("customsearch", "v1",developerKey="AIzaSyBE3mF21iLRYxHUgwtkC3YI9V8x3RjseFE")
		res = service.cse().list(
			q=missatge,
			cx='014461957768202628062:ok7nfqg1pxy',
			gl='ES',
			siteSearch='wikipedia.org'
		).execute()
		query = res['items'][0]['formattedUrl'].split("/")[-1].encode('utf-8')
		if "Presidente" in query:
			query = res['items'][1]['formattedUrl'].split("/")[-1].encode('utf-8')
		wikipedia.set_lang("es")
		resposta = wikipedia.summary(query, sentences=1, chars=0, auto_suggest=False, redirect=True).encode('utf8')
		if "(" in resposta:
			resposta = resposta.split("(")
			resposta = resposta[0] + resposta[1].split(")")[1]
	except:
		resposta = "Oups, que pregunta mas rara."
	return resposta