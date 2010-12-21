#! /usr/bin/python2.6
# -*- coding: utf-8 -*-


class C(object):
    def __init__(self):
        self._x = None

    @property
    def x(self):
        """I'm the 'x' property."""
        return self._x

    @x.setter
    def x(self, value):
        if len(str(value)) <= 5:
            self._x = value

    @x.deleter
    def x(self):
    	self._old_x = self._x
        self._x = None
        
print ">>> c = C()"
c = C()
print ">>> c.x = 12"
c.x = 12
print ">>> print c.x"
print c.x
print ">>> c.x = 8"
c.x = 8
print ">>> print c.x"
print c.x
print ">>> del c.x"
del c.x
print ">>> print c.x"
print c.x
print ">>> print c._old_x"
print c._old_x
