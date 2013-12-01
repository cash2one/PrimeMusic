#!/usr/bin/env python
# -*- coding:GBK
# author: sunhaowen@baidu.com
# date: 13-11-11 下午1:50

import MySQLdb
import hashlib

def here():
    print("PrimeMusic")


def check_authority_dir_list(authority_dir_list):
    """
    """
    conn = MySQLdb.connect(
        host = "10.46.7.171",
        port = 4198,
        user = "wise_novelclu_w",
        passwd = "C9l3U4n6M2e1",
        db = "novels_new")

    none_authority_dir_list = []
    for (gid, book_name, pen_name, dir_id, dir_url) in authority_dir_list:
        table_id = gid % 256
        sql = "SELECT count(*) as count FROM novel_authority_dir%d WHERE rid = %d" % (table_id, gid)
        cursor = conn.cursor()
        cursor.execute(sql)
        count = cursor.fetchone()[0]
        if count == 0:
            none_authority_dir_list.append((gid, book_name, pen_name, dir_id, dir_url))

    conn.close()
    return none_authority_dir_list


def generate_update_sql(none_authority_dir_list):
    """
    """
    conn = MySQLdb.connect(
        host = "10.46.7.171",
        port = 4198,
        user = "wise_novelclu_w",
        passwd = "C9l3U4n6M2e1",
        db = "novels_new")

    odd_sql_list = []
    even_sql_list = []
    for (gid, book_name, pen_name, dir_id, dir_url) in none_authority_dir_list:
        m = hashlib.md5()
        m.update(book_name)
        table_id = int(m.hexdigest(), 16) % 256
        sql = "SELECT site_id, dir_id FROM novel_cluster_info%d WHERE cluster_id = %d" % (table_id, gid)
        cursor = conn.cursor()
        cursor.execute(sql)
        for (site_id, dir_id) in cursor.fetchall():
            sql = "UPDATE IGNORE dir_ori_info%d SET update_time = unix_timestamp() WHERE dir_id = '%d';" % (site_id, dir_id)
            if site_id % 2 == 0:
                even_sql_list.append(sql)
            else:
                odd_sql_list.append(sql)
        cursor.close()
    conn.close()

    for sql in odd_sql_list:
        print(sql)
    for sql in even_sql_list:
        print(sql)


if __name__ == '__main__':

    conn = MySQLdb.connect(
        host = "10.46.7.172",
        port = 4195,
        user = "wise_novelfmt_w",
        passwd = "H4k3D8v9X2y5",
        db = "novels")

    authority_dir_list = []
    sql = "SELECT gid, book_name, pen_name, dir_id, dir_url FROM novel_authority_dir_info"
    cursor = conn.cursor()
    cursor.execute(sql)
    for (gid, book_name, pen_name, dir_id, dir_url) in cursor.fetchall():
        authority_dir_list.append((gid, book_name, pen_name, dir_id, dir_url))
    cursor.close()
    conn.close()
    none_authority_dir_list = check_authority_dir_list(authority_dir_list)
    for (gid, book_name, pen_name, dir_id, dir_url) in none_authority_dir_list:
        print("%d %s %s %d %s" % (gid, book_name, pen_name, dir_id, dir_url))
    for (gid, book_name, pen_name, dir_id, dir_url) in none_authority_dir_list:
        sql = "DELETE FROM novel_authority_dir_info WHERE gid = %d;" % gid
        print(sql)
    generate_update_sql(none_authority_dir_list)
