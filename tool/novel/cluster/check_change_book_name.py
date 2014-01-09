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
              "LIMIT 10000"
        cursor.execute(sql)
        for (dir_id, dir_url, rid) in cursor.fetchall():
            dir_id_list.append((dir_id, dir_url, rid))
    cursor.close()

    file_handler = open("./dir_id_list.txt", "w")
    for (dir_id, dir_url, rid) in dir_id_list:
        file_handler.write("%d  %s  %d\n" % (dir_id, dir_url, rid))
    file_handler.close()

if __name__ == '__main__':
    here()