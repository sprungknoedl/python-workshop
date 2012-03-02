#!/usr/bin/python3

import socket
import os
import sys

import ftplib
import poplib
import imaplib
import time

class Monitor():
    
    service_types = ["imap", "pop", "ftp", "tcp"]
    
    def __init__(self, ipaddr):
        self.ipaddr = ipaddr
        self.services = []
        self.openlist = []
        self.closedlist = []
        
    def portscan(self):
        self.openlist = []
        self.closedlist = []
        for service in self.services:
            port = service["port"]
            try:
                s = socket.create_connection((self.ipaddr, port))
                self.openlist.append(port)
                s.close()
            except socket.error:
                self.closedlist.append(port)
        
    def checkservices(self):
        for service in self.services:
            if service["type"] == "ftp":
                if self.check_ftp():
                    service["status"] = "OK"
                else:
                    service["status"] = "ERROR"
            elif service["type"] == "pop":
                if self.check_pop():
                    service["status"] = "OK"
                else:
                    service["status"] = "ERROR"
            elif service["type"] == "imap":
                if self.check_imap():
                    service["status"] = "OK"
                else:
                    service["status"] = "ERROR"
                
                
    def check_ftp(self):
        try:
            f = ftplib.FTP(host=self.ipaddr)
            return True
        except (ftplib.all_errors, socket.error, IOError):
            return False
        
    def check_imap(self):
        try:
            f = imaplib.IMAP4(host=self.ipaddr)
            return True
        except (imaplib.error, socket.error, IOError):
            return False
        
    def check_pop(self):
        try:
            f = poplib.POP3(self.ipaddr)
            return True
        except (poplib.error_proto, socket.error, IOError):
            return False

    def status(self):
        for service in self.services:
            print(service)
        
    def monitor(self):
        while True:
            self.portscan()
            self.checkservices()
            print("Open Ports:")
            print(self.openlist)
            print("Closed Ports:")
            print(self.closedlist)
            print("Services:")
            self.status()
            time.sleep(10)
            

if __name__ == "__main__":
    print("Starting python monitoring...")
    m = Monitor(input("Hostname: "))
    services = []
    while True:
        print("Add a service:")
        name = input("Name: ")
        port = input("Port: ")
        print("Please specify service type (default is raw tcp):", Monitor.service_types)
        stype = input("Service Type: ")
        if not stype in Monitor.service_types:
            print("Unkown Service Type, using raw tcp", file=sys.stderr)
            stype = "tcp"
        services.append({"name":name, "port":port, "type":stype})
        if input("Abort? Y/N").upper() == "Y":
            break
    m.services = services
    m.monitor()
