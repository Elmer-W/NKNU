import requests
from bs4 import BeautifulSoup
import random
from linebot.models import *

def spotify_random():
	url = 'https://spotifycharts.com/regional/'
	webContent = requests.get(url)
	webContent.encoding = 'UTF-8'

	soup = BeautifulSoup(webContent.text, 'html.parser')
	result = []

	songList = soup.select('table.chart-table tbody tr')
	random.shuffle(songList)
	for song in songList[:10]:
		songLink = song.select('td a')[0]['href']
		webContent = requests.get(songLink)

		temp = song.select('td')[3]
		songName = temp.select('strong')[0].text
		artist = temp.select('span')[0].text[3:]
		albumArtLink = song.select('td')[0].select('img')[0]['src'].replace('ab67616d00004851','ab67616d00001e02')
		result.append(CarouselColumn(
                thumbnail_image_url=albumArtLink,
                title=artist,
                text=songName,
                actions=[
                	URIAction(
						label='Open on Spotify',
						uri=songLink
					),
					MessageAction(
						label='顯示歌手與歌名',
						text='{} by {}'.format(songName,artist)
					)
                ]
        	)
        )

	return result

if __name__ == '__main__':
	print(spotify_random())