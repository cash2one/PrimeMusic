#!/usr/bin/env python
# -*- coding:GBK
# author: sunhaowen@baidu.com
# date: 2013/07/16 11:16

import threading
import time

def here():
    print("PrimeMusic")

def worker(index) :
    print("start : %d" % index)
    time.sleep(3)
    print("exit : %d" % index)


if __name__ == "__main__":

    test01 = threading.Thread(target=worker(01))
    test02 = threading.Thread(target=worker(02))
    test01.start()
    test02.start()
    here()