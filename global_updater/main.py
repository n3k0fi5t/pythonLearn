#!/usr/bin/env python

ref_list = ['sub_folder']

def set_syspath(ref_list):
    from os import listdir, path
    import sys

    pathname = path.dirname(path.dirname(__file__))

    while(pathname):
        folders = listdir(pathname)
        for folder in folders:
            subpath = path.join(pathname, folder)
            if path.isdir(subpath) and folder in ref_list:
                sys.path.insert(0, subpath)
        pathname = path.dirname(pathname)
    return

set_syspath(ref_list)
from sub_folder.ref import global_updater

# update ref function to this scope
global_updater(globals())

# call reference function
ref_print("hahaha", "I call the ref function")



for f,v in dict(globals()).items():
    if callable(v):
        print(f, v)
print(len(globals()))



