#!/usr/bin/env python
# -*- coding: utf-8 -*-

#list comprehension
a = [i for i in xrange(10)]

print a

#dic comprehension
b = {key:val for key,val in [(i,i**2) for i in xrange(10)]}

print b
