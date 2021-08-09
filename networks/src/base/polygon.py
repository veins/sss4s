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

from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element

import os


# Currently: Sumo default-value of Lane is 3.2m
class Polygon:
    def __init__(self, netw_obj):
        self.netw_obj = netw_obj
        self.street_margin = self.netw_obj.num_lanes * 3.2
        self.building_margin = self.netw_obj.building_margin
        self.root = Element('additional')
        self.poly_id = ""
        self.poly_shape = ""
        self.poly = {}

    def dict_poly(self):

        self.poly['id'] = self.poly_id
        self.poly['color'] = 'red'
        self.poly['fill'] = '1'
        self.poly['layer'] = '128.00'
        self.poly['shape'] = self.poly_shape

    # Setting Street-Margin

    # Generate everywhere polygons
    def generate_polygon(self):
        counter = 0

        for i in range(self.netw_obj.x_dir - 1):
            for j in range(self.netw_obj.y_dir - 1):
                self.poly_id = "poly_{}".format(counter)

                x1 = (i * self.netw_obj.x_length + self.street_margin) + self.building_margin
                y1 = -(j * self.netw_obj.y_length + self.street_margin) - self.building_margin

                x2 = (i * self.netw_obj.x_length - self.street_margin) + self.netw_obj.x_length - self.building_margin
                y2 = -(j * self.netw_obj.y_length + self.street_margin) - self.building_margin

                x3 = (i * self.netw_obj.x_length - self.street_margin) + self.netw_obj.x_length - self.building_margin
                y3 = -(j * self.netw_obj.y_length - self.street_margin) - self.netw_obj.y_length + self.building_margin

                x4 = (i * self.netw_obj.x_length + self.street_margin) + self.building_margin
                y4 = -(j * self.netw_obj.y_length - self.street_margin) - self.netw_obj.y_length + self.building_margin

                self.poly_shape = "{},{} {},{} {},{} {},{} {},{}".format(x1, y1, x2, y2, x3, y3, x4, y4, x1, y1)
                self.generate_xml()

                counter += 1

        path = os.getcwd()

        tree = ElementTree(self.root)
        tree.write(open(r'{}/road_networks/{}.add.xml'.format(path, self.netw_obj.name), 'wb'), encoding="utf-8",
                   xml_declaration=True)

    # Generate the xml-file
    def generate_xml(self):

        poly = Element('poly')
        self.root.append(poly)

        self.dict_poly()

        for key in self.poly.keys():
            poly.set("{}".format(key), "{}".format(self.poly[key]))
