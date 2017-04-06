#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

import random

train = [i**2 for i in range(10)]
label = np.array([np.round(np.random.rand())  for i in range(len(train))],dtype=int)

rd = np.arange(len(train))
np.random.shuffle(rd)
train = np.array(train)[np.newaxis]
label = label[np.newaxis]
print train,label
print train.T[rd].T,label.T[rd].T
