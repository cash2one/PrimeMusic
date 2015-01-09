#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2015-01-09 09:30'

import operator
from collections import defaultdict

def here():
    print('PrimeMusic')


def get_unique_top_query(file, number):
    """
    :param file:
    :param number:
    :return:
    """
    query_dict = defaultdict(int)
    for line in open(file, 'r').readlines():
        query = line.strip()
        query_dict[query] += 1

    query_list = sorted(query_dict.iteritems(), key=operator.itemgetter(1), reverse=True)
    for index, query_item in query_list:
        if index >= number:
            break
        print(query_item[1])


if __name__ == '__main__':
    get_unique_top_query('', 10000)
    here()







