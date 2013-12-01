#!/usr/bin/env python
# -*- coding:GBK
# author: sunhaowen@baidu.com
# date: 2013/07/16 11:16

import threading
import requests
import logging
import time
import json
import MySQLdb

def here():
    print("PrimeMusic")

def send_get_requests(url):
    try :
        result = requests.get(url).json()
    except Exception, e :
        return False
    return result

def check_guhua_dir(url) :
    result = send_get_requests(url)
    if result is False :
        return False
    if result.has_key("error_code") :
        return False
    return True

if __name__ == "__main__":

    conn = MySQLdb.connect(
        host = "10.46.7.172",
        port = 4195,
        user = "wise_novelfmt_w",
        passwd = "H4k3D8v9X2y5",
        db = "novels")
    gid_list = []

    """
    sql = "SELECT gid, book_name, pen_name, dir_url FROM novel_authority_dir_info"
    cursor = conn.cursor()
    cursor.execute(sql)
    for (gid, book_name, pen_name, dir_url) in cursor.fetchall():
        gid_list.append((gid, book_name, pen_name, dir_url))
    cursor.close()
    """

    book_name_list = open("./book_name.txt", "r").readlines()
    for book_name in book_name_list:
        sql = "SELECT gid, book_name, pen_name, dir_url FROM novel_authority_dir_info WHERE book_name = '%s' LIMIT 1" % (book_name.strip())
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        if result:
            (gid, book_name, pen_name, dir_url) = result
            gid_list.append((gid, book_name, pen_name, dir_url))
        else:
            print(book_name.strip())
        cursor.close()
    guhua_count = 0
    for (gid, book_name, pen_name, dir_url) in gid_list:
        url = "http://m.baidu.com/open/novel/novel/dirurl/gid?lcid=mco_ds&query=" + str(gid)
        print(url)
        if check_guhua_dir(url):
            guhua_count += 1
        else:
            print("%d %s %s %s" % (gid, book_name, pen_name, dir_url))

    print(guhua_count, len(gid_list))

