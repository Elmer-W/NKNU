import requests
import json

def get_route_id(search):
    url = 'https://ibus.tbkc.gov.tw/bus/NewAPI/RealRoute.ashx'
    data = {
        'type':'GetRoute',
        'lang':'Cht'
    }
    for route in requests.post(url, data=data).json():
        if search == route['nameZh']:
            return route['ID']
    return None

def get_route_info(route_name):
    url = 'https://ibus.tbkc.gov.tw/bus/newAPI/GetEstimateTime.ashx'
    routeid = get_route_id(route_name)
    if routeid == None:
        return '沒有相符的公車路線'
    else:
        data = {
            'type': 'Web',
            'routeid':routeid,
            'lang':'Cht'
        }

        # result = ''
        # for route in [requests.post(url, data=data).json()[0]]:
        #     for stop in route['cometime']:
        #         result += stop['stopname'] + stop['cometime'] +'\n'
        #     result += '----------------\n'
        # return result
        base = json.load(open(r'C:\Users\dream\Desktop\NKNU-LineBot\static\bus_route_base.json'))
        line = json.load(open(r'C:\Users\dream\Desktop\NKNU-LineBot\static\bus_route_line.json'))
        for route in [requests.post(url, data=data).json()[0]]:
            for index,stop in enumerate(route['cometime'][:5]):
                station = json.load(open(r'C:\Users\dream\Desktop\NKNU-LineBot\static\bus_route_station.json'))
                station['contents'][2]['text'] = stop['stopname']
                station['contents'][0]['text'] = stop['cometime']
                base['body']['contents'].append(station)
                if index != 4:
                    base['body']['contents'].append(line)
        # base = json.load(open(r'C:\Users\dream\Desktop\NKNU-LineBot\static\bus_route.json'))
        return base

print(get_route_info('7A'))