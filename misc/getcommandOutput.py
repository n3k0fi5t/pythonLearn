#!/usr/bin/env python
# -*- coding: utf-8 -*-
from commands import getoutput

msg = getoutput('ls -al')

print msg
