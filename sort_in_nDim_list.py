#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import operator

target = [[idx,random.randint(1,50)] for idx in range(30)]

res = sorted(target, key = lambda x :x[1])

print target
print res



"""
iteritems() will return each item of dictionary with tuple type
d = {'a':1,'b':2}
iteritems() = iterable generator which contain ('a',1), ('b',2)
"""
def runtime(f):
    from functools import wraps

    @wraps(f)
    def wrapper(*arg, **karg):
        from time import time
        t1 = time()
        result = f(*arg, **karg)
        t2 = time()
        print("function: \'{0}\' Cost {1:.4f} ms.".format(f.__name__, (t2-t1) * 1000.0))
        return result
    return wrapper

target = {chr(idx+90):random.randint(1,50) for idx in range(30)}

@runtime
def s3(target):
    res = sorted(target.iteritems(), key=lambda (k,v): [v,k])#makes tuple to list

    print
    print res

@runtime
def s1(target):
    res = sorted([[k,v] for (k,v) in target.iteritems()],key = lambda x:x[1])
    print
    print res

@runtime
def s2(target):
    res = sorted(target.items(),key=operator.itemgetter(1))
    print
    print res

s1(target)
s2(target)
s3(target)
