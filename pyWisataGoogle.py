##############################################################################################################################################################
# Name : Pencari Rekomendasi wisata
# Data Source : Google
# Version : 0.1 (Beta)
# Codename : Arial Axe
# Note : Desain Belum selesai
# Fitur yang direncanakan di versi mendatang : 1. Bisa memberikan lokasi map dari masing-masing tempat wisata
# Creator : Altair
##############################################################################################################################################################

from bs4 import BeautifulSoup as soup
import requests, json

def getWisata(q=None):
	headers= {
			"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
		}
	Time_Out = 30
	data = requests.get('https://www.google.com/search?safe=strict&source=hp&ei=OiS3XNfvH4-UwgOXjLCADw&q='+ 'tempat wisata di' + str(q), 
						headers=headers, 
						timeout=Time_Out
			).text
	
	link = ((soup(data, 'html5lib')).find('div', {'class' : 'AbmtKb'})).find('a')['href'] #Mendapatkan link untuk destinasi wisata teratas
	data = requests.get('https://www.google.com'+str(link),
						 headers=headers,
						 timeout=Time_Out
			)
	soup_data = soup(data.text, 'html5lib')
	body = soup_data.find_all("div",class_="Qc6URd eie4Pc")
	r_wisata = {"results":[],"base_url":data.url}
	for i in body:
		sinopsis  = i.find("p", class_="sBeoSd")
		try:
			prebody = i.find("div", class_="UhR2gd")
			rate = prebody.find("span",attrs={"class":"rtng"}).text
			review = prebody.find("g-review-stars").find("span")["aria-label"]
		except AttributeError:
			rate = None
			review = None
		
		if not sinopsis is None:
			sinopsis = sinopsis.text
			r_wisata["results"].append({
				"nama":i.find("h2",class_="NbdpWc").text,
				"rating":rate,
				"review":review,
				"sinopsis":sinopsis,
				"image":i.find("img")["src"],
			})
		return json.dumps(r_wisata, indent=4)
getWisata('jakarta')
