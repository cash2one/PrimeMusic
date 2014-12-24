#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-12-24 17:27'


import MySQLdb
import requests


def here():
    print('PrimeMusic')


def change_check_status():
    """
    :return:
    """
    conn = MySQLdb.connect(
        host = "10.46.7.171",
        port = 4198,
        user = "novels_w",
        passwd = "qcbxQNKMTeyyy3b8",
        db = "novels")
    conn.set_character_set('GBK')
    conn.autocommit(True)

    sql = 'select book_id from novel_basic_info where save_content = 0 and public_status = 1'
    cursor = conn.cursor()
    cursor.execute(sql)
    book_id_list = cursor.fetchall()
    cursor.close()

    for (book_id, ) in book_id_list:
        print(book_id)
        id = book_id % 256
        sql = 'update novel_chapter_info{0} set check_status = 1 where book_id = {1}'.format(id, book_id)
        cursor = conn.cursor()
        cursor.execute(sql)
        cursor.close()

        src = 'http://tc.legal.wisenovel.baidu.com/legal/cache/clear/?type=chapter-list&book_id={0}'.format(book_id)
        requests.get(src)


if __name__ == '__main__':
    change_check_status()
    here()    







