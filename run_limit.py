#!/usr/bin/env python
import threading

class ExecThread(threading.Thread):
    """TODO"""
    def __init__(self, f, *args, **kargs):
        super().__init__()
        self.f = f
        self.args = args
        self.kargs = kargs
        self.res = None
        self.setDaemon(1)

    def run(self):
        self.res = self.f(*self.args, **self.kargs)

def runtime(n):
    from functools import wraps
    def outer(f):
        @wraps(f)
        def inner(*arg, **karg):
            from time import time
            thr = ExecThread(f, *arg, **karg)
            st = time()
            thr.start()
            while time() - st < n and thr.res is None:
                continue
            result = thr.res

            del(thr)
            if result != None:
                print("\'{0}\' Cost {1:.2f} s.".format(f.__name__, (time() - st)))
            else:
                print("{0} timeout!!".format(f.__name__))
            return result
        return inner
    return outer

@runtime(1)
def testing(char, flag):
    from time import sleep
    if flag:
        sleep(3)
    print(char)

if __name__ == '__main__':
    testing("testing function", True)
    print("lalaland")
