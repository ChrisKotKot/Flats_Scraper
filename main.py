from bs4 import BeautifulSoup
from requests import get

URL = 'https://www.olx.pl/d/nieruchomosci/mieszkania/sprzedaz/podlaskie/'

def parse_price(price):
	return float(price.replace(' ', '').replace('zł', '').replace(',','.').replace('donegocjacji',''))

page = get(URL)
bs = BeautifulSoup(page.content, "html.parser")

for offer in bs.find_all('div', class_='css-9nzgu8'):
	name = offer.find('h6', class_='css-v3vynn-Text eu5v0x0').get_text()
	price = parse_price(offer.find('p', class_='css-wpfvmn-Text eu5v0x0').get_text())
	location = offer.find('p', class_='css-p6wsjo-Text eu5v0x0').get_text().strip().split('-')[0]
	#time_added = offer.find('p', class_='css-p6wsjo-Text eu5v0x0').get_text().strip().split('-')[1]
	print(name, price, location)
