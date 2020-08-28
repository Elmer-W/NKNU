import email.message
import smtplib
import re

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

def send_attachment_Email(subject, attachment, manageremail):
    password = ''
    account = ''

    msg = MIMEMultipart()
    msg['From'] = ''
    msg['To'] = manageremail
    msg['Subject'] = subject

    with open(attachment, 'rb') as f:
        content = MIMEBase('application','octet-steam')
        content.set_payload(f.read())
    encoders.encode_base64(content)
    content.add_header('Content-Disposition', 'attachment', filename = attachment)
    msg.attach(content)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(account, password)
    server.sendmail(account, manageremail, msg.as_string())
    server.close()

def Email_verification(userEmail):
    regx = r'^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]+$'
    if re.match(regx,userEmail) != None:
        return userEmail
    else:
        return None

def send_certification_letter(userEmail, randomNumber):
    password = ''
    account = ''

    msg = email.message.EmailMessage()

    msg['From'] = ''
    msg['To'] = userEmail
    msg['Subject'] = 'HP2020LineBot 認證碼'

    content = '您好，歡迎註冊HP2020LineBot\n\t你的認證碼是：{}'.format(randomNumber)

    msg.set_content(content)
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(account, password)
        server.send_message(msg)
        server.close()
        return True
    except:
        return False