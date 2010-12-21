import os
import time

pid = os.fork()
if pid == 0:
    time.sleep(5)
    print "Hello I'm a child :D"
else:
    print "killing my child"
    os.killpg(pid, 9)
