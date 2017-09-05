#!/usr/bin/env python
# -*- coding: utf-8 -*-
def test_time(func):
  def wrapper(*arg,**karg):
    import time
    t1 = time.time()
    res = func(*arg,**karg)
    t2 = time.time()
    print '%r cost %r s'%(func.func_name,t2-t1)
    return res
  return wrapper

#x,y must be list
@test_time
def compare_intersect(x, y):
  return frozenset(x).intersection(y)

import random
a = [[random.randrange(100) for i in xrange(10)]for j in range(3)]
b = [[random.randrange(100) for i in xrange(10)]for j in range(3)]
print a
print b
for i in range(len(a)):
  print compare_intersect(a[i],b[i])
