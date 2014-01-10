#!/usr/bin/env python
# -*- coding:GBK
# author: sunhaowen@baidu.com
# date: 14-1-10 下午2:44

import MySQLdb

def here():
    print("PrimeMusic")

def count_total_dir_id():
    conn = MySQLdb.connect(
        host = "10.46.7.172",
        port = 4195,
        user = "wise_novelfmt_w",
        passwd = "H4k3D8v9X2y5",
        db = "novels")
    cursor = conn.cursor()

    total_count = 0
    for table_id in xrange(0, 178):
        sql = "SELECT count(*) AS count FROM dir_fmt_info%d" % table_id
        cursor.execute(sql)
        (count, ) = cursor.fetchone()
        print(table_id, count)
        total_count += count
    print(total_count)


if __name__ == '__main__':
    count_total_dir_id()