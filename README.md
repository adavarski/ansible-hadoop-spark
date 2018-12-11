# Creating Hadoop cluster with Spark (Using vagrant + ansible)


# Hadoop-install
This project contains ansible playbooks to install Hadoop cluster.

## Easy Run

* Start virtual machines for test-run.

  ```
  vagrant up
  ```

* Start Hadoop single node cluster

  ```
  ansible-playbook -i inventories/hadoop-single hadoop.yaml
  ```

  | Node type          | Web UI                       |
  | ------------------ | ---------------------------- |
  | namenode:          | http://192.168.102.100:50070 |
  | datanode:          | http://192.168.102.100:50075 |
  | resourcemanager:   | http://192.168.102.100:8088  |
  | nodemanager:       | http://192.168.102.100:8042  |
  | job historyserver: | http://192.168.102.100:19888 |

* Start Hadoop cluster

  ```
  ansible-playbook -i inventories/hadoop hadoop.yaml
  ```

  | Node type          | Web UI                                   |
  | ------------------ | ---------------------------------------- |
  | namenode:          | http://192.168.102.100:50070             |
  | datanode:          | http://192.168.102.101:50075<br/>http://192.168.102.103:50075 |
  | resourcemanager:   | http://192.168.102.102:8088              |
  | nodemanager:       | http://192.168.102.103:8042 <br/>http://192.168.102.104:8042 |
  | job historyserver: | http://192.168.102.105:19888             |

## Ansible inventory

Ansible inventory files locate under directory: inventories

In inventory file, we define nodes and groups.

For easy management, I wrote a python script "XInv.py" (see ./inventories/XInv.py) which will parse hosts and groups yml files, and generates ansible acceptable json format.

Each directory under ./inventories represents for a dynamic-inventory setting.

For more details, see example files under ./inventories

### Define your own inventory

Inventory contains two parts: nodes and groups.

#### Define nodes

2 methods:

* Update ./inventories/_hosts.yml

  The file correspons to the vm definition which is defined in ./Vagrantfile. (see below)

* Create ./inventories/.__hosts.yml_

  You may refer to the format in ./inventories/_hosts.yml.

  Note: .__hosts.yml_ has higer priority than _hosts.yml

It would be best if you have physical machines, otherwise we may take adantage of virtualbox.

The project has a pre-defined Vagrantfile.

To create virtual machine:

```
vagrant up
```

To destroy virtual machine:

```
vagrant destroy
```

#### Define groups
Each directory under ./inventories represents for a dynamic-inventory setting.

Take ./inventories/hadoop for example, files has different usage:

| File/Directory | Comment                                  |
| -------------- | ---------------------------------------- |
| group_vars     | Define vars for groups                   |
| _groups.yml    | Define groups                            |
| hosts.py       | Main host definition file. This file will use "XInv.py" (mentioned above) to read hosts and groups yml file. |

2 methods to create your own groups:

* Update _groups.yml under an inventory directory
* Copy an inventory directory, and update its _groups.yml


## Spark Install (NOT YET FINISHED)

### Standalone mode
* Single node (Master + Slave)
  ```
  ansible-playbook -i inventories/standalone spark_standalone.yml
  ```
* Cluster with N Nodes (1 Master + (N-1) Slaves)
  ```
  ansible-playbook -i inventories/standalone_cluster spark_standalone.yml
  ```
* Cluster with ha: N Nodes (x zookeepers + y Masters + z Slaves)
  ```
  ansible-playbook -i inventories/standalone_ha spark_standalone.yml
  ```

### Run Spark on yarn
  ```
  ansible-playbook -i inventories/on-yarn spark_yarn.yml
  ```

| Node type           | Web UI                                   |
| ------------------- | ---------------------------------------- |
| namenode:           | http://192.168.102.100:50070             |
| datanode:           | http://192.168.102.101:50075 <br/>http://192.168.102.102:50075 <br/>http://192.168.102.103:50075 |
| resourcemanager:    | http://192.168.102.100:8088              |
| nodemanager:        | http://192.168.102.101:8042 <br/>http://192.168.102.102:8042 <br/>http://192.168.102.103:8042 |
| job historyserver:  | http://192.168.102.101:19888             |
| spark historyserver | http://192.168.102.104:18080             |
