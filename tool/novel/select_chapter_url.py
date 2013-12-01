#!/usr/bin/env python
# -*- coding:GBK
# author: sunhaowen@baidu.com
# date: 13-11-14 上午9:56

import MySQLdb

def here():
    print("PrimeMusic")

if __name__ == '__main__':

    conn_even = MySQLdb.connect(
        host = "10.46.7.173",
        port = 4170,
        user = "wise_novelori_w",
        passwd = "K3i8T5h1N2o9",
        db = "novels")

    conn_odd = MySQLdb.connect(
        host = "10.46.7.174",
        port = 4171,
        user = "wise_novelori_w",
        passwd = "K3i8T5h1N2o9",
        db = "novels")


    chapter_url_list = []
    for site_id in xrange(0, 178):
        if site_id % 2 == 0:
            cursor = conn_even.cursor()
        else:
            cursor = conn_odd.cursor()
        sql = "SELECT count(*) AS count FROM chapter_ori_info%d WHERE update_time > 1384099200" % site_id
        cursor.execute(sql)
        count = cursor.fetchone()[0]
        if count < 10000:
            continue
        print(site_id, count)
        sql = "SELECT chapter_url FROM chapter_ori_info%d WHERE chapter_status = 0 ORDER BY update_time DESC LIMIT 10" % site_id
        cursor.execute(sql)
        for (chapter_url, ) in cursor.fetchall():
            chapter_url_list.append(chapter_url)
        cursor.close()

    for chapter_url in chapter_url_list:
        print(chapter_url)