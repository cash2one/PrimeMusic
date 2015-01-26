#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2015-01-23 10:51'

import sys

def here():
    print('PrimeMusic')


def Mapper():
    """
    :return:
    """
    for line in sys.stdin:
        line = line.decode('utf-8', 'ignore')
        line = line.strip()
        (query, total_search_count, total_click_count, total_satisfy_count, total_url_info) = line.split('\t', 4)

        while len(total_url_info):
            single_url_info_list = total_url_info.split('\t', 18)
            if len(single_url_info_list) < 18:
                continue
            if len(single_url_info_list) == 18:
                total_url_info = single_url_info_list[-1]
            else:
                total_url_info = ''
            url = single_url_info_list[0]
            title = single_url_info_list[1]
            search_count = int(single_url_info_list[2])
            click_count = int(single_url_info_list[5])
            satisfy_count = int(float(single_url_info_list[6]))

            print('{0}\t{1}\t{2}\t{3}\t{4}\t{5}'.format(
                query.encode('GBK', 'ignore'),
                url.encode('GBK', 'ignore'),
                title.encode('GBK', 'ignore'),
                search_count,
                click_count,
                satisfy_count
            ))


if __name__ == '__main__':
    here()    







