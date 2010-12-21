import os
while True:
    pid = os.fork()
    if pid:
        print "Hello I'm a child :D"
