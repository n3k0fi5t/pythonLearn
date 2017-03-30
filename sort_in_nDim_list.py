#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

target = [[idx,random.randint(1,50)] for idx in range(30)]

res = sorted(target, key = lambda x :x[1])

print target
print res


target = {idx:random.randint(1,50) for idx in range(30)}

res = sorted(target.iteritems(), key=lambda (k,v): (v,k))

print target
print res

for idx,v, in target.iteritems():
    print idx,v
