#!/usr/bin/env python

def global_updater(glb):
    glb.update(globals())

def ref_print(*args):
    for arg in args:
        print(arg)
