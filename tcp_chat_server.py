#!/usr/bin/env python
from __future__ import print_function
import socket
import sys
import commands
import threading
from Queue import Queue

#creat simple chat msg class
class chat_item():
    def __init__(self):
        self.q = Queue()

    def setmsg(self, name, msg):
        self.q.put((name, msg))

    def getmsg(self):
        if self.q.empty():
            return (None, None)
        return self.q.get()

class chat_client_handler(threading.Thread):
    def __init__(self, client, condition, shared_item, name=''):
        super(chat_client_handler, self).__init__()
        self.client = client
        self.condition = condition
        self.item = shared_item
        self.name = name
        self.print_last = False

    def run(self):
        while(1):
            try:
                buf = self.client.recv(2147483647)
            except :
                print("Error when receiving data, close {}".format(self.name))
                print("Destroy thread: {}".format(self.name))
                sys.exit(-1)

            if not buf:
                print("Error when receiving data, close {}".format(self.name))
                print("Destroy thread: {}".format(self.name))
                sys.exit(-1)
            else:
                self.print_last = False

            #get the lock
            if(self.print_last == False):
                self.condition.acquire()
                print("\nGot message :{:<50}, from {}".format(buf, self.client.getpeername()))
                self.item.setmsg(self.client.getpeername(), buf)
                #notify the broadcasting thread
                self.condition.notify()
                self.condition.release()
                self.print_last = True

            #send recv ok to source client
            try:
                self.client.sendall("the send ok signal")
            except socket.error, e:
                print("Error sending data %s"% e)
                print("Destroy thread: {}".format(self.name))
                self.exit()
            print("{} handling recv data finish\n".format(self.name))

def get_min_thread_name(thread_list):
    for idx,thd in enumerate(thread_list):
        if(thd.isAlive()):
            continue
        else:
            return idx
    return len(thread_list)

def get_threadPool_available(thread_list):
    cnt = 0
    for thd in thread_list:
        if thd.isAlive():
            cnt += 1
    return cnt

def boradcast_handler(cond, thread_list, shared_buf, mode=1):

    #get shared buf
    while(1):
        #get msg
        cond.acquire()
        #wait the client sent the msg and be notified by another thread
        #wait() will release the lock, i.e., not acquire lock
        cond.wait()
        (name, msg) = shared_buf.getmsg()
        cond.release()

        for thd in thread_list:
            #if thd.isAlive():
            if thd.isAlive() and name != thd.client.getpeername():
                try:
                    thd.client.sendto("{}: {}".format(name, msg),thd.client.getpeername())
                    print("send broadcast to {} ok ".format(thd.client.getpeername()))
                except socket.error, e:
                    print(e)
        print("broadcast finished")
host, port = "", 56122
MAX_CONNECT = 3
shared_buf = chat_item()
thread_list = []

#creat socket
try:
    print("Creat socket ...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, e:
    print("Encounter error when creating socket!!")
    sys.exit(-1)

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("Set socket option ...")
sock.bind((host, port))
print("Binding to host: {} , port: {}".format(host, port))

sock.listen(MAX_CONNECT)
print("Listening ...")


#creat condition for shared buffer
Cond = threading.Condition()

#creat a thread to broadcast new message to others
print("Creat thread for broadcasting ...")
bdthread = threading.Thread(target = boradcast_handler,
                             args = (Cond, thread_list, shared_buf),
                             name="broadcast thread")
bdthread.setDaemon(1)
bdthread.start()

while(1):
    try:
        clientsock, clientaddr = sock.accept()
    except KeyboardInterrupt:
        sys.exit(1)
    except:
        traceback.print_exc()
        sys.exit(-1)
    try:
        print("Got connection from {:<50}".format(clientsock.getpeername()))
    except:
        print("face error!!")
        sys.exit(-1)
    idx = get_min_thread_name(thread_list)
    print("find index %d"%idx)

    if idx >= len(thread_list):
        thdname = "thread-{}".format(idx)
        thd = chat_client_handler(clientsock, Cond, shared_buf, clientsock.getpeername())
        thd.setName(thdname)
        thd.setDaemon(1)
        thd.start()
        thread_list.append(thd)
        print("Creat {:<20} to handle connection {:<30}".format(thdname, clientsock.getpeername()))
    else:
        thd = thread_list[idx]
        print("Using exist {:<20} to handle connection {:<30}".format(thd.name, clientsock.getpeername()))
        thd.__init__(clientsock, Cond, shared_buf, clientsock.getpeername())
        thd.setDaemon(1)
        thd.start()
    print("Service thread pool size: {}".format(get_threadPool_available(thread_list)))
    print("Active thread :",threading.activeCount())



