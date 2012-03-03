#!/usr/bin/python3

import os
import os.path
import struct
import math

class TftpException(Exception):
    pass

def parse(self, pbytes):
    """Try to parse the"""
    opcode = pbytes.unpack(">H", pbytes[0:2])[0]
    if opcode == 1:
        return TftpReadRequest(pbytes)
    elif opcode == 2:
        return TftpWriteRequest(pbytes)
    elif opcode == 3:
        return TftpData(pbytes)
    elif opcode == 4:
        return TftpAck(pbytes)
    elif opcode == 5:
        return TftpError(pbytes)
    else:
        raise TftpException("Unkown opcode for Packet " + str(opcode))


class _Packet():
    def __init__(self, pbytes=None):
        super().__init__(self)
        self._opcode = 0
        if pbytes:
            self._parse(pbytes)

    @property
    def opcode(self):
        return self._opcode

    @opcode.setter
    def opcode(self, opcode): 
        if self._opcode != 0:
            raise TftpException("Can't change packet opcode!")
        if opcode in (1,2,3,4,5):
            self._opcode = opcode
        else:
            raise TftpException("Unkown opcode for Packet " + str(opcode))

    def __bytes__(self):
        return self.get_bytes()

    def get_bytes(self):
        return bytes()

    def _parse(self, p):
        self.opcode = struct.unpack(">H", p[0:2])[0]
        return p[2:]

    def get_bytes(self):
        return struct.pack(">H", self.opcode)


#   Type   Op #     Format without header
#          2 bytes    string   1 byte     string   1 byte
#          -----------------------------------------------
#   RRQ/  | 01/02 |  Filename  |   0  |    Mode    |   0  |
#   WRQ    -----------------------------------------------

class ReadWriteRequest(_Packet):
    def __init__(self, pbytes=None):
        super().__init__(self)
        self._opcode = 0
        self.data = bytes()
        self.filename = ""
        self.mode = ""
        if pbytes:
            self._parse(pbytes)

    def _parse(self, p):
        p = super()._parse(p)
        self.filename, self.mode = str(p.split(bytes(1)))


    def get_bytes(self):
        return super().get_bytes() + self.filename.encode("ascii") + bytes(1) + self.mode.encode("ascii") + bytes(1)


class ReadRequest(ReadWriteRequest):
    def __init__(self, pbytes=None):
        super().__init__(self, pbytes)
        self._opcode = 1

class WriteRequest(ReadWriteRequest):
    def __init__(self, pbytes=None):
        super().__init__(self, pbytes)
        self._opcode = 2

#          2 bytes    2 bytes       n bytes
#          ---------------------------------
#   DATA  | 03    |   Block #  |    Data    |
#          ---------------------------------

class Data(_Packet):
    def __init__(self, pbytes=None):
        self.blocknr = 0
        self.data = bytes()
        self._opcode = 3
        self.last = None
        if pbytes:
            self._parse(pbytes)

    def _parse(self, p):
        p = super()._parse(p)
        self.blocknr = struct.unpack(">H", p[:2])[0]
        self.data = p[2:]
        if len(self.data) != 512:
            self.last = True
            
    def get_bytes(self):
        return super().get_bytes() + struct.pack(">H", self.blocknr) + self.data

#          2 bytes    2 bytes
#          -------------------
#   ACK   | 04    |   Block #  |
#          --------------------

class Ack(_Packet):
    def __init__(self, pbytes=None):
        self.opcode = 4
        self.blocknr = 0
        if pbytes:
            self._parse(pbytes)
            
    def _parse(self, p):
        p = super()._parse(p)
        self.blocknr = struct.unpack(">H", p)[0]
        
    def get_bytes(self):
        return super().get_bytes() + struct.pack(">H", self.blocknr)

#          2 bytes  2 bytes        string    1 byte
#          ----------------------------------------
#   ERROR | 05    |  ErrorCode |   ErrMsg   |   0  |
#          ----------------------------------------

class Error(_Packet):
    def __init__(self, pbytes=None):
        self.opcode = 5
        self.errocode = 0
        self.errmsg = ""
        if pbytes:
            self._parse(pbytes)
            
    def _parse(self, p):
        p = super()._parse(p)
        self.errorcode = struct.unpack(">H", p[:2])[0]
        self.errmsg = p[2:-1].decode("ascii")

    def get_bytes(self):
        return super().get_bytes() + struct.pack(">H", self.errorcode) + self.errmsg.encode("ascii") + bytes(1)


#TODO: find out common error message and strings and paste them here 


class file_to_packets():
    """A generator which takes a filename as argument, opens it, and returns a
    tftp Data Packet for every """
    def __init__(self, filename):
        self.filename = os.path.abspath(os.path.expanduser(filename))
        self.file = open(self.filename, "rb")
        self.filesize = os.path.getsize(self.filename)
        self.chunkcount = math.ceil(self.filesize / 512)
        if self.chunkcount > 65535:
            raise TftpException("Maximum filesize exceeded!")
        self._currentchunknr = 1
    
    def __del__(self):
        self.file.close()
    
    def __iter__(self):
        return self
    
    def __next__(self):
        data = self.file.read(512)
        if not data:
            self.file.close()
            raise StopIteration
        datap = Data()
        datap.blocknr = self._currentchunknr
        datap.data = data
        self._currentchunknr += 1
        return datap
    

    
