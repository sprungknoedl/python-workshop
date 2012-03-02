#!/usr/bin/python3

import struct

class TftpException(Exception):
    def __init__(self, msg):
        super.__init__(self)
        self.msg = msg

def parse(self, pbytes):
    opcode = pbytes.unpack("!h", [0:2])
    if opcode in (1,2,3,4,5)
        self._opcode = opcode
    else:
        raise TftpException("Unkown opcode for Packet " + str(opcode))
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


class _Packet():
    def __init__(self, packetbytes=None):
        super.__init__(self)
        if packetbytes is None:
            self._opcode = 0
        else:
            self._parse(packetbytes)

    @property
    def opcode(self):
        return self._opcode

    @opcode.setter
    def opcode(self, opcode):
        if opcode in (1,2,3,4,5)
            self._opcode = opcode
        else:
            raise TftpException("Unkown opcode for Packet " + str(opcode))

    def __bytes__(self):
        return self.get_bytes()

    def get_bytes(self):
        return bytes()

    def _parse(self, packetbytes):
        self.opcode = struct.unpack("!h", p[0:2])
        return p[2:]

    def get_bytes(self):
        return struct.pack("!h", self.opcode)


#   Type   Op #     Format without header
#          2 bytes    string   1 byte     string   1 byte
#          -----------------------------------------------
#   RRQ/  | 01/02 |  Filename  |   0  |    Mode    |   0  |
#   WRQ    -----------------------------------------------

class ReadWriteRequest(_Packet):
    def __init__(self, packetbytes=None):
        super.__init__(self)
        if packetbytes is None:
            self.data = bytes()
            self.filename = ""
            self.mode = ""
        else:
            self._parse(packetbytes)

    def _parse(self, p):
        p = super._parse(self, p):
        self.filename, self.mode = str(p.split(bytes(1)))


    def get_bytes(self):
        return super.get_bytes(self) + self.filename.encode("ascii") + bytes(1) + self.mode.encode("ascii") + bytes(1)


class ReadRequest(ReadWriteRequest):
    def __init__(self, packetbytes=None):
        super.__init__(self, packetbytes)
        self.opcode = 1

class WriteRequest(ReadWriteRequest):
    def __init__(self, packetbytes=None):
        super.__init__(self, packetbytes)
        self.opcode = 2

#          2 bytes    2 bytes       n bytes
#          ---------------------------------
#   DATA  | 03    |   Block #  |    Data    |
#          ---------------------------------

class Data(_Packet):
    def __init__(self, pbytes=None):
        if pbytes is None:
            self.blocknr = 0
            self.data = bytes()
            self.opcode = 3
        else:
            self._parse(pbytes)


    def _parse(self, p):
        p = super._parse(self, p)



#          2 bytes    2 bytes
#          -------------------
#   ACK   | 04    |   Block #  |
#          --------------------

class Ack(_Packet):
    pass

#          2 bytes  2 bytes        string    1 byte
#          ----------------------------------------
#   ERROR | 05    |  ErrorCode |   ErrMsg   |   0  |
#          ----------------------------------------

class Error(_Packet):
    pass
