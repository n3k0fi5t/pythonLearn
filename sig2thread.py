from threading import Thread

#import signal
import _signal as signal

from time import sleep

from sys import exit

def alarm(n):
    def sighandler(signum, frame):
        print("time out")
        exit(-1)
    signal.signal(signal.SIGALRM, sighandler)
    signal.alarm(n)

class SimpleThread(Thread):
    """docstring for SimpleThread"""
    def __init__(self, *arg,**karg):
        #init father class
        super().__init__()
        self.kw = "default"

        if "keyword" in karg:
            self.kw = karg["keyword"]

    def run(self):
        #wait forever
        while(1):
            print(self.kw)
            sleep(1)
            continue

    def __call__(self):
        self.__init__()
        self.run()

if __name__ == '__main__':
    print(dir(signal))
    simpleThread = SimpleThread(keyword="print yeah")
    simpleThread.setDaemon(1)
    simpleThread.start()
    SimpleThread()()

    alarm(5)
    while(1):
        pass

