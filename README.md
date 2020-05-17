# infra-community
The repo holds all of the applications running for different communities

# Network Topo for communities

| Community | Region | VPC | Subnet | K8s Cluster | Cluster CIDRs |
| :----:| :----: | :----: | :----: | :----: | :----: |
| openEuler | HongKong | net-community(172.16.0.0./16) | subnet-k8s(172.16.1.0/24) | cce-community | 172.17.0.0/16 |
| MindSpore | HongKong | vpc-9253(192.168.0.0/16) | subnet-9253(192.168.0.0/24) | osinfrastructure | 172.20.0.0/16 |
| MindSpore | BeiJing1 | vpc-mindspore-cluster(10.0.0.0/24) | subnet-mindspore-cluster(10.0.0.0/24) | mindspore-cluster | 172.16.0.0/16 |
| openEuler | BeiJing4 | net-community(172.16.0.0./16) | subnet-community(172.16.1.0/24) | openeuler-community | 172.17.0.0/16 |
| MindSpore | BeiJing4 | vpc-a0c1(192.168.0.0/16) | subnet-a105(192.168.0.0/24) | mindspore-x86-slaves | 172.16.0.0/16 |
| MindSpore | BeiJing4 | vpc-a0c1(192.168.0.0/16) | subnet-a105(192.168.0.0/24) | mindspore-arm-slaves | 172.16.0.0/16 |
| openLookeng | HongKong | vpc-lookeng-community(10.0.0.0/24) | subnet-4273(10.0.0.0/24) | cce-openlookeng | 172.21.0.0/16 |

# Kubernetes Cluster API endpoints
| Name | Community | Region | API endpoints |
| :---:| :----: | :----: | :----: |
| os-infra | None | HongKong | 119.8.122.167(https://kubernetes.default.svc) |
| mindspore | MindSpore | Beijing | 114.115.223.130 |
| mindspore-hk | MindSpore | HongKong | 119.8.45.34 |
| openeuler-cn-north4 | openEuler | Beijing4 | 114.116.226.125|
| openeuler-hk | openEuler | HongKong | 159.138.41.5 |
| openlookeng-hk | openLooKeng | HongKong | 159.138.57.217 |

