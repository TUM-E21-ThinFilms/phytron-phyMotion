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

import time
import threading

from slave.driver import Driver, Command
from slave.types import String, BitSequence
from protocol import PhytronProtocol

from messages.clear import ClearMessage


class PhytronDriver(Driver):
    def __init__(self, transport, protocol=None):
        if protocol == None:
            protocol = PhytronProtocol()

        super(PhytronDriver, self).__init__(transport, protocol)
        self.protocol = protocol

    def send_message(self, message):
        return self._protocol.query(self._transport, message)

    def clear_bus(self):
        self._protocol.clear(self._transport)
    
    def clear(self):
        self.send_message(ClearMessage())
