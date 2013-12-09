#!/usr/bin/env python
# -*- coding:utf-8
# author: sunhaowen@baidu.com
# date: 13-11-27

from bs4 import BeautifulSoup
import pymongo
import sys

def here():
    print("PrimeMusic")

class Word(object):
    """
    """
    def __init__(self):
        """
        """
        self.word = ""
        self.meaning_list = []
    
    def extract_word(self, node):
        """
        """
        self.word = node.get_text().strip()

    def extract_meaning_list(self, node):
        """
        """
        for p in node.find_all("p"):
            text = p.get_text().strip()
            self.meaning_list.append(text)
        
    def pack(self):
        """
        """
        word_document = {}
        word_document["word"] = "".join(self.word.encode("utf-8", "ignore").splitlines())
        word_document["meaning_list"] = []
        for raw_meaning in self.meaning_list:
            meaning = "".join(raw_meaning.encode("utf-8", "ignore").splitlines())
            word_document["meaning_list"].append(meaning)
        return word_document
        
    def show(self):
        """
        """
        word = "".join(self.word.encode("utf-8", "ignore").splitlines())
        print(word)
        for raw_meaning in self.meaning_list:
            meaning = "".join(raw_meaning.encode("utf-8", "ignore").splitlines())
            print(meaning)

        
class WordGroup(object):
    """
    """
    def __init__(self):
        """
        """
        self.meaning = ""
        self.word_list = []
        self.paraphrase = ""
        
    def extract_meaning(self, node): 
        """
        """
        self.meaning = node.get_text().strip()

    def extract_word(self, node_left, node_right):
        """
        """
        word = Word()
        word.extract_word(node_left)
        word.extract_meaning_list(node_right)
        self.word_list.append(word)

    def extract_paraphrase(self, node):
        """
        """
        self.paraphrase = node.get_text().strip()
    
    def pack(self):
        """
        """
        group_document = {}
        group_document["meaning"] = "".join(self.meaning.encode("utf-8", "ignore").splitlines())
        group_document["paraphrase"] = "".join(self.paraphrase.encode("utf-8", "ignore").splitlines())
        group_document["word_list"] = []
        for word in self.word_list:
            group_document["word_list"].append(word.pack())
        return group_document
        
    def show(self):
        """
        """
        meaning = "".join(self.meaning.encode("utf-8", "ignore").splitlines())
        print(meaning)
        paraphrase = "".join(self.paraphrase.encode("utf-8", "ignore").splitlines())
        print(paraphrase)
        for word in self.word_list:
            word.show()
    

class DB(object):
    """
    """
    def __init__(self):
        self.mongo_client = pymongo.MongoClient("10.26.186.33", 8897)
    
    def write_db(self, name, word_group_list):
        """
        """
        db = self.mongo_client["sunhaowen"]
        collection = db["word_group"]
        for index, word_group in enumerate(word_group_list):
            document = word_group.pack()
            document["name"] = name
            document["arg"] = "%s@%d" % (name, index)
            try:
                data = collection.find_one({"arg": document["arg"]})
                if data:
                    response = collection.update({"arg": document["arg"]}, document)
                else:
                    response = collection.insert(document)
            except Exception, e:
                print("update into mongo error [error: %s]" % e)
                continue
    
        
if __name__ == '__main__':
    
    if len(sys.argv)!= 2:
        print("need a html file")
        exit()

    name = sys.argv[1]
    
    html = open("./%s.html" % name, "r").read()
    html = html.decode("gbk", "ignore")
    html = html.encode("utf-8", "ignore")
    soup = BeautifulSoup(html)
    print(soup.original_encoding)
    
    word_group_list = []

    for table in soup.find_all("table"):
        word_group = WordGroup()

        flag = False   
        for tr in table.find_all("tr"):
            td_list = tr.find_all("td")

            if len(td_list) == 1:
                word_group.extract_paraphrase(td_list[0])
                continue
            if len(td_list) == 3 and flag == False:
                word_group.extract_meaning(td_list[0])
                word_group.extract_word(td_list[1], td_list[2])
                flag = True
                continue
            if len(td_list) >= 2:
                word_group.extract_word(td_list[len(td_list) - 2], td_list[len(td_list) - 1])
                continue
        if flag == True:
            word_group_list.append(word_group)

        word_group.show()
        #print(word_group.pack())
    
    db = DB()
    db.write_db(name, word_group_list)


