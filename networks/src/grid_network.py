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
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import ElementTree

from . import config
from .base import connection, edge, lane, junction, polygon, traffic_light
from . import grid
from .graph import Graph


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


def create_grid(name, grid_x_length, grid_y_length, grid_x_dir, grid_y_dir, lanes, tlall, tl, tlnotall, speed, building,
                building_margin, add_traffic):
    grid_obj = grid.Grid(name, grid_x_length, grid_y_length, grid_x_dir, grid_y_dir, lanes, tlall, tl, tlnotall, speed,
                         building, building_margin)

    counter = 0

    junction_obj = []

    for i in range(grid_obj.y_dir):
        a = []
        for y in range(grid_obj.x_dir):
            a.append(junction.Junction(counter, grid_obj))
            counter += 1
        junction_obj.append(a)

    lanes_obj = [lane.Lane(i, grid_obj, junction_obj) for i in range(grid_obj.num_lanes)]

    # Setting the positions of junction
    for n in range(grid_obj.y_dir):
        for m in range(grid_obj.x_dir):
            if junction_obj[n][m] != 0:
                junction_obj[n][m].addJunction(0.00 + m * grid_obj.x_length, 0.00 - (n * grid_obj.y_length))

    edges_obj_pos = []
    edges_obj_min = []

    # Creating Edges
    # Number of edges for grid
    d = 2 * (grid_obj.x_dir - 1) * grid_obj.y_dir + 2 * (grid_obj.y_dir - 1) * grid_obj.x_dir

    for i in range(d):
        if (i % 2) == 0:
            edges_obj_pos.append(edge.Edge(i, "incoming"))
        else:
            edges_obj_min.append(edge.Edge(i, "outcoming"))

    g = Graph(junction_obj, edges_obj_min, edges_obj_pos, grid_obj)

    g.compute_graph()  # Getting the internal junctions of the network

    edg_obj = g.graph_edges_min + g.graph_edges_pos

    root = Element('net')

    # Generate normal edges
    edg_elements = [Element('edge') for i in range(len(edg_obj))]

    for e, i in zip(edg_obj, range(len(edg_obj))):
        root.append(edg_elements[i])
        for k in lanes_obj:
            root = e.generateXMLE(root, k, edg_elements[i])

    tls_list = ""

    # Create possible traffic lights
    if len(grid_obj.tl) != 0 or grid_obj.tlall or len(grid_obj.tlnotall):
        tls_obj = traffic_light.TrafficLight(junction_obj, grid_obj)
        tls_list = " "
        tls_list = tls_obj.set_tls()

    add_polygon = False

    # Create buildings
    if grid_obj.building:
        poly = polygon.Polygon(grid_obj)
        poly.generate_polygon()
        add_polygon = True

    connect = connection.Connection(g, grid_obj)
    root = connect.set_connection(root)

    for n in range(grid_obj.y_dir):
        for m in range(grid_obj.x_dir):
            if junction_obj[n][m] != 0:
                root = junction_obj[n][m].generateXMLJ(root)

    tree = ElementTree(root)

    indent(root)

    path = os.getcwd()

    tree.write(open(r'{}/road_networks/{}.net.xml'.format(path, grid_obj.name), 'wb'), encoding="utf-8",
               xml_declaration=True)

    p = subprocess.Popen(['./sumoNetconvert.sh "{}" "{}" '.format(grid_obj.name, tls_list)], shell=True,
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.STDOUT)
    p.wait()
    if add_traffic:
        print("Traffic generation starting ...")
        subP = subprocess.Popen(['./sumoTrafficGen.sh "{}" "{}" '.format(grid_obj.name, add_polygon)], shell=True)
        subP.wait()
    config.create_config(grid_obj.name, add_polygon, add_traffic)
