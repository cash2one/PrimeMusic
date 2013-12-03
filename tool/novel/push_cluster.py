#!/usr/bin/env python
# -*- coding:GBK
# author: sunhaowen@baidu.com
# date: 13-11-28 下午4:51

import MySQLdb

def here():
    print("PrimeMusic")

def get_dir_id_list(book_name):
    conn = MySQLdb.connect(
        host = "10.46.7.172",
        port = 4195,
        user = "wise_novelfmt_w",
        passwd = "H4k3D8v9X2y5",
        db = "novels")
    cursor = conn.cursor()

    result_list = []
    for site_id in xrange(0, 178):
        sql = "SELECT dir_id FROM dir_fmt_info%d WHERE book_name = '%s'" % (site_id, book_name)
        cursor.execute(sql)
        for (dir_id, ) in cursor.fetchall():
            result_list.append((dir_id, site_id))

    cursor.close()
    conn.close()
    return result_list

def check_dir_id_list(dir_id_list):
    conn = MySQLdb.connect(
        host = "10.46.7.171",
        port = 4198,
        user = "wise_novelclu_w",
        passwd = "C9l3U4n6M2e1",
        db = "novels_new")
    cursor = conn.cursor()

    result_list = []
    for (dir_id, site_id) in dir_id_list:
        sql = "SELECT rid FROM dir_rid_info%d WHERE dir_id = %d" % (dir_id % 10, dir_id)
        cursor.execute(sql)
        result = cursor.fetchone()
        if not result:
            result_list.append(dir_id, site_id)
    cursor.close()
    conn.close()
    return result_list

if __name__ == '__main__':

    book_name_list = open("book_name.txt", "r").readlines()
    sql_list_odd = []
    sql_list_even = []
    for book_name in book_name_list:
        dir_id_list = get_dir_id_list(book_name.strip())
        result_list = check_dir_id_list(dir_id_list)
        for (dir_id, site_id) in result_list:
            sql = "UPDATE dir_ori_info%d SET update_time = unix_timestamp() WHERE dir_id = %d;" % (site_id, dir_id)
            if site_id % 2 == 0:
                sql_list_even.append(sql)
            else:
                sql_list_odd.append(sql)

    for sql in sql_list_even:
        print(sql)
    for sql in sql_list_odd:
        print(sql)

