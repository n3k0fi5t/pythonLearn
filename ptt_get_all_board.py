#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

import requests

import re

PTT_ENTRY_URL = 'https://www.ptt.cc/bbs/index.html'

#find first N hot board
HOT_BOARD = 214748

SUB_CLASS = ['board-name', 'board-nuser', 'board-class', 'board-title']
TARGET = ['board-name', 'board-nuser', 'board-class', 'board-title']


def get_all_board(bdn=HOT_BOARD):

    url = PTT_ENTRY_URL
    board_list = []

    with requests.session() as rs:
        res = rs.get(url)
        code = BeautifulSoup(res.text, "html.parser")

        for item in code.find_all('a',attrs={'class':'board'})[:bdn]:
            html_tag = ''
            board_info = []
            href = re.search('/bbs/.+/index.html' ,str(item))
            if href:
                html_tag = href.group()[5:-11]
            board_info.append(html_tag)
            for sub_class in frozenset(SUB_CLASS).intersection(TARGET):
                r = item.select('.' + sub_class)[0]
                board_info.append(r.text)

            board_list.append(board_info)
    return board_list
