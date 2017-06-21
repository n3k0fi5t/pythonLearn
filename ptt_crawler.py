#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import re
from sys import argv, exit
from time import sleep
import threading
import Queue
import types
import copy as cp
from ptt_get_all_board import get_all_board

LOOP = 30

def check_over18(url):
    rs = requests.session()
    res = rs.get(url)
    code = BeautifulSoup(res.text, "html.parser")
    payload = {
        'from':url[18:],
        'yes':'yes'
        }
    res = rs.post('https://www.ptt.cc/ask/over18',data=payload)
    res = rs.get(url)
    return rs
    """
    if len(code.select('.over18-notice')) != 0:
        payload = {
            'from':url[18:],
            'yes':'yes'
            }
        rs = requests.session()
        res = rs.post('https://www.ptt.cc/ask/over18',data=payload)
        res = rs.get(url)
        return rs
    else:
        return requests.session()
    """

def get_pusher(url,rs,target):
  #intialzie list
  pushlist = []

  res = rs.get(url)
  code = BeautifulSoup(res.text, "html.parser")

  print '     Search :%s'%url
  for item in code.find_all('div',attrs={'class':'push'}):
    pusher = item.find('span','f3 hl push-userid')

    if pusher != None and pusher.text == target:
      content = item.find('span','f3 push-content')
      tag = item.find('span','f1 hl push-tag')
      datetime = item.find('span','push-ipdatetime')
      if tag == None:
        tag = item.find('span','hl push-tag')

      print '        ',tag.text,pusher.text,content.text,datetime.text
      pushlist.append(tag.text + pusher.text + content.text + datetime.text)

  #add url to end of pushlist
  if len(pushlist) != 0:
    pushlist[len(pushlist)-1] += '\n     Url:%s\n\n' % url
  return pushlist

def get_essayinfo(*arg):

  #test_url='https://www.ptt.cc/bbs/Grad-ProbAsk/M.1460432922.A.E6E.html'
  #print '%s \n %s\n ' %(authorlist[i],urlist[i])

  #initalize list
  metalist = []
  essaylist = []

  #initial setting
  url = arg[0]

  if len(arg) == 2:
    rs = arg[1]
  else:
    rs = requests.session()
  res = rs.get(url)
  code = BeautifulSoup(res.text, "html.parser")

  #for item in code.select('.article-metaline'): #will get 3 item type[list]
                                                #0:author
                                                #1:title
                                                #2:date
  #  print item
  #  print item.select('.article-meat-value')
    #for i in range(len(item)):
      #if i % 2 ==1:
        #metalist.append(item.text)
        #print metalist[len(metalist)-1]

  """meta list   0 Author
                 2 Title
                 4 Date
  """

  #Get span text
  for item in code.find_all('div',attrs={'class':'article-metaline'}):
    metalist.append(item.find('span','article-meta-value').text)

  essaylist.append(metalist)

  #essay content
  essaylist.append(code.select('#main-container')[0].text)

  #essay html
  essaylist.append(code.select('#main-container')[0])

  return essaylist

def get_board_url(code, tag):
  #Get earliest url
  #    prev url
  #    next url
  #    lateist url
  for item in code.select('.btn-group.btn-group-paging'):
    mlist = re.findall('/bbs/%s/index.+(?:html)'%tag,str(item))
    if mlist:
      for i in range(len(mlist)):
        mlist[i] = 'https://www.ptt.cc' + mlist[i]
        #print mlist[i]
      return mlist
  return []

def get_essay_list(*arg):
    global LOOP

    if len(arg) != 5:
        print len(arg)
        return
    target, result, idx, tag, mode = arg
    #the latest index of the board
    indexUrl = 'https://www.ptt.cc/bbs/%s/index.html' % tag
    tarlist = []

    #cond: true for continue search
    cond = True
    counter = 0

    while cond == True:
        #init each iteration
        urlist = []
        print 'Connect to ptt.cc ..'
        print 'Loading Url :%s\n'%indexUrl

        rs = check_over18(indexUrl)
        res = rs.get(indexUrl)
        code = BeautifulSoup(res.text, "html.parser")

        #search all essay at current index
        for item in code.select('.r-ent'):
            author = item.select('.author')[0].text
            #authorlist.append(author)

            #mode 2  get author essay
            if mode == 2 and author != target:
                continue

            #Using regular expression to get url
            m = re.search('/bbs/%s/.+(?:html)' % tag,str(item.select('.title')[0]))
            if m :
                url = 'https://www.ptt.cc' + m.group()
                urlist.append(url)

                if mode == 1:
                    tarlist.extend(get_pusher(url,rs,target))
                else:
                    essayinfo = get_essayinfo(url,rs)
                    print_essay(essayinfo)
                    tarlist.append(essayinfo)

        #get next index page url
        bdurlist = get_board_url(code, tag)
        if len(bdurlist) == 0:
            print code.text
            #sleep(0.3)
            continue

        #url is the earliest one
        if bdurlist[0] == indexUrl:
            cond = False
        else:
        #get earlier url
            indexUrl = bdurlist[1]

        counter += 1
        if counter > LOOP:
            cond = False

    result[idx] = cp.deepcopy(tarlist)

class Ptt_thread(threading.Thread):
    """docstring for Ptt_thread"""
    def __init__(self, arg):
        super(Ptt_thread,self).__init__()
        self.func = arg[0]
        self.paras = arg[1:]

    def run(self):
        self.func(*self.paras)
        exit()

    def restart(self, func):
        self.func = func
        self.run()

class Ptt_crawler():
  """docstring for Ptt_crawler"""
  def __init__(self, arg):

    assert len(arg)>2, 'Need at least three parameters.'
    self.target_board = arg[0]
    self.target_id = arg[1]
    self.mode = arg[2]
    self.threads = []
    self.result = None

  def start(self):
    if len(self.threads) == 0:
        #creat empty list with same size as target number
        #creat mutable object to save result
        self.result = [[] for i in range(len(self.target_board))]
        for idx, name in enumerate(self.target_board):
            thread = Ptt_thread(arg=(get_essay_list,self.target_id , self.result, idx,name , self.mode))
            thread.daemon = True
            self.threads.append(thread)
    for thread in self.threads:
        thread.start()
        print 'Thread[%d] start'%thread.ident

  def isrunning(self):
    if len(self.threads) == 0:
        return True
    for thread in self.threads:
        if thread.isAlive():
            return False
    return True

  def get_result(self):
    if self.isrunning():
        return self.result
    print 'thread don\'t finished., please wait.'
    while not self.isrunning():
        continue
    return self.result

if __name__ == '__main__':
    board =[val[0] for val in get_all_board(5)]
    #crawler = Ptt_crawler([['Gossiping', 'sex', 'Grad-ProbAsk', 'graduate'], 'jopurin', 1])
    crawler = Ptt_crawler([board, 'wuyiulin', 1])
    crawler.start()
    for item in crawler.get_result():
        if len(item) != 0:
            for subitem in item:
                print subitem

