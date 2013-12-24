#!/usr/bin/env python
# -*- coding:GBK
# author: sunhaowen@baidu.com
# date: 13-12-23 下午2:22

import os

if __name__ == '__main__':
    
    book_name_list = open('./book_name.txt', 'r').readlines()

    for index in xrange(10):
        
        if os.path.exists('./{0}'.format(index)):
            os.system('rm -rf {0}'.format(index))
            
        os.system('mkdir {0} && cp authority_chapter.py {0}'.format(index))

        file_handler = open('./{0}/book_name.txt'.format(index), 'w')
        for line in xrange(index * 100, (index + 1) * 100):
            file_handler.write('%s' % book_name_list[line])
        file_handler.close()


               
