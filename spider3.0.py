import os
import sys
import pprint
import pandas as pd
from parsers.link_parser import LinkParser
from parsers.sub_link_parser import SubLinkParser
# from multiprocessing import Pool
from config import *

path = os.path.dirname(__file__)
sys.path.append(path)

pp = pprint.PrettyPrinter(width=41, compact=True)
COLUMN_KEY_DICT = {
    0: 'title',
    1: 'broadcast',
    2: 'bullet_chat',
    3: 'up_name',
    4: 'pts',
    5: 'website',
    6: 'likes',
    7: 'coins',
    8: 'collect',
    9: 'share',
    10: 'total_time'
}


def sub_link_spider(sub_link, config, column_dict, start_index):
    sub_link_parser = SubLinkParser(sub_link, config)

    for idx, data in enumerate(sub_link_parser.columnDataList):
        if len(column_dict) <= start_index + idx:
            return 0

        column_dict[start_index + idx].append(data)

    return len(sub_link_parser.columnDataList)


def run_spider(link):
    link_parser = LinkParser(link)

    column_dict = {i: [] for i in range(11)}
    [column_dict[i % 5].append(v) for i, v in enumerate(link_parser.columnDataList)]

    # sub_link_pool = Pool(10)
    for sub_link in link_parser.subLinkList:
        start_index = 6
        column_dict[5].append(sub_link)
        for config in ANALYSIS_LIST:
            start_index += sub_link_spider(sub_link, config, column_dict, start_index)

    return {COLUMN_KEY_DICT[k]: v for k, v in column_dict.items()}


if __name__ == "__main__":
    link_result = run_spider(
        "https://www.bilibili.com/v/popular/rank/game"
    )
    df = pd.DataFrame(link_result)
    with open("./test.txt", "w") as f:
        f.write("\n".join([f"{k}: {', '.join(v)}" for k, v in link_result.items()]))
