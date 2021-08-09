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


class Lane:
    def __init__(self, counter, network_obj, junction_obj):
        self.dict_lane = collections.OrderedDict()
        self.id = ""
        self.counter = counter
        self.index = counter
        self.length = 50.00
        self.shape = ""
        self.shape_minus = ""
        self.network_obj = network_obj
        self.junction_obj = junction_obj
        self.shape_positive = 0.00
        self.speed = self.network_obj.speed
        self.internalLanes = []

    def dictLane(self):
        self.dict_lane['id'] = self.id
        self.dict_lane['index'] = self.index
        self.dict_lane['speed'] = self.speed
        if self.network_obj.name == 'freeway':
            self.dict_lane['length'] = self.network_obj.length
        else:

            self.dict_lane['length'] = self.length
        self.dict_lane['shape'] = self.shape

    def generateXMLL(self, root, edge_id):
        d = Element('lane')
        self.id = "{}_{}".format(edge_id, self.counter)
        # Internal Lanes have different speed
        if self.id[0] == ':':
            self.speed = 3.0
        self.set_shapeLane()
        self.dictLane()
        for key in self.dict_lane.keys():
            d.set("{}".format(key), "{}".format(self.dict_lane[key]))
        return d

    # Set shape-attribute of Lane
    def set_shapeLane(self):
        self.shape_positive = self.network_obj.num_lanes * 2 * 1.60 - 1.60
        if self.network_obj.name == 'freeway':
            for i, j in zip(self.junction_obj, reversed(self.junction_obj)):
                a = (j.x, j.y)
                if self.id[0] == '-':
                    self.shape_minus = "{}".format(self.shape_minus) + " " + "{},{}".format(a[0], a[1] + (
                            self.shape_positive - (3.20 * self.counter)))
                    self.shape = self.shape_minus

                else:
                    b = (i.x, i.y)
                    self.shape = "{}".format(self.shape) + " " + "{},{}".format(b[0], b[1] - (
                            self.shape_positive - (3.20 * self.counter)))
        else:
            self.shape = "0.0,-8.0 100.0,-8.0"
