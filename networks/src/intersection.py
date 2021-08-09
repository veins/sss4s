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

class Intersection:

    def __init__(self, name, leg_length_x, leg_length_y, lanes, tlall, tl, tlnotall, multiple1, speed, building, building_margin):
        self.name = name
        self.multiple = multiple1
        self.x_dir = self.multiple + 2
        self.y_dir = 3
        self.x_length = leg_length_x
        self.y_length = leg_length_y
        self.num_lanes = lanes
        self.speed = speed
        self.tl = tl
        self.tlall = tlall
        self.tlnotall = tlnotall
        self.direction = True
        self.building = building
        self.building_margin = building_margin
