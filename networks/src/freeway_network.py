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


import os
import subprocess
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element

from . import config
from .base import edge, lane, junction
from .freeway import Freeway


def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def create_freeway(direction, numberOfLanes, length, speed, add_traffic):
    freeway_obj = Freeway(direction, numberOfLanes, length, speed)

    # freeway_obj.test_freeway()

    # Create first and second Junction (start and endpoint of the freeway)
    junction_obj = [junction.Junction(i, freeway_obj) for i in range(2)]

    # Add Positon to Junctions
    junction_obj[0].addJunction(0.00, 0.00)
    junction_obj[1].addJunction(0.00 + freeway_obj.length, junction_obj[0].y)

    lanes_obj = [lane.Lane(i, freeway_obj, junction_obj) for i in range(numberOfLanes)]

    if direction:
        edges_obj = []
        for i in range(2):
            if (i % 2) == 0:
                edges_obj.append(edge.Edge(i, ""))
            else:
                edges_obj.append(edge.Edge(i, "-"))

        edges_obj[0].addEdge(junction_obj[0], junction_obj[1])
        edges_obj[1].addEdge(junction_obj[1], junction_obj[0])
        edges_elements = [Element('edge') for i in range(2)]

    else:

        edges_obj = [edge.Edge(i, "+") for i in range(1)]
        edges_obj[0].addEdge(junction_obj[0], junction_obj[1])
        edges_elements = [Element('edge') for i in range(1)]

    root = Element('net')

    # Add tags for Edge and Lanes in root
    for e, i in zip(edges_obj, range(2)):
        root.append(edges_elements[i])
        for k in lanes_obj:
            root = e.generateXMLE(root, k, edges_elements[i])

    # Add tags for Junction in root
    for i in junction_obj:
        root = i.generateXMLJ(root)

    tree = ET.ElementTree(root)

    indent(root)

    path = os.getcwd()

    tree.write(open(r'{}/road_networks/freeway.net.xml'.format(path), 'wb'), encoding="utf-8", xml_declaration=True)

    p = subprocess.Popen(['./sumoNetconvert.sh "{}" "{}" '.format(freeway_obj.name, " ")], shell=True,
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.STDOUT)
    p.wait()

    if add_traffic:
        print("Traffic generation starting ...")
        subPTraffic = subprocess.Popen(['./sumoTrafficGen.sh "{}" "{}" '.format(freeway_obj.name, False)],
                                       shell=True)
        subPTraffic.wait()

    config.create_config(freeway_obj.name, False, add_traffic)
