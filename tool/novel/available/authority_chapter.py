#!/usr/bin/env python
# -*- coding:GBK
# author: sunhaowen@baidu.com
# date: 13-12-23 下午2:22

import re
import json
import time
import urllib
import requests
import MySQLdb

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

class DataService(object):
    """
    """
    def get(self, gid):
        """
        """
        src = 'http://m.baidu.com/open/dataservice/novel/dirurl/gid?lcid=mco_ds&query=%d' % gid
        try:
            result = requests.get(src).json()
        except Exception, e:
            print('Failed to request dataservice, exception: {0}, src: {1}'.format(e, src))
            return False
        if result.has_key('error_code'):
            print('Failed to get data from dataservice, src: {0}'.format(src))
            return False

        cid_list = []
        for group in result['group']:
            href = group['href']
            cid = group['cid']
            cid_list.append((href, cid))
        return cid_list

class DB(object):
    """
    """
    def get(self, cid):
        """
        """
        conn = MySQLdb.connect(
            host = "10.46.7.171",
            port = 4198,
            user = "wise_novelclu_w",
            passwd = "C9l3U4n6M2e1",
            db = "novels_new")
        rid, align_id = map(int, cid.split('|'))
        table_id = rid % 256

        sql = "SELECT chapter_url " \
              "FROM integrate_chapter_info%d " \
              "WHERE rid = %d AND align_id = %d " \
              "ORDER BY chapter_rank DESC"\
              % (table_id, rid, align_id)
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
        except Exception, e:
            print('Faild to read chapter_url from DB, exception: {0}, sql: {1}'.format(e, sql))
            return False

        chapter_url_list = []
        for (chapter_url, ) in cursor.fetchall():
            chapter_url_list.append(chapter_url)

        cursor.close()
        conn.close()
        return chapter_url_list


if __name__ == '__main__':

    book_name_list = []
    for line in open('./book_name.txt', 'r').readlines():
        (gid, book_name) = line.split()
        book_name_list.append((int(gid), book_name))

    silkserver = SilkServer()
    silkserver.init()
    dataservice = DataService()
    db = DB()
    file_handler = open('./result.txt', 'w')
    for (gid, book_name) in book_name_list:
        file_handler.write('book_name: %s, gid: %d\n' % (book_name, gid))
        print('book_name: %s, gid: %d' % (book_name, gid))
        cid_list = dataservice.get(gid)
        if cid_list is False:
            continue

        print('chapter_num: %d' % len(cid_list))
        bad_cid_list = []
        for (href, cid) in cid_list:
            print('%s  %s' % (cid, href))
            result = silkserver.get(href, cid)
            if result is False:
                bad_cid_list.append(cid)
                continue
            if not result.has_key('blocks'):
                bad_cid_list.append(cid)
                continue
            data = ''
            for block in result['blocks']:
                if block['type'] == 'NOVELCONTENT':
                    data = block['data_value']
            data = re.sub('<[^>]*>', '', data).encode('GBK', 'ignore')
            print(len(data))
            if len(data) < 50:
                bad_cid_list.append(cid)

        print('bad_chapter_num: %d' % len(bad_cid_list))
        for cid in bad_cid_list:
            print(cid)
            file_handler.write('%s\n' % cid)
            chapter_url_list = db.get(cid)
            if chapter_url_list is False:
                continue
            flag = 0
            real_result = ''
            for chapter_url in chapter_url_list:
                result = silkserver.get(chapter_url)
                if result is False:
                    continue
                if not result.has_key('blocks'):
                    continue
                data = ''
                for block in result['blocks']:
                    if block['type'] == 'NOVELCONTENT':
                        data = block['data_value']
                data = re.sub('<[^>]*>', '', data).encode('GBK', 'ignore')
                if len(data) > 50:
                    print(data)
                    file_handler.write('%s\n' % data)
                    flag = 1
                    real_result = result
                    break
            if flag == 1:
                flag = silkserver.save(cid, real_result)
            if flag:
                print('OK')
                file_handler.write('OK\n')
            else:
                print('ERROR')
                file_handler.write('ERROR\n')

