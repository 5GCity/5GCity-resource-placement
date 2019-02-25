# 5GCity-resource-placement

## Scope

Intelligent resource placement module for 5GCity distributed cloud and radio platform.

*The main goal of the algorith is to take into consideration the network topology and the access points locations in determining the best option for placing the VNFs that compose a Network Service.* 

## Configuration

1) Device (Network) graph - a description of the available nodes (data-center, edge) and the interconnections between them
2) Available resources per device - CPU, Memory, Storage
3) Connection links capacity

## Input

Network Service (NS) placement request
- NS description (VNFs, resource requirements)
- NS user gateway - the end node where the NS user is connected 

  *In 5GCity, we can assume that end users of a NS are the SCs and the WiFi APs and the NS gateway is the edge or DC node to which they have a direct connection*

## Output

The output of the module is one or a group of devices where the NS should be placed.




