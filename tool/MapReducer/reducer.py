#!/usr/bin/env python
# -*- coding:utf-8

__author__ = 'sunhaowen'
__date__ = '2015-01-26 18:05'


import sys
from collections import defaultdict

def here():
    print('PrimeMusic')


def Reducer():
    """
    :return:
    """
    current_domain = None
    current_domain_query_dict = {}

    for line in sys.stdin:
        line = line.strip()
        (domain, query, satisfy_count) = line.split('\t')

        if current_domain == domain:
            current_domain_query_dict[query] = True
        else:
            if current_domain is not None:
                print('{0}\t{1}'.format(current_domain, len(current_domain_query_dict)))
            current_domain = domain
            current_domain_query_dict = {}

    if current_domain is not None:
        print('{0}\t{1}'.format(current_domain, len(current_domain_query_dict)))


if __name__ == '__main__':
    Reducer()