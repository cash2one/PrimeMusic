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
    srcid = 20426
    src = 'http://yf-imps-bs07-09.yf01.baidu.com:8888/index.xml'
    key_list = process_single_site(src)
    print('srcid: {0}, src: {1}'.format(srcid, src))
    for key in key_list:
        print(key)