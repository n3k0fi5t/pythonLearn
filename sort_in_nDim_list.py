#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

target = [[idx,random.randint(1,50)] for idx in range(30)]

res = sorted(target, key = lambda x :x[1])

print target
print res



"""
iteritems() will return each item of dictionary with tuple type
d = {'a':1,'b':2}
iteritems() = iterable generator which contain ('a',1), ('b',2)
"""
target = {chr(idx+90):random.randint(1,50) for idx in range(30)}

res = sorted(target.iteritems(), key=lambda (k,v): [v,k])#makes tuple to list

print target
print
print res

res = sorted([[k,v] for (k,v) in target.iteritems()],key = lambda x:x[1])

print
print res
