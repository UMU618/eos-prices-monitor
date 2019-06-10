import json
import urllib.request
import ssl
from huobitrade import HBRestAPI, setUrl
import time
import conf

def send_dingtalk_msg(content, robot_id):
    print(content)
    try:
        msg = {'msgtype': 'text', 'text': {'content': content}}

        Headers = {'Content-Type': 'application/json; charset=utf-8'}
        url = 'https://oapi.dingtalk.com/robot/send?access_token=' + robot_id
        body = bytes(json.dumps(msg), 'utf-8')
        req = urllib.request.Request(url, data=body, headers=Headers)
        response = urllib.request.urlopen(req, context=ssl._create_unverified_context())
        if response.code != 200:
            print('fail to send dingtalk, status =', response.code)
            return False
        js = json.loads(response.read())
        if js['errcode'] != 0:
            print('fail to send dingtalk, errcode =', js['errcode'])
            return False
        return True
    except Exception as err:
        print('fail to send dingtalk, exception:', err)


if __name__ == '__main__':
    setUrl('https://api.huobi.pro', 'https://api.huobi.pro')
    api = HBRestAPI()
    price = api.get_last_ticker(symbol='eosusdt')['tick']['data'][0]['price']
    print('Now price:', price)
    while True:
        time.sleep(conf.interval)
        newprice = api.get_last_ticker(symbol='eosusdt')['tick']['data'][0]['price']
        if newprice > price:
            if (newprice - price) / price > conf.diff_precent:
                send_dingtalk_msg('Price increase to ' + newprice, conf.robot_id)
        else:
            if (price - newprice) / price > conf.diff_precent:
                send_dingtalk_msg('Price fall to ' + conf.diff_precent, conf.robot_id)
        price = newprice
