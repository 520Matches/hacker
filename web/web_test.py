# -*- coding: utf-8 -*-

import urllib2

url = "http://www.baidu.com"

headers = {}
headers['User-Agent'] = "Hacker_Test"
request = urllib2.Request(url,headers=headers)
response = urllib2.urlopen(request)

print(response.read())

response.close()