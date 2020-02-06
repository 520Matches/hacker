# -*- coding: utf-8 -*-

import Queue
import threading
import os
import urllib2

threads = 10

target = "http://121.199.71.64:8080/Video"
#target = "http://www.baidu.com"

directory = "D:/data/tomcat/Video"

filters = [".jpg",".gif",".png",".css",".ini"]

print(os.getcwd())

os.chdir(directory)

print(os.getcwd())

web_paths = Queue.Queue()

for r,d,f in os.walk("."):
    for files in f:
        remote_path = "%s/%s" % (r,files)   
        remote_path = remote_path.replace('\\','/')
        if remote_path.startswith("."):
            remote_path = remote_path[1:]
        if os.path.splitext(files)[1] not in filters:                       
            web_paths.put(remote_path)
            
            
def test_remote():
    while not web_paths.empty():
        path = web_paths.get()
        url = "%s%s" % (target,path)
        
        print("url=%s" % url)
        
        request = urllib2.Request(url)
        
        try:
            response = urllib2.urlopen(request)
            content = response.read()
            
            print("[%d] => %s" % (response.code,path))
            
            response.close()
            
        except urllib2.HTTPError as error:
            print("Failed %s" % error.code)
            pass
            
for i in range(threads):
    print ("thread number:%d" % i)
    t = threading.Thread(target=test_remote)
    t.start()     