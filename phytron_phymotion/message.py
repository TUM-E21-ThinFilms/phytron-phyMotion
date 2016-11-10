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

class Message(object):
    SEPARATOR = ':'
    STX = chr(0x02)
    ETX = chr(0x03)
    
    def __init__(self):
        self.addr = 0
        self.cmd = ''
        self.chksum = 'XX'
    
    def set_cmd(self, cmd):
        self.cmd = cmd
        
    def get_cmd(self):
        return self.cmd
    
    def set_checksum(self, chksum):
        self.chksum = chksum
        
    def get_checksum(self):
        return self.chksum
    
    def compute_checksum(self):
        data = list("".join([self.addr, self.cmd, self.SEPARATOR]))
        
        chksum = 0
        for el in data:
            chksum = ord(el) ^ chksum
            
        return hex(chksum)[2:]
        
    def set_address(self, addr):
        self.addr = addr & 0xF
    
    def get_address(self):
        return self.addr
    
    def get_raw(self):
        return "".join([self.STX, self.cmd, self.SEPARATOR, self.chksum, self.EXT])
    
    def __str__(self):
	    pass

    def __repr__(self):
	    return self.__str__()
    

class Response(object):
    def __init__(self, response_array):
        pass