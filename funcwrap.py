#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from functools import wraps

'''
@ is used to test or log something so that u won't rewrite the same function again
wrap the function into testing function
'''
def testing(func):
  #Using Decorators
  @wraps(func)
  def wrapper(*arg,**karg):
    t1 = time.time()
    result = func(*arg,**karg)
    t2 = time.time()
    print '%s took %0.3f ms' % (func.func_name, (t2-t1)*1000.0)
    return result
  return wrapper

@testing
def f(start,end):
  """the doc of f """
  return end-start

def decoratorwithargument(arg1,arg2):
  def wrap(func):
    '''
    Can see it appear at first,
    because python interpeter call it at decoration time
    '''
    print 'Inside wrap'
    print 'arg1 : %r'%arg1,'arg2 : %r'%arg2

    @wraps(func)
    def wrapper(*arg,**karg):
      res = func(*arg,**karg)
      return res
    return wrapper
  return wrap
@decoratorwithargument(100,152)
def a(b,c):
  """the doc of a """
  return b-c

if __name__ == '__main__':
  print f(1,3),'\n',f(2,5)
  print a(30,11)
  print f.__name__,f.__doc__
  print a.__name__,a.__doc__

