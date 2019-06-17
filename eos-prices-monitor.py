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

    btc_last = 0
    eos_last = 0

    btc_price = api.get_last_ticker(symbol='btcusdt')['tick']['data'][0]['price']
    print('Now BTC price:', btc_price)
    eos_price = api.get_last_ticker(symbol='eosusdt')['tick']['data'][0]['price']
    print('Now EOS price:', eos_price)

    while True:
        try:
            btc_kline = api.get_last_24h_kline(symbol='btcusdt')
            if btc_kline['status'] == 'ok':
                tick = btc_kline['tick']
                if tick['open'] < tick['close']:
                    if (tick['close'] - tick['open']) / tick['open'] >= conf.last_24h_precent:
                        if btc_last == 0:
                            btc_last = tick['close']
                            send_dingtalk_msg('BTC price increase to ' + str(tick['close']), conf.robot_id)
                        else:
                            if btc_last < tick['close']:
                                btc_last = tick['close']
                                send_dingtalk_msg('BTC price increase to ' + str(tick['close']), conf.robot_id)
                else:
                    if (tick['open'] - tick['close']) / tick['open'] >= conf.last_24h_precent:
                        if btc_last == 0:
                            btc_last = tick['close']
                            send_dingtalk_msg('BTC price fall to ' + str(tick['close']), conf.robot_id)
                        else:
                            if btc_last > tick['close']:
                                btc_last = tick['close']
                                send_dingtalk_msg('BTC price fall to ' + str(tick['close']), conf.robot_id)

        except Exception as err:
            print('fail to get last 24h BTC kline, exception:', err)

        try:
            eos_kline = api.get_last_24h_kline(symbol='eosusdt')
            if eos_kline['status'] == 'ok':
                tick = eos_kline['tick']
                if tick['open'] < tick['close']:
                    if (tick['close'] - tick['open']) / tick['open'] >= conf.last_24h_precent:
                        if eos_last == 0:
                            eos_last = tick['close']
                            send_dingtalk_msg('EOS price increase to ' + str(tick['close']), conf.robot_id)
                        else:
                            if eos_last < tick['close']:
                                eos_last = tick['close']
                                send_dingtalk_msg('EOS price increase to ' + str(tick['close']), conf.robot_id)
                else:
                    if (tick['open'] - tick['close']) / tick['open'] >= conf.last_24h_precent:
                        if eos_last == 0:
                            eos_last = tick['close']
                            send_dingtalk_msg('EOS price fall to ' + str(tick['close']), conf.robot_id)
                        else:
                            if eos_last > tick['close']:
                                eos_last = tick['close']
                                send_dingtalk_msg('EOS price fall to ' + str(tick['close']), conf.robot_id)

        except Exception as err:
            print('fail to get last 24h EOS kline, exception:', err)

        time.sleep(conf.interval)

        try:
            new_btc_price = api.get_last_ticker(symbol='btcusdt')['tick']['data'][0]['price']
            if new_btc_price > btc_price:
                if (new_btc_price - btc_price) / btc_price >= conf.diff_precent:
                    send_dingtalk_msg('Price increase to ' + str(new_btc_price), conf.robot_id)
            else:
                if (btc_price - new_btc_price) / btc_price >= conf.diff_precent:
                    send_dingtalk_msg('Price fall to ' + str(conf.diff_precent), conf.robot_id)
            btc_price = new_btc_price
        except Exception as err:
            print('fail to get last BTC price, exception:', err)

        try:
            new_eos_price = api.get_last_ticker(symbol='eosusdt')['tick']['data'][0]['price']
            if new_eos_price > eos_price:
                if (new_eos_price - eos_price) / eos_price >= conf.diff_precent:
                    send_dingtalk_msg('Price increase to ' + str(new_eos_price), conf.robot_id)
            else:
                if (eos_price - new_eos_price) / eos_price >= conf.diff_precent:
                    send_dingtalk_msg('Price fall to ' + str(conf.diff_precent), conf.robot_id)
            eos_price = new_eos_price
        except Exception as err:
            print('fail to get last EOS price, exception:', err)
