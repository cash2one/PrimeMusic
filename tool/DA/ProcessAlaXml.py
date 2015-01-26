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
        if not item.find('key'):
            continue
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
        if sitemap.find('loc') is None:
            continue
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
        (11312, 'http://ald.app111.com/function_strong.xml'),
        (19283, 'http://cq02-mco-wise-build00.cq02.baidu.com:8091/xml_build/zhangliuhui/aladdin_data/output_weather/weather.xml'),
        (10083, 'http://baidudata.weather.com.cn:8080/baiduDataInterface/getbaidugaoduanchinaweatherkey'),
        (13295, 'http://jingyan.baidu.com/z/weijin/aladin_wise_all_index_0.xml'),
        (15910, 'http://jingyan.baidu.com/z/weijin/aladin_wise_all_index_1.xml'),
        (14681, 'http://jingyan.baidu.com/z/weijin/aladin_wise_all_index_2.xml'),
        (15252, 'http://www.douguo.com/upload/xml/baidu/mobile_recipe_sitemap.xml'),
        (10389, 'http://www.douguo.com/upload/xml/baidu/mobile_shicaixml.xml'),
        (14287, 'http://gubaf10.eastmoney.com/html/forbaidu_5.xml'),
        (15921, 'http://nj02-nlp-dqa-test08.nj02.baidu.com:8080/wise_aladin_generalyesno/generate_xml_file/output/new_kv/index.xml'),
        (11736, 'http://ext.tvmao.com/data/baidu/baidu_drama_wap_2.xml'),
        (13676, 'http://s.imanhua.com/open/m1.xml')
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
            file.write('{0}\n'.format(key))
        file.close()
