import os
import sys
path = os.path.dirname(__file__)
sys.path.append(path)

import pprint
import pandas as pd
from parsers.link_parser import LinkParser
from parsers.sub_link_parser import SubLinkParser
# from multiprocessing import Pool
from config import *

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
    10:'total_time'
}


def sub_link_spider(sub_link, config, column_dict):
    sub_link_parser = SubLinkParser(sub_link, config)

    column_dict[5].append(sub_link)
    column_dict[6].append(sub_link_parser.columnDataList[0])
    column_dict[7].append(sub_link_parser.columnDataList[1])
    column_dict[8].append(sub_link_parser.columnDataList[2])
    column_dict[9].append(sub_link_parser.columnDataList[3])


def run_spider(link):
    link_parser = LinkParser(link)

    column_dict = {i: [] for i in range(10)}
    [column_dict[i % 5].append(v) for i, v in enumerate(link_parser.columnDataList)]

    for config in ANALYSIS_LIST:
        # sub_link_pool = Pool(10)
        for sub_link in link_parser.subLinkList:
            sub_link_spider(sub_link, config, column_dict)

    return {COLUMN_KEY_DICT[k]: v for k, v in column_dict.items()}


if __name__ == "__main__":
    link_result = run_spider(
        "https://www.bilibili.com/v/popular/rank/game"
    )
    df = pd.DataFrame(link_result)
    with open("./test.txt", "w") as f:
        f.write("\n".join([f"{k}: {', '.join(v)}" for k, v in link_result.items()]))
