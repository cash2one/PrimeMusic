#!/usr/bin/env python
# -*- coding:GBK
# author: sunhaowen@baidu.com
# date: 2013/07/17 16:28

import threading
import requests
import logging
import time
import json


logger = logging.getLogger("work")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

def here():
    print("PrimeMusic")

class counter(object) :
    def __init__(self, start = 0):
        self.lock = threading.Lock()
        self.value = start

    def increment(self):
        self.lock.acquire()
        try:
            self.value += 1
        finally:
            self.lock.release()


def send_get_requests(url):
    try :
        result = requests.get(url).json()
    except Exception, e :
        return False
    return result


prefix = "http://tc-wise-rdtf04.tc.baidu.com:8381/webapp?m=8&structpage=1&siteappid=376409&nocache=1&onlyspdebug=1&src="
def get_chapter(index, url_list, error_count) :
    flag = False
    for url in url_list :
        result = send_get_requests(prefix + url)
        if result is False :
            continue
        if result.has_key("page_type") :
            page_type = result["page_type"]
        else :
            continue
        if result.has_key("tpl_version") :
            tpl_version = result["tpl_version"]
        else :
            continue
        if page_type == "PAGE_TYPE_NOVEL_CONTENT" and tpl_version == 0 :
            flag = True
            logger.debug("%d right %s" % (index, url))
            break
    if flag is False :
        error_count.increment()
        logger.debug("%d error" % index)


if __name__ == "__main__":

    url_string_list = open("./right", "r").read().splitlines()
    error_count = counter()
    frequency = 5
    for index, url_string in enumerate(url_string_list) :
        url_list = url_string.split()
        get_request = threading.Thread(name=index, target=get_chapter, args=(index, url_list, error_count))
        get_request.start()
        if index % frequency == 0 :
            time.sleep(1.0)

    main_thread = threading.currentThread()
    for t in threading.enumerate() :
        if t is main_thread :
            continue
        t.join()

    print(error_count.value, len(url_string_list))
