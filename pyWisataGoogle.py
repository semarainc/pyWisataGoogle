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
import requests

def getWisata(q=None):
	""" 
		Penjelasan sedikit 
			Sebenernya ini cmn project iseng aja sehingga ini bertujuan untuk mencari tempat wisata teratas dalam google heheh 
			dalam hal ini semoga project yang gua buat ini berfaedah

		Cara Kerja
			- Cara kerjanya yaitu dengan men-trigger google search untuk mencari destinasi wisata teratas sehingga bisa memunculkan menu destinasi wisata
			  (harusnya bisa langsung ngegas ke "https://www.google.com/destination" namun ada masalah waktu request datanya karena ada bot detectornya)
			- selain itu, fungsi nya mengembalikan dictionary tujuannya biar mudah aja hehehe
			- gua gk jadiin module karena lagi mager nyetingnya :v


	"""
	nama_wisata = []
	rating_wisata = []

	r_wisata = {}
	headers= {

			"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
	}

	Time_Out = 30

	data = requests.get('https://www.google.com/search?safe=strict&source=hp&ei=OiS3XNfvH4-UwgOXjLCADw&q='+ 'tempat wisata di' + str(q), 
						headers=headers, 
						timeout=Time_Out
			).text
	
	link = ((soup(data, 'lxml')).find('div', {'class' : 'AbmtKb'})).find('a')['href'] #Mendapatkan link untuk destinasi wisata teratas

	#Reuse variabelnya biar gk makan banyak memori
	data = requests.get('https://www.google.com'+str(link),
						 headers=headers,
						 timeout=Time_Out
			).text

	soup_data = soup(data, 'lxml')

	#Sebenernya disini buat menghalau klo seandainya ada rating yang Kosong mengenai tempat wisata dari google
	for i in soup_data.findAll('div', 'fKpQpc ffysUe'):
		nama_wisata.append((i.find('h2', {'class' : 'NbdpWc'})).text)
		try:
			rating_wisata.append((i.find('span', {'class' : 'fTKmHE99XE4__star fTKmHE99XE4__star-s'}))['aria-label'])
		except Exception:
			rating_wisata.append('NULL')

	gambar = [i['src'] for i in soup_data.findAll('img', {'class' : 'bh9Cef'})]
	sinopsis = [] #SINOPSIS --> ['SHORT', 'LONG']

	for i in range(len(soup_data.findAll('p', {'class' : 'sBeoSd'}))):
		sinopsis.append([
			soup_data.findAll('p', {'class' : 'buUMge'})[i].text,
			soup_data.findAll('p', {'class' : 'sBeoSd'})[i].text
			])


	for i in range(len(nama_wisata)-1): #mumpung semuanya memiliki banyak yg sama hehehe
		r_wisata[i] = {
			"nama" : str(nama_wisata[i]),
			"rating" : str(rating_wisata[i]),
			"gambar" : str(gambar[i]),
			"sinopsis" : sinopsis[i],
			"link" : "https://www.google.com"+str(link)
		}

	#NOTE : Meskipun bisa menggunakan variabel _ namun saya rasa menggunakan variabel i lebih mudah dipahami hehehe :v
	return r_wisata

print(getWisata('jakarta')) # Memberikan 50 Hasil Pencarian
