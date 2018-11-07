# -*- coding: utf-8 -*-
import urllib2, urllib, base64


def sendPopoByUrl(to, msg):
    """
        to: 使用popo帐号的前缀.
    """
    if "@" in to:
        to = to.split("@")[0]
    try:
        text = msg.decode("utf-8").encode("gbk")
    except:
        text = msg
    text = urllib.urlencode ({'receiver': to, 'msg': base64.encodestring(text),} )
    url = 'http://10.240.120.155:9001/sendpopo?%s' % text
    print url
    try:
        req = urllib2.urlopen(url)
    except Exception, e:
        print e
    return


def send_popo_batch(toList, msg):
    """批量发送popo消息"""
    from backend import app
    import threading

    with app.app_context():
        if not toList:
            return
        if type(toList) != list:
            sendPopoByUrl(toList, msg)
        else:
            sendPopoByUrl(toList[0], msg)
            timer = threading.Timer(3, send_popo_batch, [toList[1:], msg])
            timer.start()


def send_popo_correspond(dataList):
    """对应发送消息"""
    from backend import app
    import threading

    with app.app_context():
        if not dataList:
            return
        sendPopoByUrl(dataList[0].get("to"), dataList[0].get("msg"))
        timer = threading.Timer(3, send_popo_correspond, [dataList[1:], ])
        timer.start()

