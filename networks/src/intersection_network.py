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
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element

from . import config
from .graph import Graph
from .base import edge, lane, junction, polygon, connection, traffic_light
from .intersection import Intersection


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


def create_intersection(name, length_x, length_y, lanes, tlall, tl, tlnotall, multiple, speed, building,
                        building_margin, add_traffic):
    tl = list(dict.fromkeys(tl))
    tlnotall = list(dict.fromkeys(tlnotall))

    intersection_obj = Intersection(name, length_x, length_y, lanes, tlall, tl, tlnotall, multiple, speed, building,
                                    building_margin)

    counter = 0

    junction_obj = []

    # in y-Richtung nur 3 Nodes
    for i in range(3):
        a = []
        for y in range(intersection_obj.x_dir):
            a.append(junction.Junction(counter, intersection_obj))
            counter += 1
        junction_obj.append(a)

    junction_obj[0][0] = 0
    junction_obj[0][intersection_obj.x_dir - 1] = 0
    junction_obj[2][0] = 0
    junction_obj[2][intersection_obj.x_dir - 1] = 0

    counter = 0
    # Setting the positions of junction
    for n in range(intersection_obj.y_dir):
        for m in range(intersection_obj.x_dir):
            if junction_obj[n][m] != 0:
                junction_obj[n][m].addJunction(0.00 + m * intersection_obj.x_length,
                                               0.00 - (n * intersection_obj.y_length))

    edges_obj_pos = []
    edges_obj_min = []

    # Creating Edges
    # Number of edges for multiples intersection
    # For a single intersection, multiple = 1

    mult_num = (2 * intersection_obj.multiple) + (intersection_obj.multiple - 1) + 2

    # print(mult_num)
    for i in range(2 * mult_num):
        if (i % 2) == 0:
            edges_obj_pos.append(edge.Edge(i, ""))
        else:
            edges_obj_min.append(edge.Edge(i, "-"))

    g = Graph(junction_obj, edges_obj_min, edges_obj_pos, intersection_obj)

    g.compute_graph()  # Getting the internal junctions of the network

    # print(g.graph_internal)

    lanes_obj = [lane.Lane(i, intersection_obj, junction_obj) for i in range(intersection_obj.num_lanes)]

    edg_obj = g.graph_edges_min + g.graph_edges_pos

    root = Element('net')

    # Generate normal edges and add lanes to each edge
    edg_elements = [Element('edge') for i in range(len(edg_obj))]

    for e, i in zip(edg_obj, range(len(edg_obj))):
        root.append(edg_elements[i])
        for k in lanes_obj:
            root = e.generateXMLE(root, k, edg_elements[i])

    tls_list = ""

    # Create possible traffic lights
    if len(intersection_obj.tl) != 0 or intersection_obj.tlall or len(intersection_obj.tlnotall):
        tls_obj = traffic_light.TrafficLight(junction_obj, intersection_obj)
        tls_list = " "
        tls_list = tls_obj.set_tls()

    add_polygon = False

    if intersection_obj.building:
        poly = polygon.Polygon(intersection_obj)

        poly.generate_polygon()

        add_polygon = True

    connect = connection.Connection(g, intersection_obj)
    root = connect.set_connection(root)

    for i in range(intersection_obj.x_dir):
        for j in range(intersection_obj.y_dir):
            if junction_obj[j][i] != 0:
                root = junction_obj[j][i].generateXMLJ(root)
                # print(junction_obj[j][i].incoming_edges, junction_obj[j][i].outgoing_edges)

    tree = ElementTree(root)

    indent(root)

    path = os.getcwd()

    tree.write(open(r'{}/road_networks/intersection.net.xml'.format(path), 'wb'), encoding="utf-8",
               xml_declaration=True)

    p = subprocess.Popen(['./sumoNetconvert.sh "{}" "{}" '.format(intersection_obj.name, tls_list)], shell=True,
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.STDOUT)
    p.wait()

    if add_traffic:
        print("Traffic generation starting ...")
        subPTraffic = subprocess.Popen(['./sumoTrafficGen.sh "{}" "{}" '.format(intersection_obj.name, add_polygon)],
                                       shell=True)
        subPTraffic.wait()

    config.create_config(intersection_obj.name, add_polygon, add_traffic)
