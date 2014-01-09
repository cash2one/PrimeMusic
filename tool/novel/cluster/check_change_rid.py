#!/usr/bin/env python
# -*- coding:GBK
# author: sunhaowen@baidu.com
# date: 14-1-9 下午2:44

import MySQLdb

def here():
    print("PrimeMusic")

def get_dir_id_list():
    conn = MySQLdb.connect(
        host = "10.46.7.171",
        port = 4198,
        user = "wise_novelclu_w",
        passwd = "C9l3U4n6M2e1",
        db = "novels_new")
    cursor = conn.cursor()

    dir_id_list = []
    for table_id in xrange(0, 10):
        sql = "SELECT dir_id, dir_url, rid " \
              "FROM dir_rid_info%d " \
              "ORDER BY update_time DESC " \
              "LIMIT 10000" % table_id
        cursor.execute(sql)
        for (dir_id, dir_url, rid) in cursor.fetchall():
            dir_id_list.append((dir_id, dir_url, rid))
    cursor.close()
    conn.close()

    file_handler = open("./dir_id_list.txt", "w")
    for (dir_id, dir_url, rid) in dir_id_list:
        file_handler.write("%d  %s  %d\n" % (dir_id, dir_url, rid))
    file_handler.close()

def check_diff_rid():
    dir_id_list = []
    file_handler = open("./dir_id_list.txt", "r")
    for line in file_handler.readlines():
        (dir_id, dir_url, rid) = line.split()
        dir_id_list.append((dir_id, dir_url, rid))
    file_handler.close()

    conn = MySQLdb.connect(
        host = "10.46.7.171",
        port = 4198,
        user = "wise_novelclu_w",
        passwd = "C9l3U4n6M2e1",
        db = "novels_new")
    cursor = conn.cursor()

    diff_list = []
    for (dir_id, dir_url, rid) in dir_id_list:
        table_id = dir_id % 10
        sql = "SELECT rid FROM dir_rid_info%d WHERE dir_id = %d" % (table_id, dir_id)
        cursor.execute(sql)
        (new_rid, ) = cursor.fetchone()
        if rid != new_rid:
            diff_list.append((dir_id, dir_url, rid, new_rid))
    cursor.close()
    conn.close()

    file_handler = open("./diff_list.txt", "w")
    for (dir_id, dir_url, rid, new_rid) in diff_list:
        file_handler.write("%d  %s  %d  %d\n" % (dir_id, dir_url, rid, new_rid))
    file_handler.close()

if __name__ == '__main__':
    get_dir_id_list()
