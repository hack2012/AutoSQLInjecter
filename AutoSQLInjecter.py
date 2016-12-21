#!/usr/bin/env python
#encoding:utf8

import requests
import sys
import urlparse
from bs4 import BeautifulSoup

# from optparse import OptionParser
# def main():
# 	parser = OptionParser()
# 	parser.add_option("-u", dest="url",help="The destation url for attack")
# 	(options, args) = parser.parse_args()
# 	if len(args) != 0:
# 	    parser.error("incorrect number of arguments")  
# 	if options.url:

# url = sys.argv[1]
url = "http://127.0.0.1/"
url = "http://gxxnr.cn/"
url = "http://www.cnblogs.com/qq78292959/archive/2013/04/07/3005763.html"
# parsedUrl = urlparse(url_str)

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
	print links
	print "---------------"
	# links = getAllSameFatherDomainLinks(links)
	# print links
	print "---------------"
	links = getAllSameSourceLinks(links)
	print links
	print "---------------"
	# 这个时候可以去写爬虫去判断
	# links = getAllQueryLinks(links)
	# return links


def getAllQueryLinks(links):
	tempLinks = set()
	for link in links:
		if "?" in link:
			tempLinks.add(link)
	return tempLinks

def main():
	content = getContent(url)
	soup = BeautifulSoup(content, "html.parser")
	links = getAllLinks(soup)
	hrefs = getAllHerfs(links)
	links = hrefsFilter(hrefs, getSchemeDomainPort(url))
	print links

if __name__ == "__main__":
    main()