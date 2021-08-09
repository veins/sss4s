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

class Grid:

    def __init__(self, name, leg_length_x, leg_length_y, x_dir, y_dir, lanes, tlall, tl, tlnotall, speed, building,
                 building_margin):
        """ Main properties of a grid

        Args:
            name (String): name of the road network(grid_chicago, grid_manhattan)
            leg_length_x (float): length of the road in horizontal direction
            leg_length_y (float): length of the road in vertical direction
            x_dir (int): number of nodes in horizontal direction
            y_dir (int): number of nodes in vertical direction 
            lanes (int): number of lanes per direction
            tlall (bool): equip all nodes with traffic lights
            tl (list): contains a list of junction-ids
            tlnotall (list): contains a list of junction-ids
            speed (float): max speed [m/s] on ALL roads
            building (bool): put at every corner of the intersection an building (polygon)
        """
        self.name = name
        self.x_length = round(float(leg_length_x), 2)
        self.y_length = round(float(leg_length_y), 2)
        self.num_lanes = lanes
        self.x_dir = x_dir
        self.y_dir = y_dir
        self.speed = speed
        self.tlall = tlall
        self.tl = tl
        self.tlnotall = tlnotall
        self.direction = True
        self.building = building
        self.building_margin = building_margin
