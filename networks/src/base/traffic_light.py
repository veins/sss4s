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


import sys
import logging
from src import input


# Mapping traffic-lights options 
class TrafficLight():
    def __init__(self, junc_obj, netw_obj):
        self.netw_obj = netw_obj
        self.junc_obj = junc_obj
        self.traffic_lights = []

    def input_tl(self, prompt, *args):

        for c in range(len(prompt)):

            prompt[c] = input.check_numbers_valid(prompt[c])

            if self.netw_obj.name == "intersection":

                if 0 <= prompt[c] <= self.netw_obj.multiple - 1:
                    pass
                else:
                    sys.exit("Cannot set traffic light. Junction is not existent")

            elif 0 <= prompt[c] <= self.netw_obj.x_dir * self.netw_obj.y_dir - 1:
                pass

            else:

                sys.exit(
                    "Cannot set traffic light. Junction is not existent. Junction from 0 and {} are only known.".format(
                        self.netw_obj.x_dir * self.netw_obj.y_dir - 1))

        return prompt

    def test_input_tl(self):
        """Test Cases for Input of Traffic Lights
        """
        # Handle "None"
        if len(self.netw_obj.tl) == 0:
            pass
        else:
            self.netw_obj.tl = self.input_tl(self.netw_obj.tl)

        if len(self.netw_obj.tlnotall) == 0:
            pass
        else:

            self.netw_obj.tlnotall = self.input_tl(self.netw_obj.tlnotall)

            # Remove any Duplicates
            self.netw_obj.tlnotall = list(dict.fromkeys(self.netw_obj.tlnotall))

            if len(self.tlnotall) > self.x_dir * self.y_dir:
                sys.exit(
                    "The number of values for traffic lights exceeding the existing number of nodes in the road network.")

    def set_tls(self):

        self.test_input_tl()

        # Adapt the indices of traffic lights (intersection)
        if self.netw_obj.name == "intersection":
            if len(self.netw_obj.tl) != 0:
                for i in self.netw_obj.tl:
                    self.netw_obj.tl[self.netw_obj.tl.index(i)] = str(int(i) + self.netw_obj.multiple + 3)

            if len(self.netw_obj.tlnotall) != 0:
                for i in self.netw_obj.tlnotall:
                    self.netw_obj.tlnotall[self.netw_obj.tlnotall.index(i)] = str(int(i) + self.netw_obj.multiple + 3)

        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

        self.netw_obj.tl = list(map(int, self.netw_obj.tl))
        self.netw_obj.tlnotall = list(map(int, self.netw_obj.tlnotall))

        # Equip only CERTAIN junctions with traffic lights
        if len(self.netw_obj.tl) != 0 or len(self.netw_obj.tlnotall) != 0:
            for n in range(self.netw_obj.y_dir):
                for m in range(self.netw_obj.x_dir):
                    if self.junc_obj[n][m] != 0:
                        self.junc_obj[n][m].setPriority()
                        if self.junc_obj[n][m].type == 'priority':

                            if self.netw_obj.tlall and len(self.netw_obj.tlnotall) != 0:
                                logging.warning(
                                    "Commands -tl-all/--traffic_light_all and -tl-notall/--traffic_light_notall are provided. Only -tl-all/--traffic_light_all is executed.")
                                self.netw_obj.tlall = False

                            if n * self.netw_obj.x_dir + m in self.netw_obj.tl:
                                self.traffic_lights.append(self.junc_obj[n][m].id)

                            if n * self.netw_obj.x_dir + m not in self.netw_obj.tlnotall and len(
                                    self.netw_obj.tlnotall) != 0:
                                if self.junc_obj[n][m].id not in self.traffic_lights:
                                    self.traffic_lights.append(self.junc_obj[n][m].id)

                            # Check whether all junctions should be set with TL
                            if self.netw_obj.tlall:
                                if self.junc_obj[n][m].id not in self.traffic_lights:
                                    self.traffic_lights.append(self.junc_obj[n][m].id)

        self.traffic_lights = ",".join(str(x) for x in self.traffic_lights)

        # return a list with junctions-ids, where a TL should be set
        return self.traffic_lights
