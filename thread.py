#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading

import Queue

import time

import random

Q = Queue.Queue()  #unlimit queue
THREAD_NUM = 3

class Mythread(threading.Thread):
  """docstring for Mythread"""
  def __init__(self, arg):
    super(Mythread, self).__init__()
    self.func = arg[0]
    self.arg = arg[1:]

  #run self task
  def run(self):
      self.func(*self.arg)

def count_down(*arg):
  global Q
  t = 0
  if not Q.empty():
    t = Q.get()
  for i in range(t):
    print 'wait %d sec'%(t-i),arg
    time.sleep(1)

def main():
  global Q
  threads = []
  task = [random.randint(1,10) for i in range(10)]
  map(Q.put,task)

  for i in range(THREAD_NUM):
    run_event = threading.Event()
    run_event.set()

    thread = Mythread(arg=(count_down,1.5,2))
    threads.append(thread)
    thread.daemon = True
    thread.start()

  for thread in threads:
    print 'Thread % d start join' %(thread.ident)
    thread.join()

  for thread in threads:
    print thread.ident
    thread.run()
    #block main thread until wait 1.5s or empty for thread terminate
   # thread.join(1.5)

if __name__ == '__main__':
    main()

