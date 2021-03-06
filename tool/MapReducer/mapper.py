#!/usr/bin/env python
# -*- coding:utf-8

__author__ = 'sunhaowen'
__date__ = '2015-01-23 10:51'

import sys
from urlparse import urlparse
from collections import defaultdict

def here():
    print('PrimeMusic')


def Mapper(movie_name_dict):
    """
    :return:
    """
    for line in sys.stdin:
        line = line.strip()
        (query, total_search_count, total_click_count, total_satisfy_count, total_url_info) = line.split('\t', 4)
        if not movie_name_dict.has_key(query):
            continue

        domain_dict = defaultdict(int)
        while len(total_url_info):
            single_url_info_list = total_url_info.split('\t', 18)
            if len(single_url_info_list) < 18:
                break
            if len(single_url_info_list) == 19:
                total_url_info = single_url_info_list[-1]
            else:
                total_url_info = ''

            url = single_url_info_list[0]
            domain = urlparse(url).netloc
            title = single_url_info_list[1]
            search_count = int(single_url_info_list[2])
            click_count = int(single_url_info_list[5])
            satisfy_count = int(float(single_url_info_list[6]))

            if satisfy_count > 10:
                domain_dict[domain] += satisfy_count

        domain_list = sorted(domain_dict.items(), key = lambda x: x[1], reverse = True)
        current_satisfy = 0
        for (domain, satisfy_count) in domain_list:
            print('{0}\t{1}'.format(domain, query, satisfy_count))
            current_satisfy += satisfy_count
            if current_satisfy * 2 > total_satisfy_count:
                break


if __name__ == '__main__':
    movie_name_dict = {}
    for line in open('./MovieName.txt', 'r').readlines():
        movie_name = line.strip()
        movie_name_dict[movie_name] = 1

    Mapper(movie_name_dict)