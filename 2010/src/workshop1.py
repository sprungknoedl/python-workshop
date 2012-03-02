#!/usr/bin/python
# This file contains some example solutions to exercises given during the first
# python workshop. spelling and grammar mistakes are my present to you ;)

import os

def find_mail(arg):
    """
    searches a string for e-mail addresses. returns a list.
    """

    # to append to a list, the list must exist
    res = []
    # iterate over every word in arg, split without arguments split at every whitespace
    for word in str(arg).split():
        # first solution:
        # if word.find('@') != -1:
        # better solution:
        if '@' in word:
            # append to end of list
            res.append(word)
    return res

def read_file(filename):
    """
    read file and return content as string
    """

    # open file `filename` in read mode
    with open(filename, 'r') as f:
        # read whole file at once
        return f.read()

def write_list(filename, list):
    """
    write a list to a file new line seperated
    """

    # open file `filename` in write mode
    with open(filename, 'w') as f:
        # join a list with newline (os dependent) and write
        # the string to the file
        f.write(os.linesep.join(list))

def read_list(filename):
    """
    read in previosly written file as python list
    """
    
    # open  file `filename` in read mode
    with open(filename, 'r') as f:
        # read whole file and split by lines
        return f.read().splitlines()

# dummy calls to functions
mails = find_mail(read_file('file_with_emails'))
write_list('foo', mails)
new_list = read_list('foo')
