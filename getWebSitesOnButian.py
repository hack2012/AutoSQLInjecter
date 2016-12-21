#!/usr/bin/env/ python
#coding:utf8
import requests
from bs4 import BeautifulSoup

url = "http://butian.360.cn/company/lists/page/"

def getMaxPageNumber(content):
    soup = BeautifulSoup(content, "html.parser")
    divs = soup.find("div", class_="pages")
    as_ = divs.findAll("a")
    pages_text = as_[-1].get("href")
    return int(pages_text.split("/")[-1])

def getWebSites(content):
    results = []
    soup = BeautifulSoup(content, "html.parser")
    trs = soup.findAll("tr")
    for tr in trs:
        tds = tr.findAll('td',align="left",style="padding-left:20px;")
        tds = tds[1:]
        for td in tds:
            url = td.string
            result = url
            results.append(result)
    return results

def getContentOfPage(url):
    return requests.get(url).text

maxPageNumber = getMaxPageNumber(getContentOfPage(url + "1"))

for page in range(1,maxPageNumber + 1):
    try:
        tempURL = url + str(page)
        print "Getting : " + tempURL
        result = getWebSites(getContentOfPage(tempURL))
        outfile = open("websites.txt", "a+")
        for res in result:
            outfile.write("http://" + res + "/\n")
        outfile.close()
    except Exception as e:
        pass
