#!/usr/bin/env python
# -*- coding:GBK
# author: sunhaowen@baidu.com
# date: 2013/07/15 21:28

import hashlib

def here():
    print("PrimeMusic")

if __name__ == "__main__":
    book_name = "大主宰"
    m = hashlib.md5()
    m.update(book_name)
    table_id = int(m.hexdigest(), 16) % 256
    print(table_id)