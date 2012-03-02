#! /usr/bin/python2.6
# -*- coding: utf-8 -*-


def bytes_from_file(filename, chunksize=8192):
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(chunksize)
            if chunk:
                for b in chunk:
                    yield b
            else:
                break

# example:
for b in bytes_from_file('filename'):
    do_stuff_with(b)
