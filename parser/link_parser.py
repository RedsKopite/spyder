import requests
import pprint
from html.parser import HTMLParser
from abc import ABC
from bs4 import BeautifulSoup

pp = pprint.PrettyPrinter(width=41, compact=True)


class LinkParser(HTMLParser, ABC):
    def __init__(self, link):
        self.subLinkList = []
        self.columnDataList = []

        super().__init__()

        html = requests.get(link).text
        self.feed(str(BeautifulSoup(html, "lxml").find_all("div", class_="info")))

        pp.pprint(self.subLinkList)
        pp.pprint(self.columnDataList)

    def handle_starttag(self, tag, attrs):
        for (variable, value) in attrs:
            if variable == "href" and value[2:5] == "www":
                self.subLinkList.append(f"http:{value}")

    def handle_data(self, data):
        if data not in [", ", " ", "[", "]"] and "综合得分" not in data:
            self.columnDataList.append(data.strip('\n').strip())
