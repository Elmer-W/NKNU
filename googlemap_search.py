import configparser
import googlemaps
from linebot.models import *
import time

# config = configparser.ConfigParser()
# config.read('config.ini')
# API_KEY = config['GOOGLEMAP']['API_KEY']
def get_ROI(keyword,location):
    gmaps = googlemaps.Client(key = 'AIzaSyBc1coUqxjfvS2fKO3X-hZByK6kZ8SGjOQ')

    places = gmaps.places_nearby(
        location=location,
        keyword=keyword,
        radius=2500,
        language='zh-TW'
        )
    result = []
    count = 0
    for place in sorted(places['results'], key=lambda x: x['rating'], reverse=True):
        name = place['name']
        star = place['rating']
        lat = place['geometry']['location']['lat']
        lon = place['geometry']['location']['lng']

        detail = gmaps.place(place_id=place['place_id'], language='zh-TW')
        address,phone_number,workTime,iconUrl = None,None,None,None
        try:
            address = detail['result']['formatted_address']
            locationURL = 'https://www.google.com/maps/search/?api=1&query={}'.format(address)
        except:
            locationURL = 'https://www.google.com/maps/search/?api=1&query={},{}'.format(lat,lon)
        try:
            phone_number = 'tel:' + detail['result']['international_phone_number'].replace(' ','-')
            phoneAction = URIAction(
                label='電話訂位',
                uri=phone_number
            )
        except:
            phone_number = 'tel:0800000123'
            phoneAction = URIAction(
                label='無電話訂位',
                uri=phone_number
            )
        try:
            dayOfWeek = time.strftime('%w',time.gmtime(time.time()+28800))
            workTime = detail['result']['opening_hours']['weekday_text'][int(dayOfWeek)-1]
        except:
            workTime = '未提供營業時間'
        try:
            iconUrl = detail['result']['icon']
        except:
            iconUrl = 'https://cdn.pixabay.com/photo/2016/11/22/11/48/cup-1849083_960_720.png'
        
        actionList = [
            URIAction(
                label='Google Map',
                uri=locationURL
            )
        ]
        actionList.append(phoneAction)

        text = 'Goolge評價：{}\n營業時間：\n{}'.format(star,workTime)
        result.append(CarouselColumn(
                thumbnail_image_url=iconUrl,
                title=name,
                text=text,
                actions=actionList
        	)
        )
        count += 1
        if count == 10:
            break

    return result

if __name__ == '__main__':
    API_key = 'AIzaSyBc1coUqxjfvS2fKO3X-hZByK6kZ8SGjOQ'
    get_ROI('拉麵',(22.6229005, 120.3089579))