import requests
from bs4 import BeautifulSoup
from linebot.models import *
import json
import copy
import random

def randomColor():
    color = '#'
    for _ in range(3):
        color += hex(random.randint(150,240))[2:]
    return color

def create_quick_replyButtons():
    itemList = []
    for astro in ['牡羊座','金牛座','雙子座','巨蟹座','獅子座','處女座','天秤座','天蠍座','射手座','摩羯座','水瓶座','雙魚座']:
        itemList.append(
            QuickReplyButton(
                action=PostbackAction(
                    label=astro,
                    data=astro
                    )
                )
            )

    message = TextSendMessage(
    text='選擇星座',
    quick_reply=QuickReply(
        items=itemList
        )
    )
    return message

def get_astro_info(astro):

    template_base = json.loads('''
        {
            "type": "carousel",
            "contents": []
        }
    ''')

    raw_template_card = json.loads('''
        {
          "type": "bubble",
          "size": "nano",
          "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "",
                "color": "#ffffff",
                "align": "start",
                "size": "md",
                "gravity": "center"
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": []
              }
            ],
            "backgroundColor": "",
            "paddingTop": "19px",
            "paddingAll": "12px",
            "paddingBottom": "16px"
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "",
                    "color": "#8C8C8C",
                    "size": "sm",
                    "wrap": true
                  }
                ],
                "flex": 1
              }
            ],
            "spacing": "md",
            "paddingAll": "12px"
          },
          "styles": {
            "footer": {
              "separator": false
            }
          }
        }
    ''')

    yellowStar = json.loads('''
    {
    "type": "icon",
    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
    }
    ''')
    greyStar = json.loads('''
    {
    "type": "icon",
    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"
    }
    ''')

    logo_template = json.loads('''
    {
      "type": "bubble",
      "size": "nano",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "",
                "color": "#444444",
                "size": "5xl",
                "wrap": true,
                "align": "center",
                "gravity": "center",
                "weight": "bold"
              }
            ],
            "flex": 1
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "",
                "color": "#444444",
                "size": "5xl",
                "wrap": true,
                "align": "center",
                "gravity": "center",
                "weight": "bold"
              }
            ],
            "flex": 1
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "",
                "color": "#444444",
                "size": "5xl",
                "wrap": true,
                "align": "center",
                "gravity": "center",
                "weight": "bold"
              }
            ],
            "flex": 1
          }
        ],
        "spacing": "md",
        "paddingAll": "12px",
        "backgroundColor": ""
      },
      "styles": {
        "footer": {
          "separator": false
        }
      }
    }
    ''')
    astro_name_list = []
    astro_name_list.extend(astro)
    for index in range(3):
        logo_template['body']['contents'][index]['contents'][0]['text'] = astro_name_list[index]
    logo_template['body']['backgroundColor'] = randomColor()
    template_base['contents'].append(logo_template)

    astroList = ['牡羊座','金牛座','雙子座','巨蟹座','獅子座','處女座','天秤座','天蠍座','射手座','摩羯座','水瓶座','雙魚座']
    index = astroList.index(astro)
    url = 'https://astro.click108.com.tw/daily_2.php?iAstro={}'.format(index)
    webContent = requests.get(url)
    webContent.encoding = 'UTF-8'

    soup = BeautifulSoup(webContent.text, 'html.parser')
    ptagList = soup.select('.TODAY_CONTENT')[0].select('p')
    for index, ptag in list(enumerate(ptagList))[::2]:
        template_card = copy.deepcopy(raw_template_card)

        template_card['header']['backgroundColor'] = randomColor()
        
        titleText = ptagList[index].text
        y_star_amount = titleText.count('★')
        g_star_amount = titleText.count('☆')
        titleText = titleText.replace('★','').replace('☆','').replace('：','')

        template_card['header']['contents'][0]['text'] = titleText
        template_card['body']['contents'][0]['contents'][0]['text'] = ptagList[index+1].text
        
        for _ in range(y_star_amount):
            template_card['header']['contents'][1]['contents'].append(yellowStar)
        
        for _ in range(g_star_amount):
            template_card['header']['contents'][1]['contents'].append(greyStar)
        
        template_base['contents'].append(template_card)
    return template_base

# file = open('template.json', mode= 'w' ,encoding='utf-8')
# json.dump(get_astro_info('牡羊座'), file, ensure_ascii=False)