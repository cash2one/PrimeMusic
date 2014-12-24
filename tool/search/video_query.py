#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-12-23 18:24'

import requests
import json

def here():
    print('PrimeMusic')


def check_query(word):
    """
    :param word:
    :return:
    """
    src = 'https://m.baidu.com/s?word={0}'.format(word)
    r = requests.get()


if __name__ == '__main__':
    here()    







