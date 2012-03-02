#!/usr/bin/python3

import asyncore
import socket

class TftpHandler(asyncore.dispatcher):
    
    def __init__(self):
        filename = ""
    
    def handle_read(self):
        data, addr = self.recvfrom(2048) 
        pass
    
    def handle_write(self):
        pass

class AsyncoreServerUDP(asyncore.dispatcher):
   def __init__(self):
      asyncore.dispatcher.__init__(self)
      self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
      self.set_reuse_addr()
      self.bind(('', 69))

   # Even though UDP is connectionless this is called when it binds
   # to a port
   def handle_connect(self):
      print "Server Started..."

   # This is called everytime there is something to read
   def handle_read(self):
      data, addr = self.recvfrom(514)

   # This is called all the time and causes errors if you leave it out.
   def handle_write(self):
      pass

AsyncoreServerUDP()
asyncore.loop()


