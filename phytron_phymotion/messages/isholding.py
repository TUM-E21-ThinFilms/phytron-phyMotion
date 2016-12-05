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

from phytron_phymotion.message import AxisMessage, AbstractResponse, Response


class IsHoldingMessage(AxisMessage):
    def init(self):
        self.msg._axis_cmd = '==H'

    def create_response(self, raw_response):
        return IsHoldingResponse(raw_response)


class IsHoldingResponse(AbstractResponse):
    pass