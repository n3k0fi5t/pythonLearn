#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import wraps

def c(a,b):
    return a*b

def decoratorf(func):
  def wrapper(f):
    @wraps(f)# keeps the __name__, __doc__ not to loss
    def wrap(*arg,**karg):
      res = func(*arg,**karg)
      res2 = f(res,*arg,**karg)
      return res2
    return wrap
  return wrapper

@decoratorf(c)
def y(*arg):
  return reduce(lambda x,y:x+y,arg)

if __name__ == '__main__':
  print y(3,10)
  print y.__name__, y.__doc__
