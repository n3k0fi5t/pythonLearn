ref_list = ['sub_folder', 'not in folder']


def set_syspath(ref_list):
    from os import listdir, path
    import sys

    visited = {}

    def recursive_find(pathname):
        folders = listdir(pathname)
        for folder in folders:
            subpath = path.join(pathname, folder)
            # print("find {}... {}".format(subpath, folder))
            if subpath not in visited:
                visited[subpath] = 1
                # print(visited)
            else:
                break
            if folder in ref_list:
                sys.path.insert(0, subpath)
                ref_list.pop(ref_list.index(folder))
                print("add {} to sys path".format(subpath))
            if not ref_list:
                break
            if path.isdir(subpath):
                recursive_find(subpath)

    pathname = path.dirname(path.dirname(path.abspath(__file__)))
    print(pathname)
    recursive_find(pathname)
    return

import sys
set_syspath(ref_list)
from ref import global_updater

# update ref function to this scope
global_updater(globals())

# call reference function
ref_print("hahaha", "I call the ref function")


for f, v in dict(globals()).items():
    if callable(v):
        print(f, v)
print(len(globals()))
