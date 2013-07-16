#!/usr/bin/env python
# -*- coding:GBK
# author: sunhaowen@baidu.com
# date: 2013/07/16 11:16

import threading
import requests
import logging
import time
import json

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s', )

def here():
    print("PrimeMusic")

class counter(object) :
    def __int__(self, start = 0):
        self.lock = threading.Lock()
        self.value = start

    def increment(self):
        self.lock.acquire()
        try:
            self.value += 1
        finally:
            self.lock.release()

prefix_url = "http://m.baidu.com/open/dataservice/novel/chapter/url?lcid=mco_ds&replace=1&nocache=1&query="
def send_get_requests(index, raw_url, error_count) :
    url = prefix_url + raw_url
    try:
        result = requests.get(url)
        result_list = result.json()
    except Exception, e :
        error_count.increment()
        logging.debug("%d error %s %s" % (index, e, raw_url))
        return False

    if type(result_list) == type({}) :
        error_count.increment()
        logging.debug("%d error %s %s" % (index, result_list["error_code"], raw_url))
        return False

    logging.debug("%d right %s" % (index, " ".join("%s" % dir["url"] for dir in result_list)))
    return True


if __name__ == "__main__":

    raw_url_list = open("./url", "r").read().splitlines()
    error_count = counter()
    frequency = 5
    for index, raw_url in enumerate(raw_url_list) :
        get_request = threading.Thread(name=index, target=send_get_requests, args=(index, raw_url, error_count))
        if index % frequency == 0 :
            time.sleep(1.0)

    main_thread = threading.currentThread()
    for t in threading.enumerate() :
        if t is main_thread :
            continue
        t.join()