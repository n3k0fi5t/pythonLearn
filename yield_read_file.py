#!/usr/bin/env python
from sys import argv
import pathlib

def read_file(path):
    with open(path, 'r+') as fp:
        block_size = 1024
        while True:
            content = fp.read(block_size)
            if content:
                yield content
            else:
                return

def main():
    if len(argv) > 1:
        file_path = argv[1]
        f = pathlib.Path(file_path)
        # file exist
        if f.is_file():
            for content in read_file(file_path):
                print(content)

if __name__ == '__main__':
    main()

