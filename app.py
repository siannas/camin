from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import requests, json


import errno
import os
import sys, random
import tempfile
import requests
import re

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent,
)

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('MNBTHTgxlClDXGlY7TaJSz9ML46xmFXcAT6E2cSpYDyblQfKGA0cqp4KLblZdd9VcUiXn/ijaPJrusLmoKx/NFPurWF2U3+BKETV6hDMXjCaiNLEgA8VRdfp9KJvfb+kq2xo0HdauBpou7aEgk+DmwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('e0e193b4b0719aa0d83d9695edeffbad')
#===========[ NOTE SAVER ]=======================
notes = {}

def inputmhs(nrp, nama, kosan):
    r = requests.post("http://www.aditmasih.tk/api_pannas/insert.php", data={'nrp': nrp, 'nama': nama, 'alamat': kosan})
    data = r.json()

    flag = data['flag']
    
    if(flag == "1"):
        return 'Data '+nama+' berhasil dimasukkan\n'
    elif(flag == "0"):
        return 'Data gagal dimasukkan\n'

def deletemhs(nrp):
    r = requests.post("http://www.aditmasih.tk/api_pannas/delete.php", data={'nrp': nrp})
    data = r.json()
    
    flag = data['flag']
    
    if(flag == "1"):
        return 'Data '+nrp+' berhasil dihapus\n'
    elif(flag == "0"):
        return 'Data gagal dihapus\n'
    
# Post Request
def showmhs(nrp):
    r = requests.get("http://www.aditmasih.tk/api_pannas/show.php", params={'nrp': nrp})
    data = r.json()
    
    flag = data['flag']
    hasil = data['data_angkatan']
    
    if(flag == "1"):
        return "nrp : "+hasil[0]
    elif(flag == "0"):
        return 'Data Tidak ada\n'

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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text #simplify for receove message
    sender = event.source.user_id #get usesenderr_id
    gid = event.source.sender_id #get group_id
    profile = line_bot_api.get_profile(sender)
    
    
    data=text.split('-')
    if(data[0]=='tambah'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=inputmhs(data[1],data[2],data[3])))
    
    elif(data[0]=='hapus'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=deletemhs(data[1])))
    
    elif(data[0]=='tampil'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=showmhs(data[1])))
    
    elif re.search('hai', text, flags=re.IGNORECASE):
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='Hai ' + profile.display_name),
                TextSendMessage(text='statusmu : ' + profile.status_message)
            ]
        )

            
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)