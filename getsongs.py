
#Algo:
# take the name of the song from user as an argument
# look for that name on youtube using query string - https://www.youtube.com/results?search_query=<url-encoded name of song>
# pick the url of the first youtube search result from this query link
# convert this video to mp3 using query string - http://www.youtubeinmp3.com/download/?video=<url-encoded youtube url>
# pick the url from the only hyperlink on the resulting page

import requests
from bs4 import BeautifulSoup
import re
import sys
#import urllib
from urllib import pathname2url
import time
import os
#gi.require_version('Notify', '0.7')
#from gi.repository import Notify

def getsong(name, remaining):
	filename = '/home/dipanshu/Downloads/' + name + ".mp3"
	url = r'https://www.youtube.com/results?search_query=' + pathname2url(name + 'song official music')
	r = requests.get(url)
	r_html = r.text
	
	soup = BeautifulSoup(r_html, 'html.parser')
	
	line = soup.find('', class_='yt-lockup-title')
	m = re.search(r'href=".*"', str(line))
	if m:
		item = r"http://www.youtubeinmp3.com/download/?video=" + pathname2url(r"https://youtube.com" + m.group(0)[:].split('\"')[1])
		r = requests.get(item)
		m = re.search(r'/download/get/\?i=.*"><i', str(r.text.encode('utf-8')))
		if m:
			item = m.group(0)[:-4]
			r = requests.get(r"http://youtubeinmp3.com" + item)
			with open(filename, "wb") as code:
				code.write(r.content)
			if os.path.getsize(filename) < 1048576:
				sys.argv.append(name)
				print("Re-queued to wait for processing")
				if remaining == 0:
					time.sleep(20)
	

if __name__ == "__main__":
	print("\n\nAutomatic Song Downloader\n")
#	Notify.init("Song Downloader")
	songsList = []
	if sys.argv[1] == '-f':
		i=0
		with open(sys.argv[2]) as listFile:
			for song in listFile:
				songsList.append(song)
		while i < len(songsList):
			print(str(i+1)+": Downloading '"+songsList[i].replace('\n','')+"\'")
			getsong(songsList[i], len(songsList)-i)
			i=i+1
	else:
		i=1
		while i < len(sys.argv):
			print(str(i)+": Downloading '"+sys.argv[i]+"\'")
			getsong(sys.argv[i], len(sys.argv)-i)
			i=i+1
#	Notify.Notification.new("MP3 Downloads finished.").show()
