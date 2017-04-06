#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep

from sys import stdout
class ProgressBar(object):
    """docstring for ProgressBar"""
    def __init__(self, count, iteration=0,
                prefix = '', suffix = '', accuracy=1, barlength=100,fill='=',unfill='-'):
        super(ProgressBar, self).__init__()
        self.iteration = iteration
        self.count = count
        self.prefix = prefix
        self.suffix = suffix
        self.accuracy = accuracy
        self.barlength = barlength
        self.fill = fill
        self.unfill = unfill
        self.bar = ''
        self.per = 0.0

    def progressBar(self):
        if self.iteration > self.count:
            self.iteration = self.count
        self.per = ('{0:.' + str(self.accuracy)  + 'f}').format(self.iteration / float(self.count) * 100)
        filled = self.barlength * self.iteration / self.count
        self.bar = self.fill * filled + ('>' if filled < self.barlength else '') + self.unfill * (self.barlength - filled - 1)
        return ('\r{0} [{1}]{2}% {3}').format(self.prefix, self.bar, self.per, self.suffix)

    def update(self,idx):
        self.iteration = idx
        stdout.write(self.progressBar())
        stdout.flush()
        self.isFinished()

    def isFinished(self):
        if self.iteration == self.count:
            print
            return True
        return False

l = [i for i in xrange(30)]
leng = len(l)
pb = ProgressBar(leng, prefix='Progress:', suffix='complete', barlength=50,fill='=',unfill='-', accuracy=2)
for idx,val in enumerate(l,1):
    sleep(0.05)
    pb.update(idx)
pb = ProgressBar(leng,barlength = 20)
for idx,val in enumerate(l,1):
    sleep(0.05)
    pb.update(idx)
