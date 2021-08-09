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


# Create the configuration file for SUMO


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


def create_config(name, add_polygon, add_traffic):
    root = Element("configuration")

    input_config = Element('input')

    net = Element('net-file')
    net.set("value", "{}.net.xml".format(name))

    route = Element('route-files')
    route.set("value", "{}.rou.xml".format(name))

    additional = Element('additional-files')

    if add_polygon:
        input_config.append(additional)
        additional.set("value", "{}.add.xml".format(name))

    input_config.append(net)

    if add_traffic:
        input_config.append(route)

    root.append(input_config)

    indent(root)

    path = os.getcwd()

    tree = ElementTree(root)
    tree.write(open(r'{}/road_networks/{}.sumocfg'.format(path, name), 'wb'), encoding="utf-8", xml_declaration=True)
