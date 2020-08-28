import requests
from bs4 import BeautifulSoup

url = 'http://feeds.bbci.co.uk/news/video_and_audio/world/rss.xml'

webContent = requests.get(url)
webContent.encoding = 'utf-8'
soup = BeautifulSoup(webContent.text,'xml')
for story in soup.select('item'):
    try:
        print(story.pubDate.text)
        print(story.title.text)
        print(story.description.text.replace('[&#8230;]','...').replace('…',''))
        print(story.link.text)
        print('--------')
    except:
        continue