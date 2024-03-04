import os
import time
import json

import requests
import socket

welcome_header = {
    "Host": "1.1.1.1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0"
                  "Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Content-Type": "application/x-www-form-urlencoded"
}


def init_userinfo():
    if not os.path.exists('./config.json'):
        get_userinfo()
    with open('./config.json', 'r') as f:
        data = json.load(f)
        return data


def get_userinfo():
    print('你需要输入你的登录信息，如果你是第一次使用该程序，那么这很正常')
    print('如果你第二次(或更多次)看到这条消息，请提交issues')
    print('现在你需要输入你的学号，然后按下回车')
    sid_i = input()
    print('输入你的登录密码(目前河南电子科技大学的默认密码为身份证后六位),然后按下回车')
    password_i = input()
    print('现在你需要选择你的运营商， 请输入(1,2)中的一个，1为电信, 2为联通,然后按下回车')  # telecom unicom
    ISP_select_i = 'telecom' if input() == '1' else 'unicom'

    d = {
        "sid": sid_i,
        "password": password_i,
        "ISP_select": ISP_select_i
    }

    with open('./config.json', 'a+') as f:
        f.write(json.dumps(d))
        f.flush()
        f.close()


def getTargetIP(prefix) -> str:
    result = '-1'
    count = 0
    while result == '-1' and count < 20:
        for i in socket.gethostbyname_ex(socket.gethostname())[2]:
            if i.startswith(prefix):
                result = i
        count += 1
        time.sleep(3)
    if result == '-1':
        raise RuntimeError("you didn't connect to schoolNet in 1 minute since boot")
    return result


def login():
    login_url = f'http://1.1.1.1:801/eportal/?' \
                f'c=ACSetting&' \
                f'a=Login&protocol=http:&' \
                f'hostname=1.1.1.1&' \
                f'iTermType=1&' \
                f'wlanuserip={getTargetIP(schoolNetStartWith)}&' \
                f'wlanacip=null&' \
                f'wlanacname=null&' \
                f'mac=00-00-00-00-00-00&' \
                f'ip={getTargetIP(schoolNetStartWith)}&' \
                f'enAdvert=0&' \
                f'queryACIP=0&' \
                f'loginMethod=1'
    body = {
        "DDDDD": f'%2c0%2c{sid}@{ISP_select}',
        "upass": password,
        "R1": "0",
        "R2": "0",
        "R3": "0",
        "R6": "0",
        "para": "00",
        "0MKKey": "123456",
        "buttonClicked": "",
        "redirect_url": "",
        "err_flag": "",
        "username": "",
        "password": "",
        "user": "",
        "cmd": "",
        "Login": ""
    }

    data = ''

    for i in body.items():
        data += '&'
        data += f'{i[0]}={i[1]}'

    data = data[1:]

    response = requests.post(url=login_url, data=data, headers=welcome_header, verify=False)

    if response.text.split('<title>')[1].split('</title>')[0] != '认证成功页':
        sResponse = requests.post(url=login_url, data=data, headers=welcome_header, verify=False)


if __name__ == '__main__':
    url = "http://1.1.1.1"

    schoolNetStartWith = '10.133'

    ud = init_userinfo()

    sid = ud['sid']
    password = ud['password']
    ISP_select = ud['ISP_select']
    login()
