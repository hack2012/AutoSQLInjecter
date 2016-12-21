#!/usr/bin/env python
#encoding:utf8

import requests
import sys
import urlparse
from bs4 import BeautifulSoup
from optparse import OptionParser

def urlParser(url):
	result = {}
	tempurl = urlparse.urlparse(url)
	result['scheme'] = tempurl.scheme
	result['hostname'] = tempurl.hostname
	result['path'] = tempurl.path
	if tempurl.port == None:
		result['port'] = 80
	else:
		result['port'] = tempurl.port
	return result

def getSchemeDomainPort(url):
	tempurl = urlparse.urlparse(url)
	return tempurl.scheme + "://" + tempurl.hostname + "/"

def getContent(url):
	return requests.get(url).text

def getAllLinks(soup):
	return soup.findAll(href=True)

def getAllHerfs(links):
	hrefs = set()
	for link in links:
		hrefs.add(link['href'])
	return hrefs

def judgeSameSource(url1,url2):
	_url1 = urlParser(url1)
	_url2 = urlParser(url2)
	if _url1['scheme'] == _url2['scheme'] and _url1['hostname'] == _url2['hostname'] and _url1['port'] == _url2['port']:
		return True
	else:
		return False

def getFatherDoamin(domain):
	fatherDomain = ""
	tempDomain = domain.split(".")[1:]
	for temp in tempDomain:
		fatherDomain += temp + "."
	fatherDomain = fatherDomain[0:-1]
	return fatherDomain

def judgeSameFatherDomain(url1,url2):
	_url1 = urlParser(url1)
	_url2 = urlParser(url2)
	if _url1['scheme'] == _url2['scheme'] and getFatherDoamin(_url1['hostname']) == getFatherDoamin(_url2['hostname']) and _url1['port'] == _url2['port']:
		return True
	else:
		return False

def getAllSameFatherDomainLinks(links):
	global url
	result = set()
	for link in links:
		if judgeSameFatherDomain(link, url):
			result.add(link)
	return result

def getAllSameSourceLinks(links):
	global url
	result = set()
	for link in links:
		if judgeSameSource(link, url):
			result.add(link)
	return result

def getCompleteLinks(links, domain):
	result = set()
	for link in links:
		if not (link.startswith("http://") or link.startswith("https://")):
			result.add(domain + link)
		else:
			result.add(link)
	return result

def removeAllAnchors(links):
	result = set()
	for link in links:
		if link.startswith("#"):
			continue # 锚点 , 自动忽略
		result.add(link)
	return result

def hrefsFilter(links, domain):
	links = removeAllAnchors(links)
	links = getCompleteLinks(links, domain)
	# links = getAllSameFatherDomainLinks(links) # 获取所有子域名下的所有链接
	links = getAllSameSourceLinks(links) # 获取同源策略下的所有链接
	links = getAllQueryLinks(links) # 获取具有查询功能的URL
	links = getAllTrueQueryLinks(links) # 这个函数是为了防止 xxx.css?v=xxx 这种情况出现的 , 使用黑名单进行过滤
	links = analyseAllLinks(links)
	links = mergeSameQuery(links)
	return links


def getAllQueryLinks(links):
	tempLinks = set()
	for link in links:
		if "?" in link:
			tempLinks.add(link)
	return tempLinks

def getAllTrueQueryLinks(links):
	blackList = ['css','js','html','htm','shtml']
	tempLinks = set()
	for link in links:
		fileUrl = link.split("?")[0]
		quertUrl = link.split("?")[1]
		SIGN = True
		for black in blackList:
			if fileUrl.endswith(black):
				SIGN = False
				break
		if SIGN:
			tempLinks.add(link)
	return tempLinks

def analyseAllLinks(links):
	# 从URL中提取查询的文件和查询参数
	result = []
	for link in links:
		templink = link.split("?")[0]
		tempQuery = link.split("?")[1]
		tempResult = {}
		tempResult['url'] = templink
		queryResult = {}
		temptempQueries = tempQuery.split("&")
		for temptempQuery in temptempQueries:
			temptemptempKey = temptempQuery.split("=")[0] # 其中一个参数的键
			temptemptempValue = temptempQuery.split("=")[1] # 其中一个参数的值
			queryResult[temptemptempKey] = temptemptempValue
		tempResult['value'] = queryResult
		result.append(tempResult)
	return result

def mergeSameQuery(links):
	# 合并具有相同的查询参数的相同文件
	results = []
	for link in links:
		tempResult = {}
		tempResult['url'] = link['url']
		SIGN = False
		for result in results:
			keysOfValueResult = []
			for res in result['value']:
				keysOfValueResult.append(res)
			keysOfValueLink = []
			for lin in link['value']:
				keysOfValueLink.append(lin)
			if link['url'] == result['url'] and keysOfValueLink == keysOfValueResult:
				SIGN = True
				break
		if SIGN:
			continue
		tempResult['value'] = link['value']
		results.append(tempResult)
	return results

def formateUrl(url):
	if not url.endswith("/"):
		url += "/"
	return url

def main():
	if len(sys.argv) != 2:
		print "Usage : \n\tpython " + sys.argv[0] + " [URL]"
		print "Example : \n\tpython " + sys.argv[0] + " \"http://www.jianshu.com/\""
	else:
		url = formateUrl(sys.argv[1])
		content = getContent(url)
		soup = BeautifulSoup(content, "html.parser")
		links = getAllLinks(soup)
		hrefs = getAllHerfs(links)
		links = hrefsFilter(hrefs, getSchemeDomainPort(url))
		for link in links:
			print link
		return links

if __name__ == "__main__":
    main()