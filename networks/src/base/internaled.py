#
# Copyright (C) 2021 Dalisha Logan <https://www.cms-labs.org/people/dalisha.logan/>
# Copyright (C) 2021 Tobias Hardes <https://www.cms-labs.org/people/hardes/>
#
# SPDX-License-Identifier: GPL-2.0-or-later
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
from . import lane

from xml.etree.ElementTree import Element


class InternalEdge:

    def __init__(self, internaljunc, counter, netw_obj):
        self.id = ""
        self.function = "internal"
        self.internalJunc = internaljunc
        self.dict_internal = {}
        self.counter = counter
        self.netw_obj = netw_obj
        self.internalLanesID = []

    def dict_internal_edge(self):
        self.dict_internal['id'] = self.id
        self.dict_internal['function'] = self.function

    def setLanes(self, root, *args):
        root1 = root
        self.id = ":{}_{}".format(self.internalJunc.id, self.counter)

        childi = Element('edge')
        root.append(childi)

        # If we have multiple straight connections, then multiple lanes
        if len(args) != 0:
            lanes_obj = [lane.Lane(i, self.netw_obj, self.internalJunc) for i in range(self.netw_obj.num_lanes)]
        else:
            lanes_obj = list(lane.Lane(0, self.network_obj, self.internalJunc))

        for i in lanes_obj:
            o = i.generateXMLL(root1, self.id)
            self.internalJunc.setintLanes(o.attrib['id'])
            # print(o.attrib['id'])
            self.internalLanesID.append(o.attrib['id'])
            childi.append(o)

        self.dict_internal_edge()

        for key in self.dict_internal.keys():
            childi.set("{}".format(key), "{}".format(self.dict_internal[key]))

        return self.internalLanesID, root1
