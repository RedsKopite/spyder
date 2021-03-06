import requests
import pprint
from html.parser import HTMLParser
from abc import ABC
from bs4 import BeautifulSoup
from parsers.handles import HANDLE_DATA_DICT, HANDLE_STARTTAG_DICT

pp = pprint.PrettyPrinter(width=41, compact=True)


class SubLinkParser(HTMLParser, ABC):
    def __init__(self, sub_link, config):
        self.likeDataList = []
        self.columnDataList = []
        self.config_number = config["number"]

        super().__init__()

        html = requests.get(sub_link).text
        tag_list = BeautifulSoup(html, "lxml").find_all(config["tag"], config["attrs"])
        self.ignore = len(tag_list) == 0
        self.feed(f"{tag_list}")

        pp.pprint(self.likeDataList)
        pp.pprint(self.columnDataList)

    def handle_starttag(self, tag, attrs):
        if self.ignore:
            return

        HANDLE_STARTTAG_DICT[self.config_number](attrs, self.likeDataList)

    def handle_data(self, data):
        if self.ignore:
            return

        data = HANDLE_DATA_DICT[self.config_number](data)
        if data is not None and data not in self.columnDataList:
            self.columnDataList.append(data)
    

