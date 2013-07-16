#!/usr/bin/env python
# -*- coding:GBK
# author: sunhaowen@baidu.com
# date: 2013/07/16 11:16

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


prefix = "http://m.baidu.com/open/dataservice/novel/chapter/url?lcid=mco_ds&replace=1&nocache=1&query="
def get_chapter_replace(index, url, error_count) :
    result = send_get_requests(prefix + url)

    if result is False or type(result) == type({}) :
        error_count.increment()
        logger.debug("%d error %s %s" % (index, result["error_code"], raw_url))
        return False

    logger.debug("%d right %s" % (index, " ".join("%s" % dir["url"] for dir in result)))
    return True


if __name__ == "__main__":

    raw_url_list = open("./url", "r").read().splitlines()
    error_count = counter()
    frequency = 5
    for index, raw_url in enumerate(raw_url_list) :
        get_request = threading.Thread(name=index, target=send_get_requests, args=(index, raw_url, error_count))
        get_request.start()
        if index % frequency == 0 :
            time.sleep(1.0)

    main_thread = threading.currentThread()
    for t in threading.enumerate() :
        if t is main_thread :
            continue
        t.join()

    print(error_count.value, len(raw_url_list))
