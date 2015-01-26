#!/usr/bin/env python
# -*- coding:GBK
# author: sunhaowen@baidu.com
# date: 2013/07/15 21:28

from urlparse import urlparse

def here():
    print("PrimeMusic")


if __name__ == "__main__":
    a = {'a': 1, 'b': 2, 'c': 5, 'd': 3}
    print(len(a))
    b = sorted(a.items(), key = lambda x: x[1], reverse=True)
    print(b)
    here()