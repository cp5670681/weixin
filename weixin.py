# -*- coding: utf-8 -*-
# filename: weixin.py
from flask import Flask, request, make_response
import time, hashlib
import xml.etree.ElementTree as ET
import reply
import receive
import datetime

app=Flask(__name__)

@app.route('/wechat/', methods=['GET', 'POST'])
def wechat():
    # 微信验证token
    if request.method == 'GET':
        token ='chengpeng'
        query = request.args
        signature = query.get('signature', '')
        timestamp = query.get('timestamp', '')
        nonce = query.get('nonce', '')
        echostr = query.get('echostr', '')
        s = [timestamp, nonce, token]
        s.sort()
        s = ''.join(s)
        if hashlib.sha1(s).hexdigest() == signature:
            return make_response(echostr)
    else:
        rec_msg = receive.parse_xml(request.stream.read())  #判断当前的消息类型，获取到接收实例
        
        if rec_msg.MsgType == 'text':     
            content = unicode(rec_msg.Content,"utf-8")  #转换编码为unicode，方便提取需要的文字进行判断
            if content.startswith(u"笑话",0,2):       #如果是以笑话两字开头，则进行相应回复
                 rep_text_msg = reply.TextMsg(rec_msg.FromUserName, rec_msg.ToUserName, "哈哈，我给你讲个笑话吧哈哈哈 \n %s"%ChineseTime() )  
                 return rep_text_msg.send()     #返回需要返回的xml信息  
            else:
                 rep_text_msg = reply.TextMsg(rec_msg.FromUserName,rec_msg.ToUserName,"复述：%s \n %s"%(rec_msg.Content,ChineseTime()))
                 return rep_text_msg.send()
        elif  rec_msg.MsgType =="image": #我这里的处理是，如果是图片，就返回同样的MediaId，即是回复同样的图片
            rep_img_msg = reply.ImageMsg(rec_msg.FromUserName,rec_msg.ToUserName,rec_msg.MediaId)
            return rep_img_msg.send()
        else:
            return "success"      #微信公众号规定，超过5秒未进行回复，则发起重请求，所以如果是无法识别的消息，则返回“success”，
                                       #   就不会在消息界面提示公众号异常，提升用户体验。

#获取时间戳
def getTime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
def ChineseTime():
    timenow = (datetime.datetime.utcnow() + datetime.timedelta(hours=8))
    timetext = timenow.strftime("%Y-%m-%d %H:%M:%S")
    return timetext

if __name__ == '__main__':
    app.run(debug=True)

