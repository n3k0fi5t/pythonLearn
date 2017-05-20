#!/usr/bin/env python
import signal

import sys

import os

def alarm(t):
    def handler(signum, frame):
        print("Time out")
        exit()
    signal.signal(signal.SIGALRM,handler)
    signal.alarm(t)

def main():
    alarm(30)
    sys.dont_write_bytecode = True
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    sys.stdin = os.fdopen(sys.stdin.fileno(), 'r', 0)
    while(True):
        print(raw_input("type any what you want."))

if __name__ == '__main__':
    main()
