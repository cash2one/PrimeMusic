#!/usr/bin/env python
# -*- coding:utf-8
# author: sunhaowen@baidu.com
# date: 13-11-27 ÉÏÎç12:01

from bs4 import BeautifulSoup
import pymongo

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
        self.name = "sunhaowen"
        self.mongo_client = pymongo.MongoClient("10.26.186.33", 27017)
    
    def write_db(self, word_group_list):
        """
        """

    
        
if __name__ == '__main__':
    
    html = open("./sunhaowen.htm", "r").read()
    soup = BeautifulSoup(html)
    
    word_group_list = []

    for table in soup.find_all("table"):
        word_group = WordGroup()
        
        for tr in table.find_all("tr"):
            td_list = tr.find_all("td")

            if len(td_list) == 1:
                word_group.extract_paraphrase(td_list[0])
                continue
            if len(td_list) == 3:
                word_group.extract_meaning(td_list[0])
                word_group.extract_word(td_list[1], td_list[2])
                continue
            if len(td_list) == 2:
                word_group.extract_word(td_list[0], td_list[1])
                continue
        word_group_list.append(word_group)




