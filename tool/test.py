#!/usr/bin/env python
# -*- coding:GBK
# author: sunhaowen@baidu.com
# date: 13-11-14 下午3:42

def here():
    print("PrimeMusic")

def translate(data):
    """
    """
    while (isinstance(data, list) or isinstance(data, dict)) and len(data) == 1:
        if isinstance(data, list):
            data = data[0]
        elif isinstance(data, dict):
            data = data.values()[0]

    if isinstance(data, int) or isinstance(data, str):
        return data
    if isinstance(data, list):
        for index, item in enumerate(data):
            data[index] = translate(item)
    if isinstance(data, dict):
        for (key, value) in data.items():
            if key == "innerText" or key == "outerText":
                del data[key]
                data["text"] = translate(value)
            elif key == "innerHTML" or key == "outerHTML":
                del data[key]
            else:
                data[key] = translate(value)
    return data


def translate_new(data):
    """
    """
    if isinstance(data, int) or isinstance(data, str):
        return data

    if isinstance(data, list):
        for index, item in enumerate(data):
            data[index] = translate_new(item)
    if isinstance(data, dict):
        for (key, value) in data.items():
            if key == "innerText" or key == "outerText":
                del data[key]
                data["text"] = translate_new(value)
            elif key == "innerHTML" or key == "outerHTML":
                del data[key]
            else:
                data[key] = translate_new(value)
        if len(data) == 1 and data.keys()[0] in ["text", "src", "href", "value"]:
            data = data.values()[0]
    return data

if __name__ == '__main__':

    data = {
        "pageType": "detail",
        "image" : {
            "src" : [
                "http://bcs.duapp.com/xiachufangnew/recipe_step_pic/200/bb/e5/100197543.1.jpg",
                "http://bcs.duapp.com/xiachufangnew/recipe_step_pic/200/26/f7/100197544.1.jpg"
            ]
        },
        "amount" : [
            {
                "ingredientsName" : {
                    "innerText" : "三黄鸡"
                },
                "ingredientsAmount" : {
                    "innerText" : "1斤"
                }
            },
            {
                "ingredientsName" : {
                    "innerText" : "冬菇"
                },
                "ingredientsAmount" : {
                    "innerText" : "6个"
                }
            }
        ],
        "name" : [
            {
                "innerText" : "冬菇焖鸡",
                "src": [
                    "lalal",
                    "ddddd"
                ]
            }
        ],
        "description" : {
            "innerText" : [
                "干的",
                "安泰桥"
            ]
        },
        "arg" : {
            "targeturl" : {
                "href" : "http://www.xiachufang.com/recipe/100031352/"
            }
        }
    }
    data = translate_new(data)
    print(data)

    here()
