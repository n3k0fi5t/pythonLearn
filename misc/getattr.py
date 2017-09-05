#!/usr/bin/env python
from time import sleep

class myclass(object):
    """docstring for myclass"""
    def __init__(self, *args,**kargs):
        super(myclass, self).__init__()
        self.args = args
        self.kargs = kargs
    def print_arg(self):
        for item in self.args:
            print(item)
        for k,v in self.kargs.items():
            print(k,v)
    def wait(self, w_time):
        print("start wait")
        sleep(w_time)
        print("wake up")

if __name__ == '__main__':
    obj = myclass(1,2,3,{"s":5},a=15,b=13,c={"a":2})
    #obj.print_arg()
    #obj.wait(15)
    prtarg = getattr(obj, "print_arg")
    wait = getattr(obj, "wait")

    wait(3)
    prtarg()

