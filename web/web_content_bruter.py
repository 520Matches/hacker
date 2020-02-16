# -*- coding: utf-8 -*-

import urllib2
import threading
import Queue
import urllib

threads = 10
target_url = "http://testphp.vulnweb.com"
wordlist_file = "/root/data/study/SVNDigger/all.txt"
resume = None
user_agent = "Firefox"

def build_wordlist(worldlist_file):
    fd = open(wordlist_file,"rb")
    raw_words = fd.readlines()
    fd.close()
    
    found_resume = False
    words = Queue.Queue()
    
    for word in raw_words:
        word = word.rstrip()
        
        if resume is not None:
            if found_resume:
                words.put(word)
            else:
                if word == resume:
                    found_resume = True
                    print "resuming wordlist form:%s" % resume
                    
        else:
            words.put(word)
            
    return words

def dir_bruter(word_queue,extensions=None):
    while not word_queue.empty():
        attempt = word_queue.get()
        attempt_list = []
        
        if "." not in attempt:
            attempt_list.append("/%s/" % attempt)
        else:
            attempt_list.append("/%s" % attempt)
            
        if extensions:
            for extension in extensions:
                attempt_list.append("/%s%s" % (attempt,extension))
                
        for brute in attempt_list:
            url = "%s%s" % (target_url,urllib.quote(brute))
            
            try:
                headers = {}
                headers["User-Agent"] = user_agent
                r = urllib2.Request(url,headers=headers)
                
                response = urllib2.urlopen(r)
                
                if len(response.read()):
                    print("[%d] => %s" % (response.code,url))
                    
            except urllib2.URLError,e:
                if hasattr(e,'code') and e.code != 404:
                    print("%d => %s" % (e.code,url))
                    
                pass
            
word_queue = build_wordlist(wordlist_file)
extensions = [".php",".bak",".html",".css",".inc",".orig"]

for i in range(threads):
    t = threading.Thread(target=dir_bruter,args=(word_queue,extensions,))
    t.start()
