# Copyright (C) 2016, see AUTHORS.md
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

def compute_chksum(data):
    chksum = 0
    for el in data:
        chksum = ord(el) ^ chksum
          
    return hex(chksum)[2:].upper().zfill(2)

class Message(object):
    SEPARATOR = ':'
    STX = chr(0x02)
    ETX = chr(0x03)
    
    def __init__(self):
        self.addr = '0'
        self.cmd = ''
        self.chksum = 'XX'
    
    def set_cmd(self, cmd):
        self.cmd = str(cmd)
        
    def get_cmd(self):
        return self.cmd
    
    def set_checksum(self, chksum):
        self.chksum = chksum
        
    def get_checksum(self):
        return self.chksum
    
    def compute_checksum(self):
        return compute_chksum(list("".join([self.addr, self.cmd, self.SEPARATOR])))
        
    def set_address(self, addr):
        if isinstance(addr, (int, long)):
            if addr in range(0, 16):
                addr = hex(addr)[2:]
            else:
                raise ValueError("address must be either 0...15 or '@'")

        if not isinstance(addr, basestring):
            raise ValueError("address must either be an integer or a string")
                
        if addr.upper() in "1234567890ABCEDF@" and len(addr) == 1:
            self.addr = addr.upper()
        else:
            raise ValueError("address must be either 0...9, A...F or '@'")
    
    def get_address(self):
        return self.addr
    
    def get_raw(self):
        return "".join([self.STX, self.addr, self.cmd, self.SEPARATOR, self.chksum, self.ETX])
    
    def __str__(self):
	    return self.get_raw()

    def __repr__(self):
	    return self.__str__()
    
class Response(object):
    
    ACK = chr(0x06)
    NAK = chr(0x15)
    
    def __init__(self, response_array):
        
        response_array = str(response_array)
        
        if len(response_array) > 5:
            self.stx = response_array[0]
            self.status = response_array[1]
            self.etx = response_array[-1]
            self.chksum = response_array[-3:-1]
            
            if response_array[2] == Message.SEPARATOR:
                self.response = ''
            elif response_array[-4] == Message.SEPARATOR:
                self.response = response_array[2:-4]
            else:
                raise ValueError("Invalid response given (Separator ':' not found)")
        else:
            raise ValueError("Invalid response given (Response too short)")

    def get_response(self):
        return self.response
    
    def get_raw(self):
        return "".join([self.stx, self.status, self.response, Message.SEPARATOR, self.chksum, self.etx])
    
    def compute_checksum(self):
        return compute_chksum(list("".join([self.stx, self.status, self.response, Message.SEPARATOR])))
    
    def is_successful(self):
        return self.status == self.ACK
    
    def get_checksum(self):
        return self.chksum
    
    def is_valid(self):
        if self.stx is not Message.STX or self.etx is not Message.ETX:
            return False
        
        if not self.compute_checksum() == self.chksum:
            return False
        
        return True     
    
class AbstractMessage(object):
    def __init__(self, msg):
        self.msg = Message()
        self.init()
        
    def init(self):
        pass
        
    def get_message(self):
        return self.msg
    
    def create_response(self, response):
        raise NotImplementedError()
    
class AbstractResponse(object):
    def __init__(self, response):
        if not isinstance(response, Response):
            raise TypeError("No Response given")
            
        self.resp = response
        
    def get_response(self):
        return self.response