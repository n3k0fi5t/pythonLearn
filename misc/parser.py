#!/usr/bin/env python
import argparse
def retrive_attr(attr_str):
    pre_split = attr_str.split('-')
    max_prefix = 0
    for idx, v in enumerate(pre_split):
        if len(v):
            max_prefix = idx
            break
    if max_prefix>1:
        return attr_str[max_prefix:].replace('-','_')
    elif max_prefix ==1:
        return attr_str[max_prefix]
    else:
        return attr_str
args = ['--choice-set', '-redundant', 'defualt']

parser = argparse.ArgumentParser()

parser.add_argument('-c', '--choice-set', metavar='choices', nargs='*', default='')

parser.add_argument('-r', '-redundant',nargs='?', default='')

parser.add_argument('defualt',nargs='*', default='')

ret = parser.parse_args()

for v in args:
    print(getattr(ret, retrive_attr(v)))

print(dir(ret))
