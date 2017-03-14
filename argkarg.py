#!/usr/bin/env python
# -*- coding: utf-8 -*-
def func(*arg,**karg):
  for item in arg:
    print item,
  print
  for key,val in karg.items():
    print key,val,
if __name__ == '__main__':
  func(1,2,3,4,a=1,b=2,c=3)
