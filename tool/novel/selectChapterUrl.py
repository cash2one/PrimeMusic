#!/usr/bin/env python
# -*- coding:GBK
# author: sunhaowen@baidu.com
# date: 2013/07/16 20:18

import re
import sign
import MySQLdb
import urlparse
import hashlib

def here():
    print("PrimeMusic")

if __name__ == "__main__":
    site_list = ["dawenxue.net", "sohu.com", "null", "zhulang.com", "fbook.net", "xstxw.com", "xs8.cn", "sina.com.cn", "readnovel.com", "qdmm.com", "null", "laishu.com", "8535.org", "cuiweiju.com", "jjwxc.net", "shenmaxiaoshuo.com", "null", "52blgl.com", "xs52.com", "xiazailou.com", "baishuku.com", "null", "cnd1wx.com", "vodtw.com", "gosky.net", "89wx.com", "qbxs8.com", "null", "qidian.com", "yankuai.com", "yqhhy.cc", "nilongdao.com", "77shu.com", "txtbbs.com", "wm263.com", "xiaoyanwenxue.com", "tianyibook.com", "mpzw.com", "71wx.net", "tianyabook.com", "92txt.net", "93zw.com", "didaxs.com", "doulaidu.com", "kenwen.com", "feiku.com", "fmx.cn", "langlangshu.com", "shuoshuo520.com", "null", "kanshuge.com", "ya55.com", "79wx.net", "tianya.cn", "zhaishu.com", "bookzx.net", "saesky.net", "shukeju.com", "qingfo.com", "book108.com", "paoshu8.com", "null", "zzzcn.com", "nv001.cn", "6ycn.com", "qq.com", "sfacg.com", "null", "llwx.net", "88106.com", "null", "lingdiankanshu.com", "icmfgs.com", "kanxuanhuan.com", "hongshu.com", "bokon.net", "hszw.com", "duduwo.com", "hlj3.com", "null", "null", "dushuge.net", "null", "null", "cc222.com", "bxwx.org", "bookbao.com", "binhuo.com", "92zw.com", "92to.com", "87zw.com", "66721.com", "59to.com", "null", "4xiaoshuo.com", "21zw.net", "123du.net", "dudu8.net", "null", "zongheng.com", "yl22.com", "xiaoshuoshu.org", "xiaoshuoxiu.com", "zwwx.com", "7zbook.com", "xxsy.net", "17k.com", "null", "tom.com", "epzw.com", "luoqiu.com", "mingshulou.com", "qingxinwang.com", "hongxiu.com", "null", "null", "null", "3gsc.com.cn", "null", "null", "null", "fqxsw.com", "kewaishu.net", "niubb.net", "guanhuaju.com", "bxzw.com", "jdxs.net", "ha18.com", "d5wx.com", "dashubao.com", "7kankan.com", "d3zw.com", "cilook.cn", "5i33.com", "wanshulou.com", "shanwen.com", "null", "readwx.com", "hxtk.com", "wenxuedu.com", "yawen8.com", "null", "null", "shuqi.com", "xdyqw.com", "faloo.com", "2100book.com", "kanshu.com", "1001p.com", "wjsw.com", "qdwenxue.com", "24novel.com", "uczw.com", "null", "mtfcn.com", "99reader.cn", "aiyun.com", "yxgsk.com", "dzxsw.net", "wuxia.net.cn", "null", "null", "mmzh.com", "xxs8.com", "tadu.com", "null", "huanxia.com", "yuanchuang.com", "motie.com", "qefeng.com", "docin.net", "siluke.com", "quanben.com", "xiaoshuo555.cn", "shouda8.com", "nieshu.com", "zhuzhudao.com", "xshuotxt.com"]
    url_list = open("./url", "r").read().splitlines()

    conn_even = MySQLdb.connect(
        host = "10.46.7.173",
        port = 4170,
        user = "wise_novelori_w",
        passwd = "K3i8T5h1N2o9",
        db = "novels")
    conn_odd = MySQLdb.connect(
        host = "10.46.7.174",
        port = 4171,
        user = "wise_novelori_w",
        passwd = "K3i8T5h1N2o9",
        db = "novels")

    conn = MySQLdb.connect(
        host = "10.46.7.172",
        port = 4195,
        user = "wise_novelfmt_w",
        passwd = "H4k3D8v9X2y5",
        db = "novels")

    chapter_info_list = []
    for url in url_list :
        host = urlparse.urlsplit(url).hostname
        site_id = -1
        for index, site in enumerate(site_list) :
            match = re.search(site, host)
            if match is None :
                continue
            else :
                site_id = index
                break
        if site_id == -1 :
            continue
        if site_id % 2 == 0 :
            cursor = conn_even.cursor()
        else :
            cursor = conn_odd.cursor()

        sign_result = sign.fs64(url)
        key1 = sign_result[1]
        key2 = sign_result[2]
        chapter_id = int(key1<<32) + key2

        sql = "SELECT dir_id, dir_url, chapter_id, chapter_url FROM chapter_ori_info%d WHERE chapter_id = %d" % (site_id, chapter_id)
        try :
            cursor.execute(sql)
        except Exception, e :
            print("[sql: %s, error: %s]" % (sql, e))

        res = cursor.fetchone()
        cursor.close()
        if res is None :
            continue
        (dir_id, dir_url, chapter_id, chapter_url) = res
        chapter_info_list.append((site_id, dir_id, dir_url, chapter_id, chapter_url))

    for (site_id, dir_id, dir_url, chapter_id, chapter_url) in chapter_info_list :
        sql = "SELECT book_name FROM dir_fmt_info%d WHERE dir_id = %d" % (site_id, dir_id)
        try :
            cursor = conn.cursor()
            cursor.execute(sql)
        except Exception, e :
            print("[sql: %s, error: %s]" % (sql, e))

        res = cursor.fetchone()
        cursor.close()
        if res is None :
            continue
        book_name = res[0]
        m = hashlib.md5()
        m.update(book_name)
        table_id = int(m.hexdigest(), 16) % 256

        print(table_id, chapter_id, chapter_url)

