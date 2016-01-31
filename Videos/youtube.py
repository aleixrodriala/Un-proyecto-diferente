# -*- coding: utf-8 -*-
import requests
import sys
from apiclient.discovery import build
from subprocess import check_output
import subprocess

DEVELOPER_KEY = "AIzaSyBE3mF21iLRYxHUgwtkC3YI9V8x3RjseFE"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
missatge = sys.argv[1]

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
developerKey=DEVELOPER_KEY)

r = youtube.search().list(q=missatge,part="id,snippet",maxResults=1,type="video").execute()

idvideo = r["items"][0]["id"]["videoId"]
nomvideo = r["items"][0]["snippet"]["title"]

subprocess.Popen(["python","/home/pi/AleixDomo/Videos/pyvonabackground.py","Poniendo... " + nomvideo])
	
urlfinal = "http://www.youtube.com/watch?v=" + idvideo
out = check_output(["youtube-dl", "-g", urlfinal]) 
out = out.rstrip('\n')
process = subprocess.Popen(["omxplayer",out])
process.wait()