#!/usr/bin/env python
# -*- coding:GBK
# author: sunhaowen@baidu.com
# date: 14-1-9 下午5:54

import MySQLdb

def here():
    print("PrimeMusic")

def get_diff_book_name():
    gid_list = []
    for line in open("./gid.txt", "r").readlines():
        gid = line.strip()
        gid_list.append(int(gid))

    conn = MySQLdb.connect(
        host = "10.46.7.171",
        port = 4198,
        user = "wise_novelclu_w",
        passwd = "C9l3U4n6M2e1",
        db = "novels_new")
    cursor = conn.cursor()

    file_handler = open("./diff_book_name.txt", "w")
    for gid in gid_list:
        book_name_dict = {}
        for table_id in xrange(0, 256):
            sql = "SELECT book_name, pen_name, dir_url " \
                  "FROM novel_cluster_info%d " \
                  "WHERE cluster_id = %d" % (table_id, gid)
            cursor.execute(sql)
            for (book_name, pen_name, dir_url) in cursor.fetchall():
                if book_name_dict.has_key(book_name):
                    continue
                book_name_dict[book_name] = (pen_name, dir_url)
        if len(book_name_dict) <= 1:
            continue
        file_handler.write("%d\n" % gid)
        for (key, value) in book_name_dict.items():
            file_handler.write("%s  %s  %s" % (key, value[0], value[1]))
    file_handler.close()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    get_diff_book_name()