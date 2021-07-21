# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 18:35:21 2021

@author: Admin
"""
from abc import ABC

import pandas as pd
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import re
import requests


class MyHTMLParser(HTMLParser, ABC):
    data, att, newlist = [], [], []

    def __init__(self, raw_html):
        super().__init__()
        self.feed(raw_html)

    def handle_starttag(self, tag, attrs):
        for (variable, value) in attrs:
            if variable == "href" and value[2:5] == 'www':
                self.att.append(value)

    def handle_data(self, data):
        self.data.append(data)


class GetDetails(HTMLParser, ABC):
    data, att = [], []

    def __init__(self, raw_html):
        super().__init__()
        self.feed(raw_html)

    def handle_starttag(self, tag, attrs):

        for (variable, value) in attrs:
            if variable == "title" and "点赞数" in value:
                self.att.append(value)

    def handle_data(self, data):
        self.data.append(data)


class ResponseParser(GetDetails, ABC):

    def __init__(self, raw_html, url, tag, dict_attrs):
        super().__init__(raw_html)
        self.feed(raw_html)
        self.url = url
        self.tag = tag
        self.dict_attrs = dict_attrs

    def get_response(self):
        self.html = requests.get(self.url)
        self.soup = BeautifulSoup(self.html.text, 'lxml')
        self.target_text = self.soup.find_all(self.tag, self.dict_attrs)
        self.feed(self.target_text)


if __name__ == "__main__":

    # html = requests.get('http://www.bilibili.com/v/popular/rank/game')
    # soup = BeautifulSoup(html.text, 'lxml')
    # text1 = soup.find_all('div', class_='info')
    # d = MyHTMLParser(str(text1))
    #
    # rawlist = d.data
    #
    # newlist = []
    # for i in rawlist:
    #     if i != ', ' and i != ' ' and '综合得分' not in i and i != '[' and i != ']':
    #         newlist.append(i.strip())
    #
    # column_dict = {i: [] for i in range(5)}
    # [column_dict[i % 5].append(v) for i, v in enumerate(newlist)]
    # web = ['http:' + i for i in d.att]

    # 计划把每个web里的网站中相应的内容取出来，先拿第一个测试，但一直跑不出来。想把获取html文件和处理列表等等这些都写到类里面，未遂
    newClass = ResponseParser('https://www.bilibili.com/video/BV1w44y1m79B', 'div', {'class' : 'ops'})
