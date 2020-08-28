import requests
import time
import configparser

config = configparser.ConfigParser()
config.read('statics/config.ini')

def get_weather_info_by_geo(lat, lon):
	url = 'http://api.openweathermap.org/data/2.5/weather'
	payload = {
		'lat':lat,
		'lon':lon,
		'units':'metric',
		'appid':config['OPENWEATHERMAP']['API_KEY']
	}
	returnText = ''
	try:
		r = requests.get(url,params=payload)
		result = r.json()
		if result['cod'] == 200:
			sunrise = time.strftime("%H:%M:%S",time.localtime(result['sys']['sunrise']))
			sunset = time.strftime("%H:%M:%S",time.localtime(result['sys']['sunset']))
			lat = result['coord']['lat']
			lon = result['coord']['lon']
			weather = result['weather'][0]['description']
			temp = result['main']['temp']
			
			returnText += '經度：{}\t緯度：{}\n天氣狀況：{}\n溫度：{}\n日出：{}\t日落：{}'.format(lat,lon,weather,temp,sunrise,sunset)
		
		elif result['cod'] == '404':
			returnText += result['message']
	except Exception as e:
		returnText += '連不上伺服器，發生未知錯誤'+'\n'+str(e)

	return returnText

if __name__ == '__main__':
	pass