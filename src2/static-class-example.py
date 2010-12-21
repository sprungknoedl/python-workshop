#!/usr/bin/python

class Counter(object):
    count = 0
    def __init__(self):
        self.__class__.count += 1

    @classmethod
    def print_count_class(cls):
        print "Class: count=", cls.count

    @staticmethod
    def print_count_static():
        print "Static: count=", cls.count

c = Counter()
Counter.print_count_class()
Counter.print_count_static()
