import requests
import csv
from haversine import haversine

def get_radiation_info_by_geo(lat, lon):
	url = 'http://www.aec.gov.tw/open/gammamonitor.csv'
	result = requests.get(url)
	result.encoding = 'BIG5'

	location_A = (lat, lon)
	distance = 100000000000
	closest_station = []

	rows = csv.DictReader(result.text.splitlines())
	for row in rows:
		location_B = (float(row['GPS緯度']),float(row['GPS經度']))
		temp = haversine(location_A, location_B)
		if  temp < distance:
			closest_station = row
			distance = temp

	returnText = '離你最近的是{}監測站，數值是{}(微西弗/時)'.format(closest_station['監測站'],closest_station['監測值(微西弗/時)'])
	return returnText

if __name__ == '__main__':
	pass