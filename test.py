#!/usr/bin/env python
# -*- coding:GBK
# author: sunhaowen@baidu.com
# date: 2013/07/15 21:28

from urlparse import urlparse

def here():
    print("PrimeMusic")


if __name__ == "__main__":
    parsed_uri = urlparse( 'http://stackoverflow.com/questions/1234567/blah-blah-blah-blah' )
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    domain = parsed_uri.netloc
    print domain
    here()