# 5GCity-resource-placement

## Scope

Intelligent resource placement module for 5GCity distributed cloud and radio platform.

*The main goal of the algorith is to take into consideration the network topology and the access points locations in determining the best option for placing the VNFs that compose a Network Service.* 

## Input 

1) Network Service (NS) placement request
2) Device (Network) graph - a description of the available nodes (data-center, edge) and the interconnections between them
3) Available resources per device - CPU, Memory, Storage
4) Connection links capacity
5) NS user gateway - the end node where the NS user is connected 

  *In 5GCity, we can assume that end users of a NS are the SCs and the WiFi APs and the NS gateway is the edge or DC node to which they have a direct connection*

## Output

The output of the module is one or a group of devices where the NS should be placed.

## API Usage

### POST Endpoint  http://localhost:3800/placement/

Triggers the placement algorithm. The needed input information is extracted from the slice data (compute and network chunks, resources, links).

- Asynchronous, returns an id of the request.
- The result can be obtained by GET /placement/{placement-id}

#### Body Example 
```
{
  "fwchain": {
    "source": [
      {
        "node": "pop0",
        "vnf": "vnf_user",
        "flows": [
          {
            "data_rate": 1,
            "id": "f1"
          }
        ]
      }
    ],
    "vnfs": [
      {
        "name": "vnf_user",
        "inputs_fwd": 0,
        "inputs_bwd": 0,
        "outputs_fwd": 1,
        "outputs_bwd": 0,
        "out_fwd": [],
        "out_bwd": [],
        "mem": [
          2
        ],
        "cpu": [
          2
        ],
        "vnf_delay": 0,
        "stateful": false,
        "type": "source"
      },
      {
        "name": "vnf_fw1",
        "inputs_fwd": 1,
        "inputs_bwd": 0,
        "outputs_fwd": 1,
        "outputs_bwd": 0,
        "out_fwd": [
          [
            1,
            0
          ]
        ],
        "out_bwd": [],
        "mem": [
          4,
          32
        ],
        "cpu": [
          8,
          16
        ],
        "vnf_delay": 35,
        "stateful": false,
        "type": "normal"
      },
      {
        "name": "vnf_web",
        "inputs_fwd": 1,
        "inputs_bwd": 0,
        "outputs_fwd": 0,
        "outputs_bwd": 0,
        "mem": [
          8,
          0
        ],
        "cpu": [
          8,
          0
        ],
        "out_fwd": [],
        "out_bwd": [],
        "vnf_delay": 20,
        "stateful": false,
        "type": "normal"
      }
    ],
    "name": "fw1chain",
    "vlinks": [
      {
        "dest": "vnf_fw1",
        "src": "vnf_user",
        "direction": "forward",
        "dest_input": 0,
        "src_output": 0,
        "max_delay": 50
      },
      {
        "dest": "vnf_web",
        "src": "vnf_fw1",
        "direction": "forward",
        "dest_input": 0,
        "src_output": 0,
        "max_delay": 50
      }
    ]
  },
  "network": {
    "directed": false,
    "graph": {
      "node_default": {},
      "edge_default": {}
    },
    "nodes": [
      {
        "mem": 2,
        "cpu": 2,
        "id": 0
      },
      {
        "mem": 4,
        "cpu": 16,
        "id": 1
      },
      {
        "mem": 8,
        "cpu": 32,
        "id": 2
      },
      {
        "mem": 8,
        "cpu": 32,
        "id": 3
      }
    ],
    "links": [
      {
        "source": 0,
        "target": 1
      },
      {
        "source": 0,
        "target": 2
      },
      {
        "source": 1,
        "target": 3
      }
    ],
    "multigraph": false
  }
}
```
#### Response 

- {placement-id}: id of the placement request as body
- Response codes: 202 Accepted,  400 Bad Request

### GET Endpoint http://localhost:3800/placement/{placement-id}

#### Response

Body example
```
{
    "placement": {
        "vnfs": [
            {
                "name": "vnf_fw1",
                "node": "pop1"
            },
            {
                "name": "vnf_user",
                "node": "pop0"
            },
            {
                "name": "vnf_web",
                "node": "pop3"
            }
        ],
        "vlinks": [
            {
                "src_vnf": "vnf_fw1",
                "src_node": "pop1",
                "dest_vnf": "vnf_web",
                "dest_node": "pop3"
            },
            {
                "src_vnf": "vnf_user",
                "src_node": "pop0",
                "dest_vnf": "vnf_fw1",
                "dest_node": "pop1"
            }
        ],
        "cpu_oversub": [],
        "mem_oversub": [],
        "dr_oversub": [],
        "alloc_node_res": [
            {
                "name": "vnf_fw1",
                "node": "pop1",
                "cpu": 8,
                "mem": 4
            },
            {
                "name": "vnf_user",
                "node": "pop0",
                "cpu": 2,
                "mem": 2
            },
            {
                "name": "vnf_web",
                "node": "pop3",
                "cpu": 8,
                "mem": 8
            }
        ],
        "flows": [
            {
                "arc": "vnf_fw1.0->vnf_web.0",
                "src_node": "pop1",
                "dst_node": "pop3",
                "src_vnf": "vnf_fw1",
                "dest_vnf": "vnf_web",
                "flow_id": "f1"
            },
            {
                "arc": "vnf_user.0->vnf_fw1.0",
                "src_node": "pop0",
                "dst_node": "pop1",
                "src_vnf": "vnf_user",
                "dest_vnf": "vnf_fw1",
                "flow_id": "f1"
            }
        ],
        "links": [
            {
                "arc": "vnf_fw1.0->vnf_web.0",
                "edge_src": "pop1",
                "edge_dst": "pop3",
                "link_src": "pop1",
                "link_dst": "pop3"
            },
            {
                "arc": "vnf_user.0->vnf_fw1.0",
                "edge_src": "pop0",
                "edge_dst": "pop1",
                "link_src": "pop0",
                "link_dst": "pop1"
            }
        ]
    },
    "metrics": {
        "num_instances": 3,
        "max_cpu_oversub": 0,
        "max_mem_oversub": 0,
        "changed": [
            {
                "name": "vnf_fw1",
                "node": "pop1"
            },
            {
                "name": "vnf_user",
                "node": "pop0"
            },
            {
                "name": "vnf_web",
                "node": "pop3"
            }
        ],
        "num_changed": 3,
        "path_delays": [
            {
                "src": "vnf_fw1",
                "dest": "vnf_web",
                "src_node": "pop1",
                "dest_node": "pop3",
                "path_delay": 0
            },
            {
                "src": "vnf_user",
                "dest": "vnf_fw1",
                "src_node": "pop0",
                "dest_node": "pop1",
                "path_delay": 0
            }
        ],
        "vnf_delays": [
            {
                "vnf": "vnf_fw1",
                "vnf_delay": 35
            },
            {
                "vnf": "vnf_user",
                "vnf_delay": 0
            },
            {
                "vnf": "vnf_web",
                "vnf_delay": 20
            }
        ],
        "total_path_delay": 0,
        "total_vnf_delay": 55,
        "max_endToEnd_delay": 55,
        "total_delay": 55,
        "max_dr_oversub": 0
    },
    "id": "7da2d000-b104-4c52-93b5-64863a01a3b3"
}
```

Response codes: 200 OK, 404 Item Not Found

## Setup

```
python setup.py install
```
Requires Python 3.5+

Run `placement` to start the server



### This algorithm is based on the following work:

> Sevil Dräxler, Stefan Schneider, Holger Karl: "[Scaling and Placing Bidirectional Services with Stateful Virtual and Physical Network Functions](https://ieeexplore.ieee.org/document/8459915/)". IEEE Conference on Network Softwarization (NetSoft), Montreal, CA (2018)


"B-JointSP is an optimization problem focusing on the *joint scaling and placemen*t (called embedding) of NFV network services, consisting of interconnected virtual network functions (VNFs). The exceptional about B-JointSP is its consideration of *realistic, bidirectional network services*, in which flows return to their sources. It even supports *stateful VNFs*, that need to be traversed by the same flows in both upstream and downstream direction. Furthermore, B-JointSP allows the reuse of VNFs across different network services and supports physical network functions."
