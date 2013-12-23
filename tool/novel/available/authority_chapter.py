#!/usr/bin/env python
# -*- coding:GBK
# author: sunhaowen@baidu.com
# date: 13-12-23 下午2:22

import re
import json
import time
import urllib
import requests

def here():
    print("PrimeMusic")

class SilkServer():
    """
    """
    def init(self):
        self._pathPrefix = 'http://10.211.141.17:8851/webapp'
        self._timeout = 30
        self._defaultParam = {
            'structpage': 1,
            'siteappid' : 376409,
            'version' : 0,
            'platform' : 'other',
            'onlyspdebug' : 1,
            'srd' : 1
        }
        return True

    def get(self, src, pageid = None):
        param = {}
        param.update(self._defaultParam)
        if pageid != None :
            param['xs_pageid'] = pageid
        path = self._pathPrefix + '?' + urllib.urlencode(param) + '&' + urllib.urlencode({'src': src + '#reqtype=1'})
        header={'Host' : 'internal_wise_domain.baidu.com'}
        try:
            r = requests.get(path, headers = header, timeout = self._timeout)
            if r.status_code != requests.codes.ok:
                print("Failed to request silkserver.get, status_code:{0}, path:{1}".format(r.status_code, r.url));
                return False
            result = r.json()
            return result
        except Exception as e:
            print("Failed to request silkserver.get, exception:{0}".format(e));
            return False

    def save(self, pageid, data, expr = 315360000):
        data['page_expire_time'] = int(time.time()) + expr
        param = {}
        param.update(self._defaultParam)
        param['xs_pageid'] = pageid
        param['xs_pageexpiretime'] = int(time.time()) + expr
        path = self._pathPrefix + '?' + urllib.urlencode(param) + '&' + urllib.urlencode({'src': 'www.baidu.com'})
        try:
            str_data = json.dumps(data)
            header = {
                'content-type': 'application/json',
                'Host' : 'internal_wise_domain.baidu.com'
            }
            r = requests.post(path, data=str_data, headers=header)
            if r.status_code != requests.codes.ok:
                print("Failed to request silkserver.save, status_code:{0}, path:{1}".format(r.status_code, r.url));
                return False
        except Exception as e:
            print("Failed to request silkserver.save, exception:{0}, pageid:{1}".format(e, pageid));
            return False
        return True

class DataService():
    """
    """
    def init(self):
        """
        """

    def get(self, gid):
        """
        """
        src = 'http://m.baidu.com/open/dataservice/novel/dirurl/gid?lcid=mco_ds&query=%d' % gid
        try:
            result = requests.get(url).json()
            
    
if __name__ == '__main__':
    
    silkserver = SilkServer()
    silkserver.init()
    result = silkserver.get('http://www.shukeju.com/a/64/64526/9930741.html', '3961103225|5206658917899571812')
    if not result.has_key('blocks'):
        exit()
    data = ''
    for block in result['blocks']:
        if block['type'] == 'NOVELCONTENT':
            data = block['data_value']

    data = re.sub('<[^>]*>', '', data).encode('GBK', 'ignore')
    print(data)
    
