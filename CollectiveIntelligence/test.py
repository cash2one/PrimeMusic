#!/usr/bin/env python
# -*- coding:GBK
# author: sunhaowen@baidu.com
# date: 2013/07/15 21:48

from sklearn import svm

def here():
    print("PrimeMusic")

if __name__ == "__main__":
    X = [[0, 0], [1, 1]]
    y = [0, 1]
    clf = svm.SVC()
    clf.fit(X, y)
    print(clf.predict([[2., 2.]]))