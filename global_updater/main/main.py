ref_list = ['sub_folder']

def set_syspath(ref_list):
    from os import listdir, path
    import sys

    pathname = (path.dirname(path.abspath(__file__)))

    while(pathname):
        folders = listdir(pathname)
        for folder in folders:
            subpath = path.join(pathname, folder)
            if path.isdir(subpath) and folder in ref_list:
                sys.path.insert(0, subpath)
                ref_list.pop(ref_list.index(folder))
                print("add {} to sys path".format(subpath))
        if not ref_list:
            break
        pathname = path.dirname(pathname)
    return

set_syspath(ref_list)

from ref import global_updater

# update ref function to this scope
global_updater(globals())

# call reference function
ref_print("hahaha", "I call the ref function")



for f,v in dict(globals()).items():
    if callable(v):
        print(f, v)
print(len(globals()))



