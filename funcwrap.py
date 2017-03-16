#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

'''
@ is used to test or log something so that u won't rewrite the same function again
wrap the function into testing function
'''
def testing(func):
  #Using Decorators
  def wrapper(*arg,**karg):
    t1 = time.time()
    result = func(*arg,**karg)
    t2 = time.time()
    print '%s took %0.3f ms' % (func.func_name, (t2-t1)*1000.0)
    return result
  return wrapper

@testing
def f(start,end):
  return end-start

if __name__ == '__main__':
  print f(1,3),'\n',f(2,5)
