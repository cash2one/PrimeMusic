#!/usr/bin/env python
# -*- coding:GBK
# author: sunhaowen@baidu.com
# date: 13-11-19 下午3:03

import MySQLdb
import hashlib

def here():
    print("PrimeMusic")

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
    for (book_name, gid) in none_authority_dir_list:
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

    none_authority_dir_list = []
    for line in open("./gid", "r").readlines():
        book_name, gid = line.strip().split()
        none_authority_dir_list.append((book_name, gid))

    generate_update_sql(none_authority_dir_list)

    here()