#!/usr/bin/env python

class myclass(object):
    """docstring for myclass"""
    def __init__(self, *arg):
        super(myclass, self).__init__()
        self.arg = arg

    def __call__(self, *arg, **karg):
        for item in arg:
            print(item)
        for k,v in karg.items():
            print(k,v)
if __name__ == '__main__':
    obj = myclass()(1,2,3,a=1,b=2,c=3)
