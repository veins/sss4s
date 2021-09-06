## What is the tool sss4s 

 **sss4s** is a command-line tool, which is able to generate road networks with command-line options. This tool uses certain tools from the road-traffic simulator SUMO and works currently with version 1.8.0 of SUMO.

 Thus, it is important to install the right version of SUMO in order that the tool *sss4s* works.


## How to use the tool sss4s

1. Please make sure, that the *SUMO_HOME* variable is set.

2. Execute the file sss4s.py in the directory networks with below listed
command-line options

3. The *net.xml*-, *add.xml*- and the *rou.xml*-files can be found in the subdirectory
road_networks of the directory networks.

4. Command-line options examples for executing the file sss4s.py
    ``` python sss4s.py intersection -m 2 -tl 0 1 ```
*Explanation: Generates 2 intersections with traffic lights at the junction*
with ID 0 and at the junction with ID 1
    ``` python sss4s.py freeway -b -len 1000 ```
*Explanation: Generates a bidirectional freeway with a road length
of 1000 meters*

5. In order to execute the simulation with the road network in SUMO, use the file with the
extension *.sumocfg*

