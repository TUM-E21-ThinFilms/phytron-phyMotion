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

import slave
import logging
from slave.transport import Timeout
from slave.protocol import Protocol
from message import AbstractMessage, Message, Response

class CommunicationError(Exception):
    pass

class PhytronProtocol(Protocol):
    def __init__(self, slave_addr=0, logger=None):

        if logger is None:
            logger = logging.getLogger(__name__)
            logger.addHandler(logging.NullHandler())

        self.logger = logger
        self.receiver = slave_addr

    def set_logger(self, logger):
        self.logger = logger

    def clear(self, transport):
        self.logger.debug("Clearing message queue")
        while True:
            try:
                transport.read_bytes(32)
            except slave.transport.Timeout:
                return
        
    def send_message(self, transport, message):
        
        data = message.get_raw()
        self.logger.debug('Send: "%s"', message)

        transport.write(data)
    
    def read_response(self, transport):
        try:
            return transport.read_until(Message.ETX)
        except:
            raise CommunicationError("Could not read response")
    
    def query(self, transport, message):
        if not isinstance(message, AbstractMessage):
            raise TypeError("message must be an instance of AbstractMessage")
            
        msg = message.get_message()
        msg.set_address(self.receiver)
        msg.set_checksum(msg.compute_checksum())
        
        self.send_message(transport, msg)
        response = self.read_response(transport)
        
        resp = message.create_response(response)
        
        if not resp.is_valid():
            self.logger.error("Received invalid response: %s", resp)
            raise CommunicationError("Invalid response")
            
        if not resp.is_successful():
            self.logger.warning("Action (%s) was not successfuly: %s", message, resp)
            
        return resp

    def write(self, transport, message):
        return self.query(transport, message)
