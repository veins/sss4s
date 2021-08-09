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


class Junction:

    def __init__(self, counter, network_obj):
        self.dict_junction = collections.OrderedDict()
        self.counter = counter
        self.id = "junc{}".format(self.counter)
        self.type = 'dead_end'
        self.x = 0
        self.y = 0
        self.incLanes = ""
        self.intLanes = ""
        self.shape = ""
        self.network_obj = network_obj
        self.incoming_edges = []
        self.outgoing_edges = []
        self.status = ""
        self.deathend = True
        self.internal = False
        self.all_direction_incoming = [0, 0, 0, 0]
        self.all_direction_outcoming = [0, 0, 0, 0]

    # Adds a Junction with coordinates
    def addJunction(self, x, y):
        self.x = x
        self.y = y
        # self.counter += 1

    def dictJunction(self):
        self.dict_junction['id'] = self.id
        self.dict_junction['type'] = self.type
        self.dict_junction['x'] = self.x
        self.dict_junction['y'] = self.y
        self.dict_junction['incLanes'] = self.incLanes
        self.dict_junction['intLanes'] = self.intLanes
        self.dict_junction['shape'] = self.shape
        self.dict_junction['type'] = self.type

    # key is attribute of junction and must be string
    def addDictJunction(self, key, value):
        self.dict_junction['{}'.format(key)] = value

    def generateXMLJ(self, root):
        b = Element('junction')
        root.append(b)
        self.set_shapeJunction(root)
        self.setincLanes(root)
        self.setPriority()
        self.dictJunction()
        for key in self.dict_junction.keys():
            b.set("{}".format(key), "{}".format(self.dict_junction[key]))

        return root

    # Always 3D coordinates
    # if s[0] = "-" dann tue das -Y ich weiss dass die edge die bidrectional ist
    def set_shapeJunction(self, root):
        c = self.network_obj.num_lanes * 2 * 1.60
        if self.network_obj.direction:
            for child in root:
                if child.tag == "edge":
                    if (child.attrib['id'][0] == '-') and (child.attrib['from'] == self.id):
                        self.shape = "{},{} {},{} {},{}".format(self.x, self.y, self.x, self.y - c, self.x, self.y)

                    elif (child.attrib['id'][0] == "e") and (child.attrib['from'] == self.id):
                        self.shape = "{},{} {},{} {},{}".format(self.x, self.y, self.x,
                                                                self.y + self.network_obj.num_lanes * 2 * 1.60, self.x,
                                                                self.y)
        else:
            self.shape = "{},{} {},{} {},{}".format(self.x, self.y, self.x, self.y - c, self.x, self.y)

    # Setting here the attribute incLanes of the Junction
    def setincLanes(self, root):
        first = True
        for child1 in root:
            if child1.tag == "edge" and child1.attrib['id'][0] != ':':
                if child1.tag == "edge" and child1.attrib['to'] == self.id:
                    for i in child1:
                        if first:
                            self.incLanes = i.attrib['id']
                            first = False
                        else:
                            self.incLanes = self.incLanes + " " + i.attrib['id']

    # set ingoing edge
    def setIncomingEdge(self, edgeto):
        self.incoming_edges.append(edgeto)

    # set outgoing edge
    def setOutgoingEgde(self, edgefr):
        self.outgoing_edges.append(edgefr)

    # Checking if Junction is a deathend or a junction with traffic light
    def setPriority(self):
        if self.network_obj.direction:
            if (len(self.incoming_edges) + len(self.outgoing_edges)) in [8, 4, 6]:
                self.deathend = False
                self.type = "priority"
                self.internal = True

    # Subtree of the Junction
    def setRequest(self, root):
        pass

    # Internal lanes of the junction
    def setintLanes(self, id):
        self.intLanes = self.intLanes + " " + "{}".format(id)
