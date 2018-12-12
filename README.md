# Creating Hadoop cluster with Spark 
# using vagrant + ansible


## Hadoop + Spark single node easy setup
```
$ vagrant up
$ ansible-playbook -i inventories/hadoop-single hadoop.yaml
$ ansible-playbook -i inventories/standalone spark_standalone.yml


  | Node type          | Web UI                       |
  | ------------------ | ---------------------------- |
  | namenode:          | http://192.168.102.100:50070 |
  | datanode:          | http://192.168.102.100:50075 |
  | resourcemanager:   | http://192.168.102.100:8088  |
  | nodemanager:       | http://192.168.102.100:8042  |
  | job historyserver: | http://192.168.102.100:19888 |
  | spark historyserver | http://192.168.102.104:18080|            
  
Note: If spark history server is not running:

[vagrant@cluster-node-00 ~]$ sudo yum install net-tools
[vagrant@cluster-node-00 ~]$ sudo netstat -antpl|grep LIST
tcp        0      0 127.0.0.1:25            0.0.0.0:*               LISTEN      891/master          
tcp        0      0 0.0.0.0:50010           0.0.0.0:*               LISTEN      26120/java          
tcp        0      0 0.0.0.0:50075           0.0.0.0:*               LISTEN      26120/java          
tcp        0      0 0.0.0.0:10020           0.0.0.0:*               LISTEN      26806/java          
tcp        0      0 0.0.0.0:50020           0.0.0.0:*               LISTEN      26120/java          
tcp        0      0 127.0.0.1:43813         0.0.0.0:*               LISTEN      26120/java          
tcp        0      0 192.168.102.100:9000    0.0.0.0:*               LISTEN      26013/java          
tcp        0      0 0.0.0.0:50090           0.0.0.0:*               LISTEN      26301/java          
tcp        0      0 0.0.0.0:111             0.0.0.0:*               LISTEN      385/rpcbind         
tcp        0      0 0.0.0.0:19888           0.0.0.0:*               LISTEN      26806/java          
tcp        0      0 0.0.0.0:10033           0.0.0.0:*               LISTEN      26806/java          
tcp        0      0 0.0.0.0:50070           0.0.0.0:*               LISTEN      26013/java          
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      599/sshd            
tcp6       0      0 192.168.102.100:8088    :::*                    LISTEN      26604/java          
tcp6       0      0 ::1:25                  :::*                    LISTEN      891/master          
tcp6       0      0 :::13562                :::*                    LISTEN      26700/java          
tcp6       0      0 192.168.102.100:8030    :::*                    LISTEN      26604/java          
tcp6       0      0 192.168.102.100:8031    :::*                    LISTEN      26604/java          
tcp6       0      0 192.168.102.100:8032    :::*                    LISTEN      26604/java          
tcp6       0      0 192.168.102.100:8033    :::*                    LISTEN      26604/java          
tcp6       0      0 :::8040                 :::*                    LISTEN      26700/java          
tcp6       0      0 :::8042                 :::*                    LISTEN      26700/java          
tcp6       0      0 :::38927                :::*                    LISTEN      26700/java          
tcp6       0      0 :::111                  :::*                    LISTEN      385/rpcbind         
tcp6       0      0 :::22                   :::*                    LISTEN      599/sshd  
         
[root@cluster-node-00 spark]# sbin/start-history-server.sh
starting org.apache.spark.deploy.history.HistoryServer, logging to /opt/spark/logs/spark-root-org.apache.spark.deploy.history.HistoryServer-1-cluster-node-00.out
[root@cluster-node-00 spark]# sudo netstat -antpl|grep 1808
tcp6       0      0 :::18080                :::*                    LISTEN      32526/java          

Note: jdk role fixes because of oracle want to login add this line:

headers: 'Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com%2F; oraclelicense=accept-securebackup-cookie'

$ cat roles/jdk/tasks/install_from_tar.yml

- name: Download {{ _jdk_.tarball_file }}
  cached_get_url:
    cached: "{{ resource_cache }}/{{ _jdk_.tarball_file }}"
    # url: "{{ pkg_ic.url }}/{{ _jdk_.version_detail }}/{{ _jdk_.tarball_file }}"
    url: "{{ pkg_ic.full_url }}"
    headers: 'Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com%2F; oraclelicense=accept-securebackup-cookie'
    dest: '{{ pkg_ic.install_path }}/{{ _jdk_.tarball_file }}'


$ cat roles/jdk/defaults/main.yml 
---

pkg_ic:
  name: jdk
  repo_install: false
  install_path: /usr/lib/jdk
  java_version: 8
  java_subversion: 192
  java_full_version: 1.8.0_192
  b_version: 12
  url: http://download.oracle.com/otn-pub/java/jdk
  full_url: https://download.oracle.com/otn-pub/java/jdk/8u192-b12/750e1c8617c5452694857ad95c3ee230/jdk-8u192-linux-x64.tar.gz

```

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

For easy management, we use a python script "XInv.py" (see ./inventories/XInv.py) which will parse hosts and groups yml files, and generates ansible acceptable json format.

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

The project has a pre-defined Vagrantfile.ORIG.

To create virtual machine:

```
vagrant up
```

To destroy virtual machine:

```
vagrant destroy or vagrant destroy -f
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
