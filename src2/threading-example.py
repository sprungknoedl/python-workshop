#! /usr/bin/python2.6
# -*- coding: utf-8 -*-


from threading import Thread, Lock
#from multiprocessing import Process as Thread
#from multiprocessing import Lock

class Worker(Thread):
    
    lock = Lock()
    val = 0
    
    def __init__(self, lower, upper):
        Thread.__init__(self)
        self.lower = lower
        self.upper = upper
		
    def run(self):
        x = sum( i**10 % (i**2-1) for i in xrange(self.lower, self.upper) )
        with self.lock:
            self.val += x

def main():
    threads = [Worker(2, 1000), Worker(1000, 2000), Worker(2000, 3000)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print Worker.val

if __name__ == "__main__":
    main()
