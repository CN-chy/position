import time
import requests
import hashlib
from urllib.parse import unquote
def gen_qs(url):
    qs = url.split('?')[1]
    qs = qs.split('&')
    qs.sort(key=lambda e: e.split('=')[0])
    return '&'.join(qs)

def gen_sign(url , timestamp, salt='d5aaacbkgy988cpdtq5m97720j1t5u8m'):
    qs = gen_qs(url)
    data = qs + salt + str(timestamp)[:8]
    sign = hashlib.md5(data.encode()).hexdigest()
    return sign

def send_sms(phone):
    url = f'https://qzb.cntjhr.com/newapi/api/user/login/sendcode?phone={phone}&ischeckLogin=0'
    timestamp = int(time.time())
    headers = {
        'Host': 'qzb.cntjhr.com',
        'Connection': 'keep-alive',
        'timestamp': str(timestamp),
        'xweb_xhr': '1',
        'Authorization': '',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c11)XWEB/11275',
        'sign':  gen_sign(unquote(url) ,timestamp),
        'appkey': 'ZBE36LCpWHtL',
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://servicewechat.com/wx8df0c890844bdc43/42/page-frame.html',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    time.sleep(1)
    res = requests.get(url, headers=headers, verify=False)
    data = res.json()
    print(data)
    return data['code'] == 10000

def get_token(phone, smscode):
    url = 'https://qzb.cntjhr.com/newapi/api/user/login/login'
    timestamp = int(time.time())
    para = {
        'username': phone,
        'password': smscode,
        'login_type': '0',
        'agid': '',
        'device_id': '17388395118776850392',
        'qr_code': ''
    }
    qs = '?'
    for key, value in para.items():
        qs += key
        qs += '='
        qs += value
        qs += '&'
    qs = qs[:-1]
    headers = {
        'Host': 'qzb.cntjhr.com',
        'Connection': 'keep-alive',
        'timestamp': str(timestamp),
        'xweb_xhr': '1',
        'Authorization': '',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c11)XWEB/11275',
        'sign':  gen_sign(unquote(url) + qs ,timestamp),
        'appkey': 'ZBE36LCpWHtL',
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://servicewechat.com/wx8df0c890844bdc43/42/page-frame.html',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    time.sleep(1)

    res = requests.post(url, headers=headers, verify=False, data=para)
    print(res.text)
    data = res.json()['data']
    print(data)
    return data['token']
# phone = '17823263306'
# if send_sms(phone):
#     smscode = str(input('验证码：'))
#     print(smscode)
#     print(get_token(smscode, phone))
