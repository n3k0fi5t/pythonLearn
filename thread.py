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
    self.func = arg

  #run self task
  def run(self):
    self.func()

def count_down():
  global Q
  t = 0
  if not Q.empty():
    t = Q.get()
  for i in range(t):
    print 'wait %d sec'%(t-i)
    time.sleep(1)

def main():
  global Q
  threads = []
  task = [random.randint(1,10) for i in range(10)]
  map(Q.put,task)

  for i in range(THREAD_NUM):
    thread = Mythread(count_down)
    threads.append(thread)
  for thread in threads:
    thread.start()

    #block main thread until wait 1.5s or empty for thread terminate
    thread.join(1.5)

if __name__ == '__main__':
  main()

