#!/usr/bin/env python
# built-in modules
import math
from sys import exit

import re
import requests
import argparse
from bs4 import BeautifulSoup as BS

URL = 'http://www.findrate.tw/'

SUPPORT_CODE = ['jpy', 'usd', 'cny', 'eur', 'hkd', 'gbp',
        'aud', 'cad', 'sgd', 'chf', 'zar', 'sek', 'thb',
        'php', 'idr', 'krw', 'vnd', 'myr', 'inr', 'dkk',
        'nzd', 'mop', 'mxn', 'try'
        ]

HELP_DOC = {'jpy':'日幣', 'usd':'美金', 'cny':'人民幣',
        'eur':'歐元', 'hkd':'港幣', 'gbp':'英鎊',
        'aud':'澳幣', 'cad':'澳幣', 'sgd':'新加坡幣',
        'chf':'瑞士法郎', 'zar':'南非幣', 'sek':'瑞典幣',
        'thb':'泰幣','php':'菲國比索', 'idr':'印尼幣',
        'krw':'韓元', 'vnd':'越南盾', 'myr':'馬來幣',
        'inr':'印度披索', 'dkk':'丹麥幣','nzd':'紐元',
        'mop':'澳門幣', 'mxn':'墨西哥比索', 'try':'土耳其里拉'}

ORDINAL_NUMBERS = ['1st', '2nd', '3rd']

class BankExchange(object):
    """doc of BankExchange"""

    def __init__(self, bank_name, attrs=[], amount=0):
        super(BankExchange, self).__init__()
        self._attrs = attrs
        self._pot = 0
        self._lowest = 0
        self.fee = 0
        self.name = bank_name
        self.amount = amount

        # start to parse attributes
        self._parseAttrs()
        self.calculate()

    def __call__(self):
        return self

    def _parseAttrs(self):
        assert len(self._attrs) == 6, 'length error of bank data'
        # assgin a very high value to not sold bank
        if self._attrs[1] == '--':
            self.cash_sell = 1e9
        else:
            self.cash_sell = float(self._attrs[1])
        self.time = self._attrs[4]
        self.fee_describes = self._attrs[5]
        self._parseFee()

    def _parseFee(self):
        dcbs = self.fee_describes.split(',')
        for dcb in dcbs:
            if '免手續費' in dcb or 'ATM免收' in dcb or '本行賣免收' in dcb:
                self.fee = 0
                continue

            # pasring number
            r = re.search('[-+]?\d*\.\d+|\d+', dcb)
            if r:
                quantity = float(r.group())
            else:
                # invalid
                continue

            if '總額' in dcb:
                self._pot = quantity * 0.01 # partial of total
            elif '最低' in dcb:
                self._lowest = quantity
            elif '每筆' in dcb:
                self.fee = quantity

        if hasattr(self, '_lowest') and self._lowest != 0:
            if self.fee == 0 and self.amount:
                if self._lowest > self.amount * self._pot:
                    self.fee = self._lowest
                else:
                    self.fee = self.amount * self._pot
        elif hasattr(self, '_pot') and self._pot != 0 :
            self.fee = self.amount * self._pot

        self.fee = math.ceil(self.fee)

    def disp_info(self):
        print(
"""Info:
\tBank name: {0}
\tcash sell: {1}
\tUpdate time: {2}
\tfee: {3}
\tamount: {4}
\tpot: {5}
\tlowest: {6}
\tdescribes: {7}
""".format(self.name, self.cash_sell, self.time, self.fee, self.amount,
    self._pot, self._lowest, self.fee_describes
))

    def setAmount(self, amount):
        self.amount = amount

    def calculate(self):
        # quantize by jpy / consume NTD
        self.cp_value = 1 / self.cash_sell * self.amount / (self.amount + self.fee)

def create_pareser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a','--amount', nargs='?',
            default=-1, metavar='Cash to exchange (required)')
    parser.add_argument('-c', '--code', nargs='?', metavar='Currency code (required)',
            default='')
    parser.add_argument('-i', '--inquire', action='store_true')
    parser.add_argument('-tops', nargs='?', default=1, metavar="top X of max CP, X is integer")
    return parser

def get_source(url, code):
    from selenium import webdriver
    from time import sleep
    wait_time = 3

    print("Open chrome driver")
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=option)
    print("\tfind button")
    driver.get(URL)
    ele = driver.find_elements_by_class_name(code)
    print("\tclick button")
    assert len(ele) > 0, 'unknown error, button must be found'
    ele[0].click()
    print("\tget page source")
    sleep(wait_time) # wait for page

    src = driver.page_source
    driver.close()
    driver.quit()
    print('\tclose driver')
    return src

def inquire_function():
    for (k, v) in HELP_DOC.items():
        print('Money name: {0:}\t code: {1}'.format(v, k))

# utils
def isnumber(val, ntype=float):
    try:
        ntype(val)
        return True
    except:
        return False

def assert_and_help(parser, flag=True, describe=''):
    if flag is False:
        print(describe)
        parser.print_usage()
        exit(-1)

# main
def main():
    parser = create_pareser()
    args = parser.parse_args()
    if args.inquire is True:
        inquire_function()
        exit(1)
    else:
        assert_and_help(parser, args.code in SUPPORT_CODE,
                "Code is invalid, please re-input, use -i to inquired code")
        assert_and_help(parser, isnumber(args.amount), "Must be a number")
        assert_and_help(parser, float(args.amount) > 0,
                "Exchange cash must larger than 0")
        assert_and_help(parser, isnumber(args.tops, ntype=int),
                "Tops must be an integer")

        # assign value
        tops = int(args.tops)
        code = 'a_' + args.code

    # use selenium to get page source because of dynamicaly generated url
    src = get_source(URL, code)

    # use bs4 to parse html
    bank_rate = {}
    code = BS(src, 'html.parser')
    for item in code.find_all('table')[1].find_all('tr'):
        rate_list, bank_name = [], ''
        for subitem in item.find_all('td'):
            if subitem.attrs['class'][0] == 'bank':
                bank_name = subitem.text.strip('\n')
            elif subitem.attrs['class'][0] == 'WordB':
                rate_list.append(subitem.text)
            else:
                pass

        # drop invalid data
        if rate_list is [] or bank_name == '':
            continue
        if bank_name not in bank_rate:
            bank_rate[bank_name] = rate_list

    bank_list = {}

    for k, v in bank_rate.items():
        bank = BankExchange(k, v, float(args.amount))
        bank_list[bank.name] = bank

    # sort
    cmp_result = sorted([v for (k, v) in bank_list.items()],
            key=lambda x:x.cp_value, reverse=True)

    for i in range(tops):
        ordn = ORDINAL_NUMBERS[i] if i < len(ORDINAL_NUMBERS) else str(i + 1) + 'th'
        assert len(bank_list) > i, ''
        print("{0} is the {2} CP value in exchange with rate: {1:.4}"
            .format(cmp_result[i].name, (1 / cmp_result[i].cp_value), ordn))
        # display the bank info
        cmp_result[i].disp_info()

if __name__ == '__main__':
    main()
