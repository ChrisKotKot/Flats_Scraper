from bs4 import BeautifulSoup
from requests import get
import sqlite3
from sys import argv

URL = 'https://www.olx.pl/d/nieruchomosci/mieszkania/sprzedaz/podlaskie/'

def parse_price(price):
	return float(price.replace(' ', '').replace('zł', '').replace(',','.').replace('donegocjacji',''))

db = sqlite3.connect('dane.db')
cursor = db.cursor()

if len(argv) > 1 and argv[1] == 'setup':
	cursor.execute('''CREATE TABLE offers (name TEXT, price REAL, city TEXT, date TEXT )''')
	quit()
#python main.py setup

page = get(URL)
bs = BeautifulSoup(page.content, "html.parser")

for offer in bs.find_all('div', class_='css-9nzgu8'):
	name = offer.find('h6', class_='css-v3vynn-Text eu5v0x0').get_text().strip()
	price = parse_price(offer.find('p', class_='css-wpfvmn-Text eu5v0x0').get_text())
	location = offer.find('p', class_='css-p6wsjo-Text eu5v0x0').get_text().strip().split('-')[0]
	time_added = offer.find('p', class_='css-p6wsjo-Text eu5v0x0').get_text().strip().split('-')[1]
	#link = offer.find('a href', class_='css-1bbgabe')
	#link = offer.find('a')
	#print(link)
	cursor.execute('INSERT INTO offers VALUES(?,?,?,?)',(name,price,location,time_added))
	db.commit()

db.close()

