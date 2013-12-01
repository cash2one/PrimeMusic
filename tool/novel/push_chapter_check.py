#!/usr/bin/env python
# -*- coding:GBK
# author: sunhaowen@baidu.com
# date: 13-11-11 下午9:20

import MySQLdb
import hashlib

def here():
    print("PrimeMusic")

def get_chapter_id_list(dir_id_list):
    """
    """
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

    chapter_id_list = []
    for (site_id, dir_id, dir_url) in dir_id_list:
        if site_id % 2 == 0:
            cursor = conn_even.cursor()
        else:
            cursor = conn_odd.cursor()
        sql = "SELECT chapter_id, chapter_url, chapter_status FROM chapter_ori_info%d WHERE dir_id = %d" % (site_id, dir_id)
        cursor.execute(sql)
        for (chapter_id, chapter_url, chapter_status) in cursor.fetchall():
            if chapter_status != 0:
                chapter_id_list.append((site_id, chapter_id, chapter_url, chapter_status))
        cursor.close()
    return chapter_id_list

if __name__ == '__main__':

    conn = MySQLdb.connect(
        host = "10.46.7.171",
        port = 4198,
        user = "wise_novelclu_w",
        passwd = "C9l3U4n6M2e1",
        db = "novels_new")

    none_authority_dir_list = []
    for line in open("./gid", "r").readlines():
        gid, book_name = line.strip().split()
        none_authority_dir_list.append((gid, book_name))

    dir_id_list = []
    for (gid, book_name) in none_authority_dir_list:
        m = hashlib.md5()
        m.update(book_name)
        table_id = int(m.hexdigest(), 16) % 256

        sql = "SELECT site_id, dir_id, dir_url FROM novel_cluster_info%d WHERE cluster_id = %d" % (table_id, gid)
        cursor = conn.cursor()
        cursor.execute(sql)
        for (site_id, dir_id, dir_url) in cursor.fetchall():
            dir_id_list.append((site_id, dir_id, dir_url))
        cursor.close()

    chapter_id_list = get_chapter_id_list()


    here()