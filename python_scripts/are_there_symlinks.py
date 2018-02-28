#!/usr/bin/python
# author: Sean O'Haver
# description: Useful script in rpm building to check for symlinks from the
#              current working directory
import os

def is_symlink(filename):
    if os.path.islink(filename):
        print "{0} is a symlink for {1}".format(
            filename,
            os.path.join(os.path.dirname(filename), os.readlink(filename))
        )

for dpath, dnames, filenames in os.walk(os.getcwd()):
    for filename in filenames:
        fullpath = os.path.join(dpath, filename)
        is_symlink(fullpath)
    for dname in dnames:
        fullpath = os.path.join(dpath, dname)
        is_symlink(fullpath)

