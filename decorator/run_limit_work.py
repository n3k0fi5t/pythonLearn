#!/usr/bin/env python
import threading
from sys import exit
def runtime(n):
    def _async_raise(tid, exctype, thr):
        import inspect, ctypes
        if not inspect.isclass(exctype):
            raise TypeError("Only types can be raised (not instances)")
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid),
                                                      ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # "if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    class ExecThread(threading.Thread):
        """TODO"""
        def __init__(self, f, t ,*args, **kargs):
            super(ExecThread, self).__init__()
            self.f = f
            self.t = t
            self.args = args
            self.kargs = kargs
            self.res = None
            self.setDaemon(1)

        def run(self):
            self.res = self.f(*self.args, **self.kargs)

        def terminate(self):
            _async_raise(self._get_tid(), SystemExit, self)

        def _get_tid(self):
            if not self.isAlive():
                raise threading.ThreadError("the thread is not active")
            return self.ident

    from functools import wraps
    def outer(f):
        @wraps(f)
        def inner(*arg, **karg):
            from time import time
            thr = ExecThread(f, n,  *arg, **karg)
            st = time()
            thr.start()
            while time() - st < n and thr.res is None:
                continue
            if thr.isAlive():
                thr.terminate()
            result = thr.res

            # delete thread
            del(thr)
            # handle the result
            if result != None:
                print("\'{0}\' Cost {1:.2f} s.".format(f.__name__, (time() - st)))
            else:
                print("{0} timeout!!".format(f.__name__))
            return result
        return inner
    return outer

@runtime(3)
def testing(char, flag):
    from time import sleep
    if flag:
        cnt = 0
        while cnt < 10:
            print("sleeeeep")
            sleep(1)
    print(char)
    return 1

if __name__ == '__main__':
    from time import sleep
    testing("testing function2", False)
    testing("testing function1", True)
    print("lalaland")
    sleep(10)
