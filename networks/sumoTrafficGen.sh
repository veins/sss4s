#!/bin/bash


scenario_name=$1
scenario_add=$2

if [ "$scenario_name" == "freeway" ]
then
    ${SUMO_HOME}/tools/randomTrips.py -n  $PWD/road_networks/${scenario_name}.net.xml --allow-fringe -o $PWD/road_networks/${scenario_name}.trips.xml -e 80 
else
    ${SUMO_HOME}/tools/randomTrips.py -n $PWD/road_networks/${scenario_name}.net.xml -o $PWD/road_networks/${scenario_name}.trips.xml -e 80
fi



#####
# If an add.xml-file then include it in the duarouter
####


if [ "${scenario_add}" == True ]
then
    ${SUMO_HOME}/bin/duarouter --net-file $PWD/road_networks/${scenario_name}.net.xml -a $PWD/road_networks/${scenario_name}.add.xml --route-files $PWD/road_networks/${scenario_name}.trips.xml --output-file $PWD/road_networks/${scenario_name}.rou.xml 2> /dev/null
else
    ${SUMO_HOME}/bin/duarouter --net-file $PWD/road_networks/${scenario_name}.net.xml --route-files $PWD/road_networks/${scenario_name}.trips.xml --output-file $PWD/road_networks/${scenario_name}.rou.xml 2> /dev/null
fi

mv $PWD/road_networks/${scenario_name}.rou.alt.xml $PWD/road_networks/rou_alt_xml


${SUMO_HOME}/tools/assign/duaIterate.py -n $PWD/road_networks/${scenario_name}.net.xml -r $PWD/road_networks/${scenario_name}.rou.xml --begin 0 --end 80 -l 3 
