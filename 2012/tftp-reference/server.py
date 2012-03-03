#!/usr/bin/python3

# misc
import sys
import argparse
import logging
# for async network handling
import asyncore
import socket
import time
# the tftp data structures
import tftproto

class TftpServerException(Exception):
    pass



#TODO: meh this udp shit is annoying, why the fuck didn't they use tcp?
# ok so we might want to support more than one "connection" at once
# one stream per ip address
# of course to keep it simple we can also allow one "connection" globally
# 
# so I thought of something like this:
    # AsyncoreServerUDP: 
        # receives from udp socket
        # based on ip address we pass it on to another handler object
    # TftpHandlerPool:
        # maintains a mapping ip address to handler objet
        # tracks timeouts (e.g remove handler obj after x seconds)
    # TftpHandler:
        # gets and parses data
        # sends response
        # tracks "connection" state
        
class TftpHandler(asyncore.dispatcher_with_send):
    def __init__(self):
        
    
    # This is called everytime there is something to read
    def handle_read(self):
        data, addr = self.recvfrom(514) # this is there
        logging.debug("read {0} bytes from {1}".format(len(data), addr))

    def handle_write(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]

class TftpHandlerPool():
    # create a class that handles one tftp handler object per peer
    # since udp is connectionless we have to track "connections" ourself 
    pass

class AsyncoreServerUDP(asyncore.dispatcher):
    def __init__(self, hostname="", ipversion=4):
        asyncore.dispatcher.__init__(self)
        if ipversion == 4:
            self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        elif ipversion == 6:
            self.create_socket(socket.AF_INET6, socket.SOCK_DGRAM)
        else:
            raise TftpServerException("Unkown IP Version = {0}".format(ipversion))
        self.set_reuse_addr()
        self.bind((hostname, 69))
        self.handlers = {}

    # Even though UDP is connectionless this is called when it binds
    # to a port
    def handle_connect(self):
        logging.debug("Received first packet!")
        
    def handle_read(self):
        handler = TftpHandler()

    def handle_write(self):
        handler = TftpHandler()



def run(args):
    logging.info("Starting Server...")
    AsyncoreServerUDP(args.bind)
    asyncore.loop()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=\
                            'A simple async tftp server, written in python.')
    parser.add_argument('-v', '--verbosity', metavar='N', type=str, nargs='?',\
                         help='configure verbosity of logging', default='INFO',\
                         choices=("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"))
    parser.add_argument("-b", "--bind", metavar="hostname" type=str, nargs="?",\
                                help="hostname/address to bind to", default="")
    args = parser.parse_args()
    logging.basicConfig(level=args.verbosity)
    run(args)
        
