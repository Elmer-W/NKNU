import requests
import csv
from haversine import haversine

def get_AQI_info_by_geo(lat, lon):
	url = 'https://data.epa.gov.tw/api/v1/aqx_p_432?limit=1000&api_key=9be7b239-557b-4c10-9775-78cadfc555e9&format=csv'
	result = requests.get(url)
	result.encoding = 'UTF-8'
	location_A = (lat, lon)
	distance = 100000000000
	closest_station = []

	rows = csv.DictReader(result.text.splitlines())
	for row in rows:
		location_B = (float(row['Latitude']),float(row['Longitude']))
		temp = haversine(location_A, location_B)
		if  temp < distance:
			closest_station = row
			distance = temp

	PM25 = closest_station['PM2.5']
	siteName = closest_station['\ufeffSiteName']
	AQI = int(closest_station['AQI'])
	
	AQIList = [50,100,150,200,300,500,600]
	colorList = ['綠色','黃色','橘色','紅色','紫色','棗紅色','棗紅色']
	AQIList.append(AQI)
	color = colorList[sorted(AQIList).index(AQI)]

	returnText = '以下為{}站提供的資訊\nAQI指數：{}警報\nPM2.5：{}'.format(siteName,color,PM25)
	
	return returnText

if __name__ == '__main__':
	pass