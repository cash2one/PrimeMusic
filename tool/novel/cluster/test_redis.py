#!/usr/bin/env python
# -*- coding:utf-8
# author: sunhaowen@baidu.com
# date: 14-1-12 下午4:31

import json
import redis
import time

def here():
    print("PrimeMusic")

def set_dir_info():
    dir_info = {
        "dir_url": "http://read.qidian.com/BookReader/3013862.aspx",
        "book_name": "斗破苍穹",
        "pen_name": "天蚕土豆",
        "chapter_list": []
    }
    for chapter_index in xrange(0, 100):
        chapter = {}
        chapter["chapter_index"] = chapter_index
        chapter["chapter_title"] = "第一章 世俗的圆满，守拙的幸福"
        chapter["chapter_url"] = "http://www.douban.com/note/2289922/"
        dir_info["chapter_list"].append(chapter)

    value = json.dumps(dir_info)

    start_time = time.time()
    redis_client = redis.Redis(host = "10.92.58.49", port = 6379)
    for key in xrange(0, 10000000):
        redis_client.set("%d" % key, value)

    print(time.time() - start_time)

if __name__ == '__main__':
    set_dir_info()