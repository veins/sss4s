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
from itertools import zip_longest
from xml.etree.ElementTree import Element

from . import internaled


class Connection:

    def __init__(self, gr, netw_obj1):
        self.fr = ""
        self.to = ""
        self.fromLane = "0"
        self.totalLane = "0"
        self.dir = ""
        self.state = ""
        self.via = ""
        self.tl = ""
        self.gr = gr
        self.counter_1 = 0
        self.counter_2 = 0
        self.netw_obj = netw_obj1
        self.internal_edges = []
        self.dict_conn = {}
        self.root = ""
        self.linkIndex = 0
        self.edge_hop = {1: 'l', 2: 's', 3: 'r'}
        self.left_lanes = 1
        self.right_lanes = 1

    def dict_connect(self):
        self.dict_conn['from'] = self.fr
        self.dict_conn['to'] = self.to
        self.dict_conn['fromLane'] = self.fromLane
        self.dict_conn['toLane'] = self.totalLane
        self.dict_conn["dir"] = self.dir
        self.dict_conn["via"] = self.via
        self.dict_conn["state"] = "M"
        # self.dict_conn['linkIndex'] = self.linkIndex

        # self.dict_conn['tl'] = self.tl
        # self.dict_conn["pass"] = "false"

    def add_dict(self, key, value):
        self.dict_conn[key] = value

    def generate_conn_XML(self, graph_junction, *args):
        """Add the connection in the .net.xml-file

        Args:
            graph_junction (list): List of junctions
        """

        # Create the internal edge
        a = internaled.InternalEdge(graph_junction, self.counter_1, self.netw_obj)

        # If self.dir = 's', create multiple internal lanes
        b = a.setLanes(self.root, self.dir)
        self.root = b[1]
        for i, j in zip(b[0], range(self.netw_obj.num_lanes)):
            self.via = i
            self.create_connection_xml(graph_junction)
            self.linkIndex += 1
            break

        self.counter_1 += 1

    def create_connection_xml(self, graph_junction1):

        self.dict_connect()

        # print(self.fr, self.to, self.fromLane, self.fromLane, self.linkIndex)
        conn_element = Element('connection')
        conn_element_2 = Element('connection')

        self.root.append(conn_element)

        for key in self.dict_conn.keys():
            conn_element.set("{}".format(key), "{}".format(self.dict_conn[key]))

        self.dict_conn['from'] = ":{}_{}".format(graph_junction1.id, self.counter_1)

        self.root.append(conn_element_2)

        for key in self.dict_conn.keys():
            if key == 'linkIndex':
                pass
            elif key != 'via':
                conn_element_2.set("{}".format(key), "{}".format(self.dict_conn[key]))

    def create_connection(self, tjunction, incoming_edge, outcoming_edge, incoming_lane, outcoming_lane, direction):
        # tjunction: junction object
        # incoming lane (list) 
        # outcoming lane (list)

        # Equal the length of lists of both lists (incoming_lane, outcoming_lane)
        # Right now, assumption: len(incoming_len) <= len(outcoming_lane)
        # Extend the length of the list 'incoming_lane' with the last element of the list 'incoming_lane'
        # until it reaches of the length of 'outcoming_lane'
        incoming_lane, outcoming_lane = (list(x) for x in (zip(*zip_longest(list(incoming_lane), list(outcoming_lane),
                                                                            fillvalue=incoming_lane[
                                                                                len(incoming_lane) - 1]))))

        # print(tjunction.id,'len',len(tjunction.incoming_edges),'incoming',incoming_lane,'outcoming',
        # outcoming_lane, 'direction', direction)

        self.fr = incoming_edge
        self.to = outcoming_edge
        self.dir = direction

        # print(self.dir)
        incoming_outcoming_lane = list(zip(incoming_lane, outcoming_lane))

        for i in incoming_outcoming_lane:
            self.fromLane = int(i[0])
            self.totalLane = int(i[1])
            self.generate_conn_XML(tjunction)

    def check_direction(self, tjunction, edge_hop):
        """
            Check the direction up, down, left, right
            Set here self.dir == the direction of the lanes
            You can something with edge_hop parameter
            Make the number of left lanes dynamic
        """

        if self.netw_obj.num_lanes == 1:
            one_lane = 1
        else:
            one_lane = 0

        if len(tjunction.incoming_edges) == 2:

            for edge_incoming in tjunction.all_direction_incoming:
                if edge_incoming != 0 and tjunction.all_direction_outcoming[
                    (tjunction.all_direction_incoming.index(edge_incoming) + edge_hop) % len(
                            tjunction.all_direction_outcoming)] != 0:
                    edge_outcoming = tjunction.all_direction_outcoming[
                        (tjunction.all_direction_incoming.index(edge_incoming) + edge_hop) % len(
                            tjunction.all_direction_outcoming)]

                    # Define the lanes that should be connected together
                    lane_ingoing = range(0, self.netw_obj.num_lanes)
                    lane_outgoing = range(0, self.netw_obj.num_lanes)

                    self.create_connection(tjunction, edge_incoming, edge_outcoming, lane_ingoing, lane_outgoing,
                                           self.edge_hop[edge_hop])

        else:

            for edge_incoming in tjunction.all_direction_incoming:
                # second statement - circular indexing
                if edge_incoming != 0 and tjunction.all_direction_outcoming[
                    (tjunction.all_direction_incoming.index(edge_incoming) + edge_hop) % len(
                            tjunction.all_direction_outcoming)] != 0:

                    edge_outcoming = tjunction.all_direction_outcoming[
                        (tjunction.all_direction_incoming.index(edge_incoming) + edge_hop) % len(
                            tjunction.all_direction_outcoming)]

                    # Go clockwise
                    # left - lane view
                    if edge_hop == 1:

                        # Check whether the current edge can have straight lanes
                        # If not, add additional left lanes
                        if tjunction.all_direction_outcoming[
                            (tjunction.all_direction_incoming.index(edge_incoming) + 2) % len(
                                    tjunction.all_direction_outcoming)] != 0:

                            lane_ingoing = range(self.netw_obj.num_lanes - 1,
                                                 self.netw_obj.num_lanes - 1 - self.left_lanes, -1)

                            lane_outgoing = range(self.netw_obj.num_lanes - 1,
                                                  self.netw_obj.num_lanes - 1 - self.left_lanes, -1)

                        else:

                            lane_ingoing = range(self.netw_obj.num_lanes - 1,
                                                 self.netw_obj.num_lanes - 1 - self.left_lanes, -1)

                            lane_outgoing = range(self.netw_obj.num_lanes - 1,
                                                  self.netw_obj.num_lanes - 1 - self.left_lanes, -1)

                    # straight
                    if edge_hop == 2:
                        lane_ingoing = range(0, self.netw_obj.num_lanes - self.left_lanes + 1)
                        lane_outgoing = range(0, self.netw_obj.num_lanes - self.left_lanes + 1)

                    # right - lane view
                    if edge_hop == 3:

                        # Check whether the current edge can have straight lanes
                        # If not, add additional right lanes
                        if tjunction.all_direction_outcoming[
                            (tjunction.all_direction_incoming.index(edge_incoming) + 2) % len(
                                    tjunction.all_direction_outcoming)] != 0:

                            lane_ingoing = range(0, self.right_lanes)
                            lane_outgoing = range(0, self.netw_obj.num_lanes - self.left_lanes + 1)


                        else:

                            lane_ingoing = range(0, self.netw_obj.num_lanes // 2 + 1)
                            lane_outgoing = range(0, self.netw_obj.num_lanes // 2 + 1)

                    self.create_connection(tjunction, edge_incoming, edge_outcoming, lane_ingoing, lane_outgoing,
                                           self.edge_hop[edge_hop])

    def default_connection(self):
        pass

    def user_defined_connection(self):
        pass

    # Setting Connection for each direction,1 lane in each direction, plain links
    def set_connection(self, root1):
        """Iterating over the linked lists containing junctions. Then examining, whether the junctions
        have traffic lights. Information needed for the connection. Then it is checked, how many 
        junctions the incoming edges, the junctions are containing. It is needed to draw the connections.

        Args:
            root1 ([xml]): [description]

        Returns:
            [xml]: [description]
        """
        self.root = root1

        for i in range(len(self.gr.graph_junctions)):
            for j in range(len(self.gr.graph_junctions[i])):
                if self.gr.graph_junctions[i][j] != 0:
                    self.gr.graph_junctions[i][j].setPriority()
                    self.counter_1 = 0
                    if self.gr.graph_junctions[i][j].type == "priority":
                        for k in range(1, 4):
                            self.check_direction(self.gr.graph_junctions[i][j], k)

        return self.root
