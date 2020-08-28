import imgkit
from function.email_cer import *

def absent(date, name, atype, reason, manageremail):

    config = imgkit.config(wkhtmltoimage='./bin/wkhtmltopdf')

    with open('absent_template.txt',mode='r',encoding='utf-8') as file:
        htmlDoc = file.read()

    y,m,d = date[0],date[1],date[2]
    htmlDoc = htmlDoc.format(y,m,d,name,atype,reason)
    imgkit.from_string(htmlDoc, 'out.pdf', config=config)
    send_attachment_Email(atype, 'out.pdf', manageremail)
    return '假單寄送成功'