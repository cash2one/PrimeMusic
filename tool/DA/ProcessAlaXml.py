#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2015-01-13 16:17'


import requests
from xml.etree import ElementTree

def here():
    print('PrimeMusic')


def get_xml_key_list(src):
    """
    """
    try:
        response = requests.get(src)
        tree = ElementTree.fromstring(response.content)
        print('src: {0}'.format(src))
    except Exception, e:
        return []

    key_list = []
    for item in tree.iter('item'):
        key = item.find('key').text
        if len(key):
            key_list.append(key)
    return key_list


def process_single_site(src):
    """
    """
    try:
        response = requests.get(src)
        tree = ElementTree.fromstring(response.content)
        print('src: {0}'.format(src))
    except Exception, e:
        return []

    key_list = []
    if tree.tag == 'DOCUMENT':
        key_list = get_xml_key_list(src)
        return key_list

    for sitemap in tree.iter('sitemap'):
        loc = sitemap.find('loc').text
        key_list.extend(get_xml_key_list(loc))
    return key_list


if __name__ == '__main__':

    source_list = [
        (20426, 'http://yf-imps-bs07-09.yf01.baidu.com:8888/index.xml'),
        (16325, 'http://cq02-mco-wise-build00.cq02.baidu.com:8091/xml_build/jiajintao/people_zhixin/people.xml'),
        (11198, 'http://ald.app111.com/precise_strong.xml'),
        (11235, 'http://ald.app111.com/addressing.xml'),
        (12064, 'http://ald.app111.com/function_weak.xml'),
        (11312, 'http://ald.app111.com/function_strong.xml')
    ]
    for (srcid, src) in source_list:
        print('srcid: {0}, src: {1}'.format(srcid, src))
        result = process_single_site(src)
        file = open('./{0}.txt'.format(srcid), 'w')
        for key in result:
            try:
                key = key.encode('GBK')
            except Exception, e:
                continue
            file.write('{0}\n'.format(key.encode('GBK')))
        file.close()
