#!/usr/bin/python3
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
import argparse
import os
import sys
from src import freeway_network, intersection_network, grid_network, __version__, __label__
from test import freewaytest, intersectiontest, gridtest

from src.base.xmlCommenter import writeDocumentation


def main():
    arg_parser = argparse.ArgumentParser()
    parser = arg_parser.add_subparsers()

    freeway_parser = parser.add_parser("freeway", help="")
    intersection_parser = parser.add_parser("intersection", help="")
    grid_chicago_parser = parser.add_parser("grid_chicago", help="")
    grid_manhattan_parser = parser.add_parser("grid_manhattan", help="")

    # Create Options for freeway
    freeway_parser.add_argument("-b", "--bidirectional", default=False, action='store_true',
                                help="Generates both directions (default: false)")
    freeway_parser.add_argument("-l", "--lanes", default=4, type=int, help="Number of lanes per direction (default: 4)")
    freeway_parser.add_argument("-len", "--length", default=250, type=float,
                                help="Length for each lane (in meters, default:250)")
    freeway_parser.add_argument("-s", "--speed", default=27.778, type=float,
                                help="The maximum speed for vehicles (default: 27.778 m/s)")
    freeway_parser.add_argument("-t", "--traffic", default=False, action='store_true',
                                help="If true, sss4s will generate artificial traffic for the scenario (default: false)")

    # Create Options for Intersection
    intersection_parser.add_argument("-m", "--multiple", default=1, type=int)
    intersection_parser.add_argument("-x-len", "--intersection_x_length", default=100, type=float)
    intersection_parser.add_argument("-y-len", "--intersection_y_length", default=100, type=float)
    intersection_parser.add_argument("-s", "--speed", default=13.89, type=float)
    intersection_parser.add_argument("-l", "--lanes", default=1, type=int)
    intersection_parser.add_argument("-tl-all", "--traffic_light_all", action='store_true')
    intersection_parser.add_argument("-tl", "--traffic_light", default=[], nargs='+')
    intersection_parser.add_argument("-tl-notall", "--traffic_light_notall", default=[], nargs='+')
    intersection_parser.add_argument("-p", "--polygon", action='store_true')
    intersection_parser.add_argument("-pm", "--polygon_margin", default=5, type=int)
    intersection_parser.add_argument("-t", "--traffic", default=False, action='store_true',
                                     help="If true, sss4s will generate artificial traffic for the scenario (default: "
                                          "false)")

    # Create Options for Grid_Chicago
    grid_chicago_parser.add_argument("-x-len", "--grid_x_length", default=160, type=float)
    grid_chicago_parser.add_argument("-y-len", "--grid_y_length", default=70, type=float)
    grid_chicago_parser.add_argument("-x-dir", "--grid_x_direction", default=4, type=int)
    grid_chicago_parser.add_argument("-y-dir", "--grid_y_direction", default=4, type=int)
    grid_chicago_parser.add_argument("-l", "--lanes", default=1, type=int)
    grid_chicago_parser.add_argument("-tl-all", "--traffic_light_all", action='store_true')
    grid_chicago_parser.add_argument("-tl", "--traffic_light", default=[], nargs='+')
    grid_chicago_parser.add_argument("-tl-notall", "--traffic_light_notall", default=[], nargs='+')
    grid_chicago_parser.add_argument("-p", "--polygon", action='store_true')
    grid_chicago_parser.add_argument("-s", "--speed", default=13.89, type=float)
    grid_chicago_parser.add_argument("-pm", "--polygon_margin", default=5, type=int)
    grid_chicago_parser.add_argument("-t", "--traffic", default=False, action='store_true',
                                     help="If true, sss4s will generate artificial traffic for the scenario (default: false)")

    # Create Options for Grid_Manhattan
    grid_manhattan_parser.add_argument("-len", "--grid_length_bothdirections", default=60, type=float)
    grid_manhattan_parser.add_argument("-x-dir", "--grid_x_direction", default=4, type=int)
    grid_manhattan_parser.add_argument("-y-dir", "--grid_y_direction", default=4, type=int)
    grid_manhattan_parser.add_argument("-l", "--lanes", default=1, type=int)
    grid_manhattan_parser.add_argument("-tl-all", "--traffic_light_all", action='store_true')
    grid_manhattan_parser.add_argument("-tl", "--traffic_light", default=[], nargs='+')
    grid_manhattan_parser.add_argument("-tl-notall", "--traffic_light_notall", default=[], nargs='+')
    grid_manhattan_parser.add_argument("-p", "--polygon", action='store_true')
    grid_manhattan_parser.add_argument("-s", "--speed", default=13.89, type=float)
    grid_manhattan_parser.add_argument("-pm", "--polygon_margin", default=5, type=int)
    grid_manhattan_parser.add_argument("-t", "--traffic", default=False, action='store_true',
                                       help="If true, sss4s will generate artificial traffic for the scenario (default: false)")

    args = arg_parser.parse_args()

    dir_road_networks = "road_networks"
    if not os.path.exists(dir_road_networks):
        os.makedirs(dir_road_networks)

    if len(sys.argv) == 1:
        sys.exit("Use --help to get the list of options.")
    if sys.argv[1] == "freeway":
        print("Generating freeway ...")
        freeway_test = freewaytest.TestFreeway(args.lanes, args.length, args.speed)
        freeway_test.test_freeway()
        freeway_network.create_freeway(args.bidirectional, args.lanes, args.length, args.speed, args.traffic)

    if sys.argv[1] == "intersection":
        print("Generating intersection ...")
        intersection_test = intersectiontest.TestIntersection(args.intersection_x_length,
                                                              args.intersection_y_length, args.lanes,
                                                              args.multiple, args.speed,
                                                              args.polygon)
        intersection_test.test_intersection()
        intersection_network.create_intersection("intersection", args.intersection_x_length, args.intersection_y_length,
                                                 args.lanes, args.traffic_light_all, args.traffic_light,
                                                 args.traffic_light_notall, args.multiple, args.speed, args.polygon,
                                                 args.polygon_margin,
                                                 args.traffic)

    if sys.argv[1] == "grid_chicago":
        print("Generating Chicago grid ...")
        grid_test = gridtest.TestGrid(args.grid_x_length, args.grid_y_length, args.grid_x_direction,
                                      args.grid_y_direction, args.lanes, args.speed)
        grid_test.test_grid()
        grid_network.create_grid("grid", args.grid_x_length, args.grid_y_length, args.grid_x_direction,
                                 args.grid_y_direction, args.lanes, args.traffic_light_all, args.traffic_light,
                                 args.traffic_light_notall, args.speed, args.polygon, args.polygon_margin, args.traffic)

    if sys.argv[1] == "grid_manhattan":
        print("Generating Manhattan grid ...")
        grid_network.create_grid("grid", args.grid_length_bothdirections, args.grid_length_bothdirections,
                                 args.grid_x_direction, args.grid_y_direction, args.lanes, args.traffic_light_all,
                                 args.traffic_light, args.traffic_light_notall, args.speed, args.polygon,
                                 args.polygon_margin, args.traffic)

    # Write sss4s parameters to XML
    writeDocumentation(sys.argv[1], args)


if __name__ == "__main__":
    print(__label__ + " Version " + str(__version__) + "\n" +
          "Copyright (C) 2021 \n" +
          "License GPL-2.0-or-later: https://spdx.org/licenses/GPL-2.0-or-later.html\n")
    main()
