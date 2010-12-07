#! /usr/bin/python2.6
# -*- coding: utf-8 -*-

import sys

def find(string, search):
    string = string.lower()
    search = search.lower()
    for p in (".", ",", ";", ":", "?", "!"):
        string = string.replace(p, "")
    search = search.strip()
    search = search.split(" ")[0]
    return (search in string)

if __name__ == "__main__":
    # read the user input
    if len(sys.argv) == 3:
        string = sys.argv[1]
        search = sys.argv[2]
    else:
        string = raw_input("String to search in: ")
        search = raw_input("String to search for: ")
    # apply find function
    if find(string, search):
        print "Input contains the specified word."
        sys.exit()
    else:
        print >>sys.stderr, "Input does not contain the specified word"
        sys.exit(-1)
        
##############################################################################
        
def find_mail(string):
	result = []
	for word in string.split():
		if word.find('@') == 0:
			result.append(word)
	return result
    
def find_mail(f):
	result = []
	for word in f.readline():
		if word.find('@') == 0:
			result.append(word)
	return result
    
with open(raw_inpput('file: ')) as f:
	list = find_mail(f)