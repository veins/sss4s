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

import collections

from xml.etree.ElementTree import Element

from . import lane


class Edge:
    def __init__(self, counter, positive):
        self.dict_edge = collections.OrderedDict()
        self.counter = counter
        self.id = "edge_{}".format(self.counter)
        self.positive = positive
        self.fr = ""
        self.to = ""
        self.priority = -1
        self.funtion = ""
        self.lengthforlane = ""
        self.changed = ""

    # Add Edge between the Junctions and add the minus
    def addEdge(self, junction1, junction2):
        self.fr = junction1.id
        junction1.setOutgoingEgde(self.id)

        self.to = junction2.id
        junction2.setIncomingEdge(self.id)

    def dictEdge(self):
        self.dict_edge['id'] = self.id
        self.dict_edge['from'] = self.fr
        self.dict_edge['to'] = self.to
        self.dict_edge['priority'] = -1

    # root
    # l = lanes_obj
    # child: edge_elements of root
    def generateXMLE(self, root, l, child):
        l.length = self.lengthforlane
        k = l.generateXMLL(root, self.id)  # Wir setzen hier die ID der Lane
        child.append(k)
        self.dictEdge()
        for key in self.dict_edge.keys():
            child.set("{}".format(key), "{}".format(self.dict_edge[key]))
        return root


class InternalEdge:

    def __init__(self, internaljunc, counter, netw_obj):
        self.id = ""
        self.function = "internal"
        self.internalJunc = internaljunc
        self.dict_internal = collections.OrderedDict()
        self.counter = counter
        self.netw_obj = netw_obj

    def dict_internal_edge(self):
        self.dict_internal['id'] = self.id
        self.dict_internal['function'] = self.function

    def setLanes(self, root):
        self.id = ":{}_{}".format(self.internalJunc.id, self.counter)
        childi = Element('edge')
        root.append(childi)
        l = lane.Lane(0, self.netw_obj, self.internalJunc)
        o = l.generateXMLL(root, self.id)
        self.internalJunc.setintLanes(o.attrib['id'])
        childi.append(o)
        self.dict_internal_edge()

        for key in self.dict_internal.keys():
            childi.set("{}".format(key), "{}".format(self.dict_internal[key]))
