#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep

from sys import stdout

def progressBar(iteration, total, prefix='', suffix='',accuracy=1,length=100,fill='='):
    per = ('{0:.' + str(accuracy)  + 'f}').format(iteration / float(total) * 100)
    filled = length * iteration / total
    bar = fill * filled + ('>' if filled < length else '') + '-' * (length - filled - 1)
    return ('\r{0} [{1}]{2}% {3}').format(prefix, bar, per, suffix)

l = [i for i in xrange(300)]
leng = len(l)

for idx,val in enumerate(l,1):
    sleep(0.05)
    stdout.write(progressBar(idx,leng, prefix='Progress:', suffix='complete', length=50))
    stdout.flush()
