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
- The progress can be checked by GET /placement/{placement-id} and reading the status (READY, IN PROGRESS, FAIL).

#### Body Example 
```
{
   TBD ...
   "nsd",
   "slice"
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
    "status: "READY",
    "ns_id":"6b63089158f568073093f70a",
    "placemenet-map":[  
        {  
            "chunk_id":"6b63089158f568073093f70a",
            "vdu_id":"6b63089158f568073093f70a"
        },
        {  
            "chunk_id":"6b63089158f568073093p11c",
            "vdu_id":"6b63089158f568073093f90b"
        }
    ]"
}
```

Response codes: 200 OK, 404 Item Not Found



