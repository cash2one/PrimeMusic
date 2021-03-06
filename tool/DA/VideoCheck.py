#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-12-23 18:24'

import requests
import logging
import json
import time
import threading


def here():
    print('PrimeMusic')


logger = logging.getLogger("test")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


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


def get_json_result(src):
    """
    :param src:
    :return:
    """
    try:
        result = requests.get(src).json()
    except Exception, e:
        return False
    return result


def video_topic_check(word):
    """
    :param word:
    :return:
    """
    src = 'http://app.video.baidu.com/app?md=android&ct=905969664&word={0}&ie=utf-8&jsonFn=videoJson&pn=0&rn=18&s=1&mtj_cuid=BE4C7DF73D04A81C9A88E022C34769B7%7C68220915083635&version=5.3.0'.format(word)
    result = get_json_result(src)
    if not result:
        logger.info('word: {0}, error: {1}'.format(word, 'not get json'))
        return False

    if not result.has_key('sResult'):
        logger.info('word: {0}, error: {1}'.format(word, 'not get sResult'))
        return False
    s_result = result['sResult']

    if not s_result.has_key('topicjson'):
        logger.info('word: {0}, error: {1}'.format(word, 'not get topicjson'))
        return False
    if not len(s_result['topicjson']):
        logger.info('word: {0}, error: {1}'.format(word, 'not get topicjson'))
        return False
    topic_json = s_result['topicjson'][0]
    title = topic_json['title']
    intro = topic_json['intro']
    logger.info('word: {0}, title: {1}, intro: {2}'.format(word, title.encode('GBK'), intro.encode('GBK')))
    return True


if __name__ == '__main__':

    query_list = [line.strip() for line in open('./query.txt', 'r').readlines()]

    frequency = 20
    main_thread = threading.currentThread()
    for index, query in enumerate(query_list):
        check_thread = threading.Thread(name=index, target=video_topic_check, args=(query, ))
        check_thread.start()

        logger.info('threading number: {0}'.format(threading.active_count()))
        if threading.active_count() > frequency:
            time.sleep(1.0)

    for t in threading.enumerate() :
        if t is main_thread :
            continue
        t.join()
    here()







