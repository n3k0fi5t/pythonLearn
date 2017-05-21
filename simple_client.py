#encoding: utf-8
from __future__ import print_function
import socket,sys,time
import threading

IS_ALIVE = False

def handleThread(clientsock, cond):
  global IS_ALIVE
  print("\nUsing {} to handle listening\n".format(clientsock.getsockname()))
  while(1):
    # try:
    #   sock, sockaddr=clientsock.accept()
    #   print("Got connection from {}".format(sock.getpeername()))
    # except KeyboardInterrupt:
    #   sys.exit(1)
    # except:
    #   traceback.print_exc()
    #   sys.exit(1)
    try:
      buf = clientsock.recv(2048)
      if buf :
        if buf != "the send ok signal":
          print("\n{:<50}{},from:{}".format(buf, " "*15, clientsock.getpeername()))
      else:
        cond.acquire()
        IS_ALIVE = False
        cond.notifyAll()
        print(IS_ALIVE)
        cond.release()
        print("Detroy thread")
        sys.exit(-1)

    except socket.error, e:
      print("Error receiving data %s" %(e))
      sys.exit(1)

def main():
  global IS_ALIVE

  port=56122
  host='127.0.0.1'
  cond = threading.Condition()
  while 1:
    try:
      s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except socket.error, e:
      print("Strange error creating socket: %s"% e)
      sys.exit(1)
    try:
      s.connect((host,port))
      cond.acquire()
      IS_ALIVE = True
      thread=threading.Thread(target = handleThread,
                               args = (s, cond), name="")
      #set the thread could be killed at the same time when parent thread was killed
      thread.setDaemon(1)
      thread.start()
      cond.release()
    except socket.gaierror,e:
      print("Error connect to server %s\n" % e)
      sys.exit(1)
    print("\nconnect to ",(host,port))
    print("Start conversation ...")
    while(1):
        try:
          cmd = raw_input()
        except KeyboardInterrupt:
          print("close connect to {}".format(s.getpeername()))
          s.close()
          sys.exit(1)

        cond.acquire()
        is_alive = IS_ALIVE
        cond.release()
        if is_alive == False:
          print("Server offline")
          sys.exit(-1)
        try:
          s.sendto(cmd, (host,port))
        except (socket.error,socket.gaierror), e:
          print("Error sending data %s"% e)
          #print("Server offline")
          sys.exit(-1)


if __name__=='__main__':
  main()
