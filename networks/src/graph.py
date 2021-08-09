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

class Graph:
    def __init__(self, matrix_junctions, list_edges_pos, list_edges_min, netw_obj):
        """Creates connections between junctions and edges """

        self.graph_junctions = matrix_junctions
        self.graph_edges_pos = list_edges_pos
        self.graph_edges_min = list_edges_min
        self.netw_obj = netw_obj

    def compute_graph(self):
        k = list(zip(self.graph_edges_pos, self.graph_edges_min))

        counter = 0

        # Connect junctions with edges from up to down
        for i in range(len(self.graph_junctions) - 1):
            for j in range(len(self.graph_junctions[i])):

                if self.graph_junctions[i][j] != 0:
                    if self.graph_junctions[i + 1][j] != 0:
                        # print(self.graph_junctions[i+1][j].id)
                        self.graph_junctions[i + 1][j].status = "down"
                        self.graph_junctions[i][j].status = "up"

                        k[counter][0].addEdge(self.graph_junctions[i][j], self.graph_junctions[i + 1][j])

                        # Down
                        self.graph_junctions[i][j].all_direction_outcoming[2] = k[counter][0].id
                        self.graph_junctions[i + 1][j].all_direction_incoming[0] = k[counter][0].id

                        k[counter][1].addEdge(self.graph_junctions[i + 1][j], self.graph_junctions[i][j])

                        self.graph_junctions[i][j].all_direction_incoming[2] = k[counter][1].id
                        self.graph_junctions[i + 1][j].all_direction_outcoming[0] = k[counter][1].id

                        # print('first',k[counter][0].id, k[counter][1].id)

                        # It is necessary that I later can set the attribute length of the lane correctly
                        self.setting_length_lane(counter, k)
                        counter = counter + 1

                        # Connect junctions with edges from right to left
        for i in range(len(self.graph_junctions)):
            if self.netw_obj.name == "intersection":
                if i != 0 and i != (len(self.graph_junctions) - 1):
                    for j in range(len(self.graph_junctions[i]) - 1):
                        if j != range(len(self.graph_junctions[i]) - 1):
                            if self.graph_junctions[i][j] != 0:
                                self.graph_junctions[i][j + 1].status = "left"
                                self.graph_junctions[i][j].status = "right"

                                k[counter][0].addEdge(self.graph_junctions[i][j], self.graph_junctions[i][j + 1])

                                self.graph_junctions[i][j + 1].all_direction_incoming[3] = k[counter][0].id
                                self.graph_junctions[i][j].all_direction_outcoming[1] = k[counter][0].id

                                k[counter][1].addEdge(self.graph_junctions[i][j + 1], self.graph_junctions[i][j])
                                # print('fifth',k[counter][0].id, k[counter][1].id)

                                self.graph_junctions[i][j].all_direction_incoming[1] = k[counter][1].id
                                self.graph_junctions[i][j + 1].all_direction_outcoming[3] = k[counter][1].id

                                self.setting_length_lane(counter, k)
                                counter = counter + 1


            else:
                for j in range(len(self.graph_junctions[i]) - 1):
                    if j != range(len(self.graph_junctions[i]) - 1):
                        if self.graph_junctions[i][j] != 0:
                            self.graph_junctions[i][j + 1].status = "right"
                            self.graph_junctions[i][j].status = "left"

                            k[counter][0].addEdge(self.graph_junctions[i][j], self.graph_junctions[i][j + 1])

                            self.graph_junctions[i][j + 1].all_direction_incoming[3] = k[counter][0].id
                            self.graph_junctions[i][j].all_direction_outcoming[1] = k[counter][0].id

                            k[counter][1].addEdge(self.graph_junctions[i][j + 1], self.graph_junctions[i][j])

                            self.graph_junctions[i][j].all_direction_incoming[1] = k[counter][1].id
                            self.graph_junctions[i][j + 1].all_direction_outcoming[3] = k[counter][1].id

                            self.setting_length_lane(counter, k)
                            counter = counter + 1

    def setting_length_lane(self, counter, k):
        k[counter][0].lengthforlane = self.netw_obj.x_length
        k[counter][1].lengthforlane = self.netw_obj.x_length
