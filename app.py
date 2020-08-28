from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
import configparser
from function.AQI_monitor import get_AQI_info_by_geo
from function.radiation_monitor import get_radiation_info_by_geo
from function.weather_monitor import get_weather_info_by_geo
from function.spotify_top_200 import spotify_random
from function.astro import *
from function.bus_route import *
import json
import twder
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from function.email_cer import send_certification_letter
import random
import os


config = configparser.ConfigParser()
config.read('config.ini')
access_token = config['LINE']['ACCESS_TOKEN']
secret = config['LINE']['SECRET']
# scope=['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
# creds = ServiceAccountCredentials.from_json_keyfile_name('HP2020DEMO-a85244012f28.json',scope)
# client = gspread.authorize(creds)
# spreadSheet = client.open('HP2020LINEBOT')
# workSheet_user = spreadSheet.worksheet('user')
# workSheet_status = spreadSheet.worksheet('status')

app = Flask(__name__)
app.config['DEBUG'] = True

line_bot_api = LineBotApi(access_token)
handler = WebhookHandler(secret)

def get_user_info_from_gsheet(event):
    userID = event.source.user_id
    try:
        cell = workSheet_status.find(userID)
        user_row = cell.row
        user_col = cell.col
        user_status = workSheet_status.cell(user_row,2).value
    except:
        workSheet_status.append_row([userID,'未註冊'])
        workSheet_user.append_row([userID])
        cell = workSheet_status.find(userID)
        user_row = cell.row
        user_col = cell.col
        user_status = workSheet_status.cell(user_row,2).value

    return user_row, user_col, user_status, userID

def user_register_flow(user_row, user_col, user_status, userID, userSend):
    if user_status == '未註冊':
        workSheet_status.update_cell(user_row,2,'註冊中-1')
        message = TextSendMessage(text='請輸入姓名，讓我認識妳/你！')
    
    elif user_status == '註冊中-1':
        workSheet_user.update_cell(user_row,2,userSend)
        workSheet_status.update_cell(user_row,2,'註冊中-2')
        message = TextSendMessage(
            text='請到手機上選擇日期',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=
                            DatetimePickerAction(
                                label="請輸入生日",
                                data="birthday",
                                mode="date",
                                initial="1990-01-01",
                                max="2002-12-31",
                                min="1930-01-01"
                        )
                    )
                ]
            )
        )
    elif user_status == '註冊中-2':
        workSheet_user.update_cell(user_row,3,userSend)
        workSheet_status.update_cell(user_row,2,'註冊中-3')
        message = TextSendMessage(text='請輸入你的電子郵件')

    elif user_status == '註冊中-3':
        workSheet_user.update_cell(user_row,4,userSend)
        certification_number = str(random.randint(1000,9999))
        send_certification_letter(userSend, certification_number)
        workSheet_status.update_cell(user_row,3,certification_number)
        workSheet_status.update_cell(user_row,2,'註冊中-4')
        message = TextSendMessage(text='請輸入您的認證碼\n(請至電子郵件中取得認證碼)')

    elif user_status == '註冊中-4':
        certification_number = workSheet_status.cell(user_row,3).value
        if str(certification_number) == userSend:
            workSheet_status.update_cell(user_row,2,'已註冊')
            message = TextSendMessage(text='註冊完成')
        else:
            message = TextSendMessage(text='認證錯誤，請重新認證碼')
    return message

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@app.route("/callback", methods=['GET'])
def show():
    return '<h1>This is a LineBot Server.</h1>'

@app.route('/')
def hello():
    return '<h1>Success</h1>'

@app.errorhandler(Exception)
def handle_error_message(e):
    import traceback
    error = traceback.format_exc()
    app.logger.info('Error:'+error)

@handler.add(PostbackEvent)
def handle_postback_message(event):
    user_row, user_col, user_status, userID = get_user_info_from_gsheet(event)
    userSend = event.postback.data
    if userSend in ['牡羊座','金牛座','雙子座','巨蟹座','獅子座','處女座','天秤座','天蠍座','射手座','摩羯座','水瓶座','雙魚座']:
        #message = TextSendMessage(text=userSend+'\n'+get_astro_info(userSend))
        result = get_astro_info(userSend)
        message = FlexSendMessage(alt_text='星座運勢小卡', contents = result)
    elif userSend == 'birthday':
        birthday = event.postback.params['date']
        message = user_register_flow(user_row, user_col, user_status, userID, birthday)
    line_bot_api.reply_message(event.reply_token, message)


@handler.add(MessageEvent, message=TextMessage)
 def handle_message(event):
    userSend = event.message.text
    message = TextSendMessage(text='聽不懂')
    line_bot_api.reply_message(event.reply_token, message)
# def handle_message(event):
#     user_row, user_col, user_status, userID = get_user_info_from_gsheet(event)
#     userSend = event.message.text
#     if user_status != '已註冊':
#         message = user_register_flow(user_row, user_col, user_status, userID, userSend)

#     elif user_status == '已註冊':
#         if userSend in ['music','音樂','Music']:
#             message = TemplateSendMessage(
#                     alt_text='隨機從Spotify top 200 取10首歌',
#                     template=CarouselTemplate(
#                         columns=spotify_random()
#                     )
#                 )
#         elif userSend in ['astro','星座','運勢','星座運勢']:
#             message = create_quick_replyButtons()

#         else:
#             message = TextSendMessage(text='聽不懂')
#     line_bot_api.reply_message(event.reply_token, message)

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    user_row, user_col, user_status, userID = get_user_info_from_gsheet(event)

    if user_status != '已註冊':
        userSend = ''
        message = user_register_flow(user_row, user_col, user_status, userID, userSend)

    elif user_status == '已註冊':
        message = StickerSendMessage(
            package_id=11537,
            sticker_id=52002750
        )

    line_bot_api.reply_message(event.reply_token, message)

@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):

    lon = event.message.longitude 
    lat = event.message.latitude
    result = get_weather_info_by_geo(lat,lon)
    result += '\n' + get_AQI_info_by_geo(lat,lon)
    result += '\n' + get_radiation_info_by_geo(lat,lon)

    message = TextSendMessage(text=result)
    line_bot_api.reply_message(event.reply_token, message)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0',port=port)