#!/bin/bash

scenario_name=$1
traffic_light=$2

if [ -z "${traffic_light}" ]
then
    ${SUMO_HOME}/bin/netconvert --sumo-net-file $PWD/road_networks/${scenario_name}.net.xml --output-file $PWD/road_networks/${scenario_name}.net.xml 
else
    ${SUMO_HOME}/bin/netconvert --sumo-net-file $PWD/road_networks/${scenario_name}.net.xml --output-file $PWD/road_networks/${scenario_name}.net.xml --tls.set ${traffic_light}
fi

