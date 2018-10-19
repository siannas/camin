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

def updatemhs(nrplama,nrp, nama, kosan):
    r = requests.post("http://www.aditmasih.tk/api_pannas/update.php", data={'nrp_lama':nrplama,'nrp': nrp, 'nama': nama, 'alamat': kosan})
    data = r.json()

    flag = data['flag']
    
    if(flag == "1"):
        return 'Data '+nama+' berhasil diperbarui\n'
    elif(flag == "0"):
        return 'Data gagal diperbarui\n'    
    
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
    hasil = data['data_angkatan'][0]
    
    if(flag == "1"):
        return "nrp : " + hasil['nrp'] +"\nnama : "+hasil['nama']+"\nalamat : "+hasil['alamat']
    elif(flag == "0"):
        return 'Data Tidak ada\n'

def showallmhs():
    r = requests.get("http://www.aditmasih.tk/api_pannas/all.php")
    data = r.json()
    
    flag = data['flag']
       
    if(flag == "1"):
        text = ""
        index = 0
        
        while index<data['panjang']:
            hasil = data['data_angkatan'][index]
            index += 1
            text += str(index)+". nrp : " + hasil['nrp']
            text += "\n   nama : " + hasil['nama']
            text += "\n   alamat : " + hasil['alamat'] + "\n"            
        return text    
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
    if(data[0]=='menu'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(
            '1. tambah-nrp(5)-nama-alamat\n'+
            '2. perbarui-nrp lama-nrp(5)-nama-alamat\n'+
            '3. tampilkan-nrp(5)\n'+
            '4. hapus-nrp(5)\n'+
            '5. tampilkan semua'
        ))
    elif text == 'flex':
        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='https://example.com/cafe.jpg',
                size='full',
                aspect_ratio='20:13',
                aspect_mode='cover',
                action=URIAction(uri='http://example.com', label='label')
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    # title
                    TextComponent(text='Brown Cafe', weight='bold', size='xl'),
                    # review
                    BoxComponent(
                        layout='baseline',
                        margin='md',
                        contents=[
                            IconComponent(size='sm', url='https://example.com/gold_star.png'),
                            IconComponent(size='sm', url='https://example.com/grey_star.png'),
                            IconComponent(size='sm', url='https://example.com/gold_star.png'),
                            IconComponent(size='sm', url='https://example.com/gold_star.png'),
                            IconComponent(size='sm', url='https://example.com/grey_star.png'),
                            TextComponent(text='4.0', size='sm', color='#999999', margin='md',
                                          flex=0)
                        ]
                    ),
                    # info
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Place',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text='Shinjuku, Tokyo',
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Time',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text="10:00 - 23:00",
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5,
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    # callAction, separator, websiteAction
                    SpacerComponent(size='sm'),
                    # callAction
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='CALL', uri='tel:000000'),
                    ),
                    # separator
                    SeparatorComponent(),
                    # websiteAction
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='WEBSITE', uri="https://example.com")
                    )
                ]
            ),
        )
        message = FlexSendMessage(alt_text="hello", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
    elif(data[0]=='tambah'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=inputmhs(data[1],data[2],data[3])))
    
    elif(data[0]=='hapus'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=deletemhs(data[1])))
    
    elif(data[0]=='tampilkan'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=showmhs(data[1])))
    
    elif(data[0]=='tampilkan semua'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=showallmhs()))
        
    elif(data[0]=='perbarui'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(updatemhs(data[1],data[2],data[3],data[4])))

    elif re.search('hai', text, re.IGNORECASE):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='Hai ' + profile.display_name))
    
            
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
