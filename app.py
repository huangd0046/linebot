from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


#======這裡是呼叫的檔案內容=====
from message import *
from new import *
from Function import *
#======這裡是呼叫的檔案內容=====

import pyodbc

server = 'smartsalesdata.database.windows.net'  
database = 'SmartSalesData' 
username = 'smartsales' 
password = 'Smart123' 
connectionstring = 'DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password
conn = pyodbc.connect(connectionstring) 
cursor = conn.cursor()
cursor.execute('update Member set Line = 200 where MemberID =1')

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('Juhemq8ByKN1Gda06cL4k6Rfiet5f3lde8Vu7YB+cwZP/7HAG2KeqJnGEHs1EsU+pkr/1C1+PvHslVJhA6XZix4htkHZc7gc6Pltd8yy9jKIRgVoxHhGwdU1+T6rniID5ao2M6i8oOIzl+qFilSVggdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('71412c86f65f7fde579e5e030daa8170')
# User ID
to = 'U4c911f672e86fec082cf3dfeec378b3b'


def sendMessage():
    try:
        line_bot_api.push_message(to, TextSendMessage(text='台科大電腦研習社'))
    except LineBotApiError as e:
        # error handle
        raise e
sendMessage()


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if '最新合作廠商' in msg:
        user_id = event.source.user_id
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=user_id))

       # message = imagemap_message()
       # line_bot_api.reply_message(event.reply_token, message)
    elif '最新活動訊息' in msg:
        message = buttons_message()
        line_bot_api.reply_message(event.reply_token, message)
    elif '註冊會員' in msg:
        message = Confirm_Template()
        line_bot_api.reply_message(event.reply_token, message)
    elif '旋轉木馬' in msg:
        message = Carousel_Template()
        line_bot_api.reply_message(event.reply_token, message)
    elif '圖片畫廊' in msg:
        message = test()
        line_bot_api.reply_message(event.reply_token, message)
    elif '功能列表' in msg:
        message = function_list()
        line_bot_api.reply_message(event.reply_token, message)
    else:
        message = TextSendMessage(text=msg)
        line_bot_api.reply_message(event.reply_token, message)


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
