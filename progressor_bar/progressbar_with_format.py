#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep

import sys

bar = 10

pad = lambda s : '\r[{0:-<{2}}] {1}%'.format('='*(s/10), s,bar)

for i in range(101):
    sleep(0.05)
    sys.stdout.write(pad(i))
    sys.stdout.flush()
