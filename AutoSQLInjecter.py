#!/usr/bin/env python
# encoding:utf8

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

queryParameters = getQueryParameters("http://gxxnr.cn/")
injectableUrls = getAllInjectableUrls(queryParameters)

for injectableUrl in injectableUrls:
	print injectableUrl

