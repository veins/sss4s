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
import subprocess
from datetime import date
from xml.dom import minidom
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET
import os


def writeDocumentation(param, args):
    # launch SUMO netconvert to get information about the current version
    process = subprocess.run(["netconvert"], capture_output=True)
    netconvertOutput = process.stdout.decode("utf-8")

    sss4sE = Element('ss4sConfiguration')
    inputE = Element("input")

    if param == "freeway":
        ET.SubElement(inputE, 'direction', {'value': str(args.bidirectional)})
        ET.SubElement(inputE, 'lanes', {'value': str(args.lanes)})
        ET.SubElement(inputE, 'length', {'value': str(args.length)})
        ET.SubElement(inputE, 'speed', {'value': str(args.speed)})
        filename = os.getcwd() + '/road_networks/freeway.net.xml'

    if param == "intersection":
        ET.SubElement(inputE, 'intersection_x_length', {'value': str(args.intersection_x_length)})
        ET.SubElement(inputE, 'intersection_y_length', {'value': str(args.intersection_y_length)})
        ET.SubElement(inputE, 'lanes', {'value': str(args.lanes)})
        ET.SubElement(inputE, 'traffic_light_all', {'value': str(args.traffic_light_all)})
        ET.SubElement(inputE, 'traffic_light', {'value': str(args.traffic_light)})
        ET.SubElement(inputE, 'traffic_light_notall', {'value': str(args.traffic_light_notall)})
        ET.SubElement(inputE, 'multiple', {'value': str(args.multiple)})
        ET.SubElement(inputE, 'speed', {'value': str(args.speed)})
        ET.SubElement(inputE, 'polygon', {'value': str(args.polygon)})
        ET.SubElement(inputE, 'traffic', {'value': str(args.traffic)})
        filename = os.getcwd() + '/road_networks/intersection.net.xml'

    if param == "grid_chicago":
        ET.SubElement(inputE, 'grid_x_length', {'value': str(args.grid_x_length)})
        ET.SubElement(inputE, 'grid_y_length', {'value': str(args.grid_y_length)})
        ET.SubElement(inputE, 'grid_x_direction', {'value': str(args.grid_x_direction)})
        ET.SubElement(inputE, 'grid_y_direction', {'value': str(args.grid_y_direction)})
        ET.SubElement(inputE, 'lanes', {'value': str(args.lanes)})
        ET.SubElement(inputE, 'traffic_light_all', {'value': str(args.traffic_light_all)})
        ET.SubElement(inputE, 'traffic_light', {'value': str(args.traffic_light)})
        ET.SubElement(inputE, 'traffic_light_notall', {'value': str(args.traffic_light_notall)})
        ET.SubElement(inputE, 'speed', {'value': str(args.speed)})
        ET.SubElement(inputE, 'polygon', {'value': str(args.polygon)})
        filename = os.getcwd() + '/road_networks/grid.net.xml'

    if param == "grid_manhattan":
        ET.SubElement(inputE, 'grid_length_bothdirections', {'value': str(args.grid_length_bothdirections)})
        ET.SubElement(inputE, 'grid_length_bothdirections', {'value': str(args.grid_length_bothdirections)})
        ET.SubElement(inputE, 'grid_x_direction', {'value': str(args.grid_x_direction)})
        ET.SubElement(inputE, 'grid_y_direction', {'value': str(args.grid_y_direction)})
        ET.SubElement(inputE, 'lanes', {'value': str(args.lanes)})
        ET.SubElement(inputE, 'traffic_light_all', {'value': str(args.traffic_light_all)})
        ET.SubElement(inputE, 'traffic_light', {'value': str(args.traffic_light)})
        ET.SubElement(inputE, 'traffic_light_notall', {'value': str(args.traffic_light_notall)})
        ET.SubElement(inputE, 'speed', {'value': str(args.speed)})
        ET.SubElement(inputE, 'polygon', {'value': str(args.polygon)})
        filename = os.getcwd() + '/road_networks/grid.net.xml'

    with open(filename, 'r') as f:
        data = f.read()
        start = data.find(" generated on") + len(" generated on")
        data = "\n".join(data[start:len(data)].split("\n")[1:-1])

    with open(filename, 'w') as f:
        end = data.find("-->")
        substring = data[end:len(data)]
        sss4sE.append(inputE)
        xmlstr = minidom.parseString(ET.tostring(sss4sE)).toprettyxml(indent="      ")
        f.write("\n<!--generated on " + str(
            date.today()) + " by 'SIMPLE SYNTHETIC SCENARIOS 4 SUMO (sss4s)', cleaned "
                            "with " + netconvertOutput.split("\n")[0] + " \n" + xmlstr + "-->\n" + data[
                                                                                                0:end] + "\n" + data[
                                                                                                                end:len(
                                                                                                                    data)])
        print("Network and SUMO-configuration written to " + os.path.dirname(filename))
