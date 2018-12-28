# Creating Hadoop cluster with Spark 

using vagrant + ansible


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


Hadoop and Spark LATEST releases: Hadoop - 3.1.1 , Spark -2.4.0

davar@home ~/LABS/ansible-hadoop-spark-playground $ cat roles/hadoop/defaults/main.yml 
---

drop_data: false
fresh_unzip: true
start_on_finish: true
run_demo: false

# passw0rd
hadoop_password: $6$VKqoODAnoEqhS$QhuYlkAChxm5P1FLgrPXJO4OrdM/qRBsfnBr6Jsfw18GserWNBSJ5kKl64nX9ouqdnBeGSzjMSd5z1SfFMgpE1

pkg_ic:
  name: hadoop
  install_path: /usr/lib
  url: https://www-eu.apache.org/dist/hadoop/common/hadoop-3.1.1/hadoop-3.1.1.tar.gz
  file: hadoop-3.1.1.tar.gz
  basename: hadoop-3.1.1
  version: 3.1.1

hadoop_client_conf:
  users:
    demo_runner:
      name: andy
      id: 3001
    spark:
      name: spark
      id: 3002


davar@home ~/LABS/ansible-hadoop-spark-playground $ cat roles/spark/vars/main.yml 
---

spark_ics:
  no_hadoop:
    version: 2.4.0
    url: https://archive.apache.org/dist/spark/spark-2.4.0/spark-2.4.0-bin-without-hadoop.tgz
    file: spark-2.4.0-bin-without-hadoop.tgz
    basename: spark-2.4.0-bin-without-hadoop
  with_hadoop:
    version: 2.4.0
    url: https://archive.apache.org/dist/spark/spark-2.4.0/spark-2.4.0-bin-hadoop2.7.tgz
    file: spark-2.4.0-bin-hadoop2.7.tgz
    basename: spark-2.4.0-bin-hadoop2.7


Note: Remove         - mapred-site.xml from roles/hadoop/tasks/config_hadoop_common.yml


davar@home ~/LABS/ansible-hadoop-spark-playground $ diff roles/spark/tasks/extract_spark.yml roles/spark/tasks/extract_spark.yml.ORIG
20c20,21
<       get_url:
---
>       cached_get_url:
>         cached: "{{ resource_cache }}/{{ spark_ic.file }}"
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


#### Multinode - 2 nodes example
```
davar@home ~/LABS/ansible-hadoop-spark-playground-multi-node/inventories/hadoop $ vagrant up
Bringing machine 'hadoop-00' up with 'virtualbox' provider...
Bringing machine 'hadoop-01' up with 'virtualbox' provider...

davar@home ~/LABS/ansible-hadoop-spark-playground-multi-node $ ansible-playbook -i inventories/standalone_cluster spark_standalone.yml
 [ERROR]:

 [WARNING]: Could not match supplied host pattern, ignoring: zk


PLAY [Pre-setup] *********************************************************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************************************************
Wednesday 12 December 2018  04:03:39 +0200 (0:00:00.739)       0:00:00.739 **** 
ok: [node_01]
ok: [node_00]

TASK [basic/system : debug] **********************************************************************************************************************************
Wednesday 12 December 2018  04:03:47 +0200 (0:00:07.467)       0:00:08.207 **** 
ok: [node_00] => {
    "msg": "osfamily:RedHat , distribution:CentOS , release:Core , version:7(7.5.1804) , pkg:yum\n"
}
ok: [node_01] => {
    "msg": "osfamily:RedHat , distribution:CentOS , release:Core , version:7(7.5.1804) , pkg:yum\n"
}

TASK [basic/system : include_vars] ***************************************************************************************************************************
Wednesday 12 December 2018  04:03:47 +0200 (0:00:00.158)       0:00:08.365 **** 
ok: [node_01] => (item=/home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/basic/system/vars/os/RedHat.yml)
ok: [node_00] => (item=/home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/basic/system/vars/os/RedHat.yml)

TASK [basic/hosts : debug] ***********************************************************************************************************************************
Wednesday 12 December 2018  04:03:47 +0200 (0:00:00.199)       0:00:08.564 **** 
ok: [node_00] => {
    "msg": "Will set hostname as cluster-node-00"
}
ok: [node_01] => {
    "msg": "Will set hostname as cluster-node-01"
}

TASK [basic/hosts : Set hostname] ****************************************************************************************************************************
Wednesday 12 December 2018  04:03:47 +0200 (0:00:00.097)       0:00:08.662 **** 
ok: [node_01]
ok: [node_00]

TASK [basic/hosts : set_fact] ********************************************************************************************************************************
Wednesday 12 December 2018  04:03:49 +0200 (0:00:01.860)       0:00:10.523 **** 
ok: [node_00]
ok: [node_01]

TASK [basic/hosts : Update /etc/hosts : drop 127.0.0.1 to hostname (avoid address binding problem)] **********************************************************
Wednesday 12 December 2018  04:03:49 +0200 (0:00:00.106)       0:00:10.629 **** 
ok: [node_01]
ok: [node_00]

TASK [basic/hosts : Update /etc/hosts : add hostnames] *******************************************************************************************************
Wednesday 12 December 2018  04:03:50 +0200 (0:00:00.773)       0:00:11.403 **** 
ok: [node_00] => (item=node_00)
ok: [node_01] => (item=node_00)
ok: [node_01] => (item=node_01)
ok: [node_00] => (item=node_01)

TASK [basic/sources : Setup proxy for package manager] *******************************************************************************************************
Wednesday 12 December 2018  04:03:51 +0200 (0:00:01.364)       0:00:12.768 **** 
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/basic/sources/tasks/proxy/yum.yml for node_00, node_01

TASK [basic/sources : Setup proxy for yum] *******************************************************************************************************************
Wednesday 12 December 2018  04:03:52 +0200 (0:00:00.136)       0:00:12.904 **** 
skipping: [node_00]
skipping: [node_01]

TASK [basic/sources : Disable proxy for yum] *****************************************************************************************************************
Wednesday 12 December 2018  04:03:52 +0200 (0:00:00.072)       0:00:12.976 **** 
ok: [node_01]
ok: [node_00]

TASK [basic/sources : Resolve vars] **************************************************************************************************************************
Wednesday 12 December 2018  04:03:52 +0200 (0:00:00.778)       0:00:13.755 **** 
ok: [node_00] => (item=/home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/basic/sources/vars/os_aware/CentOS.yml)
ok: [node_01] => (item=/home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/basic/sources/vars/os_aware/CentOS.yml)

TASK [basic/sources : Update repo] ***************************************************************************************************************************
Wednesday 12 December 2018  04:03:53 +0200 (0:00:00.121)       0:00:13.877 **** 
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/basic/sources/tasks/os_aware/CentOS.yml for node_00, node_01

TASK [basic/sources : (CentOS) Check CentOS-Base.repo.backup] ************************************************************************************************
Wednesday 12 December 2018  04:03:53 +0200 (0:00:00.129)       0:00:14.006 **** 
ok: [node_01]
ok: [node_00]

TASK [basic/sources : (CentOS) Backup CentOS-Base.repo] ******************************************************************************************************
Wednesday 12 December 2018  04:03:53 +0200 (0:00:00.797)       0:00:14.804 **** 
skipping: [node_00]
skipping: [node_01]

TASK [basic/sources : Pick Mirror config] ********************************************************************************************************************
Wednesday 12 December 2018  04:03:54 +0200 (0:00:00.070)       0:00:14.875 **** 
ok: [node_00] => (item=/home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/basic/sources/templates/mirrors/CentOS-7.repo.aliyun)
ok: [node_01] => (item=/home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/basic/sources/templates/mirrors/CentOS-7.repo.aliyun)

TASK [basic/sources : (CentOS) Use new CentOS-Base.repo] *****************************************************************************************************
Wednesday 12 December 2018  04:03:54 +0200 (0:00:00.125)       0:00:15.000 **** 
ok: [node_01]
ok: [node_00]

TASK [basic/sources : (CentOS) Update repo cache] ************************************************************************************************************
Wednesday 12 December 2018  04:03:55 +0200 (0:00:01.277)       0:00:16.278 **** 
ok: [node_01]
ok: [node_00]

TASK [basic/sources : (CentOS) Install the dependence packages] **********************************************************************************************
Wednesday 12 December 2018  04:03:58 +0200 (0:00:03.205)       0:00:19.484 **** 

TASK [basic/disable_firewall : stop firewalld service] *******************************************************************************************************
Wednesday 12 December 2018  04:03:58 +0200 (0:00:00.071)       0:00:19.556 **** 
ok: [node_01]
ok: [node_00]

TASK [basic/disable_firewall : stop ufw service] *************************************************************************************************************
Wednesday 12 December 2018  04:03:59 +0200 (0:00:01.043)       0:00:20.599 **** 
fatal: [node_00]: FAILED! => {"changed": false, "msg": "Could not find the requested service ufw: host"}
...ignoring
fatal: [node_01]: FAILED! => {"changed": false, "msg": "Could not find the requested service ufw: host"}
...ignoring

TASK [jdk : Fetch JAVA_HOME, setup if absent] ****************************************************************************************************************
Wednesday 12 December 2018  04:04:00 +0200 (0:00:00.684)       0:00:21.284 **** 
ok: [node_01]
ok: [node_00]

TASK [jdk : Fetch java version] ******************************************************************************************************************************
Wednesday 12 December 2018  04:04:01 +0200 (0:00:00.850)       0:00:22.134 **** 
ok: [node_00]
ok: [node_01]

TASK [jdk : debug] *******************************************************************************************************************************************
Wednesday 12 December 2018  04:04:02 +0200 (0:00:00.861)       0:00:22.996 **** 
ok: [node_00] => {
    "msg": "os:RedHat , distribution:CentOS-7.5.1804(Core) , JAVA_HOME:/usr/lib/jdk/jdk1.8.0_192 , Java version:1.8.0_192\n"
}
ok: [node_01] => {
    "msg": "os:RedHat , distribution:CentOS-7.5.1804(Core) , JAVA_HOME:/usr/lib/jdk/jdk1.8.0_192 , Java version:1.8.0_192\n"
}

TASK [jdk : Install from repo] *******************************************************************************************************************************
Wednesday 12 December 2018  04:04:02 +0200 (0:00:00.156)       0:00:23.153 **** 
[DEPRECATION WARNING]: Using tests as filters is deprecated. Instead of using `result|failed` instead use `result is failed`. This feature will be removed in
 version 2.9. Deprecation warnings can be disabled by setting deprecation_warnings=False in ansible.cfg.
skipping: [node_00]
[DEPRECATION WARNING]: Using tests as filters is deprecated. Instead of using `result|failed` instead use `result is failed`. This feature will be removed in
 version 2.9. Deprecation warnings can be disabled by setting deprecation_warnings=False in ansible.cfg.
skipping: [node_01]

TASK [jdk : Install from tar] ********************************************************************************************************************************
Wednesday 12 December 2018  04:04:02 +0200 (0:00:00.113)       0:00:23.266 **** 
[DEPRECATION WARNING]: Using tests as filters is deprecated. Instead of using `result|failed` instead use `result is failed`. This feature will be removed in
 version 2.9. Deprecation warnings can be disabled by setting deprecation_warnings=False in ansible.cfg.
skipping: [node_00]
[DEPRECATION WARNING]: Using tests as filters is deprecated. Instead of using `result|failed` instead use `result is failed`. This feature will be removed in
 version 2.9. Deprecation warnings can be disabled by setting deprecation_warnings=False in ansible.cfg.
skipping: [node_01]

TASK [zookeeper : Install and config zookeeper] **************************************************************************************************************
Wednesday 12 December 2018  04:04:02 +0200 (0:00:00.071)       0:00:23.338 **** 
skipping: [node_00]
skipping: [node_01]

PLAY [Setup Spark] *******************************************************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************************************************
Wednesday 12 December 2018  04:04:02 +0200 (0:00:00.088)       0:00:23.427 **** 
ok: [node_01]
ok: [node_00]

TASK [basic/system : debug] **********************************************************************************************************************************
Wednesday 12 December 2018  04:04:03 +0200 (0:00:01.063)       0:00:24.490 **** 
ok: [node_00] => {
    "msg": "osfamily:RedHat , distribution:CentOS , release:Core , version:7(7.5.1804) , pkg:yum\n"
}
ok: [node_01] => {
    "msg": "osfamily:RedHat , distribution:CentOS , release:Core , version:7(7.5.1804) , pkg:yum\n"
}

TASK [basic/system : include_vars] ***************************************************************************************************************************
Wednesday 12 December 2018  04:04:03 +0200 (0:00:00.107)       0:00:24.598 **** 
ok: [node_00] => (item=/home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/basic/system/vars/os/RedHat.yml)
ok: [node_01] => (item=/home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/basic/system/vars/os/RedHat.yml)

TASK [spark : Present spark_install_dir] *********************************************************************************************************************
Wednesday 12 December 2018  04:04:03 +0200 (0:00:00.123)       0:00:24.721 **** 
ok: [node_00]
ok: [node_01]

TASK [spark : set_fact] **************************************************************************************************************************************
Wednesday 12 December 2018  04:04:04 +0200 (0:00:00.635)       0:00:25.357 **** 
ok: [node_00]
ok: [node_01]

TASK [spark : set_fact] **************************************************************************************************************************************
Wednesday 12 December 2018  04:04:04 +0200 (0:00:00.111)       0:00:25.469 **** 
ok: [node_00]
ok: [node_01]

TASK [spark : Delete Spark installation - /opt/spark-2.2.0-bin-hadoop2.7] ************************************************************************************
Wednesday 12 December 2018  04:04:04 +0200 (0:00:00.115)       0:00:25.584 **** 
skipping: [node_00] => (item=/opt/spark-2.2.0-bin-hadoop2.7) 
skipping: [node_00] => (item=/opt/spark) 
skipping: [node_01] => (item=/opt/spark-2.2.0-bin-hadoop2.7) 
skipping: [node_01] => (item=/opt/spark) 

TASK [spark : Download - spark-2.2.0-bin-hadoop2.7.tgz] ******************************************************************************************************
Wednesday 12 December 2018  04:04:04 +0200 (0:00:00.124)       0:00:25.709 **** 
changed: [node_01]
changed: [node_00]

TASK [spark : Unarchive package - /opt] **********************************************************************************************************************
Wednesday 12 December 2018  04:04:27 +0200 (0:00:22.808)       0:00:48.517 **** 
changed: [node_01]
changed: [node_00]

TASK [spark : Make soft link] ********************************************************************************************************************************
Wednesday 12 December 2018  04:04:46 +0200 (0:00:18.720)       0:01:07.238 **** 
changed: [node_01]
changed: [node_00]

TASK [spark : Export SPARK_HOME ...] *************************************************************************************************************************
Wednesday 12 December 2018  04:04:54 +0200 (0:00:08.459)       0:01:15.697 **** 
changed: [node_01]
changed: [node_00]

TASK [spark : Present group - spark] *************************************************************************************************************************
Wednesday 12 December 2018  04:04:55 +0200 (0:00:00.869)       0:01:16.567 **** 
changed: [node_01]
changed: [node_00]

TASK [spark : Present users - [u'spark', u'swift', u'andy']] *************************************************************************************************
Wednesday 12 December 2018  04:04:57 +0200 (0:00:01.528)       0:01:18.095 **** 
changed: [node_01] => (item=spark)
changed: [node_00] => (item=spark)
changed: [node_01] => (item=swift)
changed: [node_01] => (item=andy)
changed: [node_00] => (item=swift)
changed: [node_00] => (item=andy)

TASK [spark : Gather Spark Nodes] ****************************************************************************************************************************
Wednesday 12 December 2018  04:05:01 +0200 (0:00:03.723)       0:01:21.818 **** 
ok: [node_00]
ok: [node_01]

TASK [spark : set_fact] **************************************************************************************************************************************
Wednesday 12 December 2018  04:05:01 +0200 (0:00:00.245)       0:01:22.063 **** 
ok: [node_00]
ok: [node_01]

TASK [spark : set_fact] **************************************************************************************************************************************
Wednesday 12 December 2018  04:05:01 +0200 (0:00:00.111)       0:01:22.174 **** 
skipping: [node_00]
skipping: [node_01]

TASK [spark : debug] *****************************************************************************************************************************************
Wednesday 12 December 2018  04:05:01 +0200 (0:00:00.069)       0:01:22.244 **** 
skipping: [node_00]
skipping: [node_01]

TASK [spark : set_fact] **************************************************************************************************************************************
Wednesday 12 December 2018  04:05:01 +0200 (0:00:00.069)       0:01:22.313 **** 
skipping: [node_00]
skipping: [node_01]

TASK [spark : Present Spark Deploy Zookeeper Dir] ************************************************************************************************************
Wednesday 12 December 2018  04:05:01 +0200 (0:00:00.069)       0:01:22.383 **** 
skipping: [node_00]
skipping: [node_01]

TASK [spark : Present Spark Conf Dir - /etc/spark/conf] ******************************************************************************************************
Wednesday 12 December 2018  04:05:01 +0200 (0:00:00.079)       0:01:22.462 **** 
changed: [node_01]
changed: [node_00]

TASK [spark : Copy Spark Scripts] ****************************************************************************************************************************
Wednesday 12 December 2018  04:05:02 +0200 (0:00:00.684)       0:01:23.147 **** 
changed: [node_00]
changed: [node_01]

TASK [spark : Copy Spark Conf Dir] ***************************************************************************************************************************
Wednesday 12 December 2018  04:05:10 +0200 (0:00:07.704)       0:01:30.852 **** 
changed: [node_01]
changed: [node_00]

TASK [spark : Enable Spark Config files] *********************************************************************************************************************
Wednesday 12 December 2018  04:05:11 +0200 (0:00:01.630)       0:01:32.482 **** 
changed: [node_01] => (item=spark-env.sh)
changed: [node_00] => (item=spark-env.sh)
changed: [node_01] => (item=spark-defaults.conf)
changed: [node_00] => (item=spark-defaults.conf)

TASK [spark : Export SPARK_CONF_DIR] *************************************************************************************************************************
Wednesday 12 December 2018  04:05:12 +0200 (0:00:01.283)       0:01:33.766 **** 
changed: [node_00]
changed: [node_01]

TASK [spark : Set Spark configuration for standalone mode] ***************************************************************************************************
Wednesday 12 December 2018  04:05:13 +0200 (0:00:00.609)       0:01:34.375 **** 
skipping: [node_00]
skipping: [node_01]

TASK [spark : Copy standalone conf] **************************************************************************************************************************
Wednesday 12 December 2018  04:05:13 +0200 (0:00:00.068)       0:01:34.444 **** 
skipping: [node_00]
skipping: [node_01]

TASK [spark : Set Spark's eventlog] **************************************************************************************************************************
Wednesday 12 December 2018  04:05:13 +0200 (0:00:00.219)       0:01:34.663 **** 
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/spark/tasks/config/eventlog.yml for node_00, node_01

TASK [spark : Present Spark Local Eventlog Dir] **************************************************************************************************************
Wednesday 12 December 2018  04:05:14 +0200 (0:00:00.201)       0:01:34.865 **** 
changed: [node_00]
changed: [node_01]

TASK [spark : Present Spark Remote Eventlog Dir - /spark_eventlog] *******************************************************************************************
Wednesday 12 December 2018  04:05:14 +0200 (0:00:00.846)       0:01:35.711 **** 
skipping: [node_00]
skipping: [node_01]

TASK [spark : Config password-less from localhost] ***********************************************************************************************************
Wednesday 12 December 2018  04:05:14 +0200 (0:00:00.075)       0:01:35.787 **** 
skipping: [node_00]
skipping: [node_01]

TASK [spark : Config password-less from master] **************************************************************************************************************
Wednesday 12 December 2018  04:05:15 +0200 (0:00:00.064)       0:01:35.851 **** 
skipping: [node_00]
skipping: [node_01]

TASK [spark : Present SPARK_LOG_DIR - /home/[u'spark', u'swift', u'andy']/logs] ******************************************************************************
Wednesday 12 December 2018  04:05:15 +0200 (0:00:00.077)       0:01:35.928 **** 
changed: [node_01] => (item=spark)
changed: [node_00] => (item=spark)
changed: [node_01] => (item=swift)
changed: [node_00] => (item=swift)
changed: [node_00] => (item=andy)
changed: [node_01] => (item=andy)

TASK [spark : Export LOG_DIRs for - [u'spark', u'swift', u'andy']] *******************************************************************************************
Wednesday 12 December 2018  04:05:17 +0200 (0:00:02.124)       0:01:38.053 **** 
changed: [node_00] => (item=spark)
changed: [node_01] => (item=spark)
changed: [node_00] => (item=swift)
changed: [node_01] => (item=swift)
changed: [node_00] => (item=andy)
changed: [node_01] => (item=andy)

TASK [spark : include_tasks] *********************************************************************************************************************************
Wednesday 12 December 2018  04:05:19 +0200 (0:00:02.027)       0:01:40.081 **** 
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/spark/tasks/run_daemons.yml for node_00, node_01

TASK [spark : Run stop-all.sh] *******************************************************************************************************************************
Wednesday 12 December 2018  04:05:19 +0200 (0:00:00.181)       0:01:40.262 **** 
skipping: [node_00]
skipping: [node_01]

TASK [spark : Run start-all.sh] ******************************************************************************************************************************
Wednesday 12 December 2018  04:05:19 +0200 (0:00:00.075)       0:01:40.337 **** 
skipping: [node_00]
skipping: [node_01]

TASK [spark : Run Spark History_server] **********************************************************************************************************************
Wednesday 12 December 2018  04:05:19 +0200 (0:00:00.072)       0:01:40.410 **** 
skipping: [node_00]
skipping: [node_01]

TASK [spark : include_tasks] *********************************************************************************************************************************
Wednesday 12 December 2018  04:05:19 +0200 (0:00:00.069)       0:01:40.480 **** 
skipping: [node_00]
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/spark/tasks/run_demo.yml for node_01

TASK [spark : Run Standalone run-demo.sh] ********************************************************************************************************************
Wednesday 12 December 2018  04:05:19 +0200 (0:00:00.152)       0:01:40.632 **** 
skipping: [node_01]

TASK [spark : Run on-yarn run-demo.sh] ***********************************************************************************************************************
Wednesday 12 December 2018  04:05:19 +0200 (0:00:00.045)       0:01:40.677 **** 
skipping: [node_01]

PLAY RECAP ***************************************************************************************************************************************************
node_00                    : ok=45   changed=14   unreachable=0    failed=0   
node_01                    : ok=46   changed=14   unreachable=0    failed=0   

Wednesday 12 December 2018  04:05:19 +0200 (0:00:00.023)       0:01:40.700 **** 
=============================================================================== 
spark : Download - spark-2.2.0-bin-hadoop2.7.tgz ----------------------------------------------------------------------------------------------------- 22.81s
spark : Unarchive package - /opt --------------------------------------------------------------------------------------------------------------------- 18.72s
spark : Make soft link -------------------------------------------------------------------------------------------------------------------------------- 8.46s
spark : Copy Spark Scripts ---------------------------------------------------------------------------------------------------------------------------- 7.70s
Gathering Facts --------------------------------------------------------------------------------------------------------------------------------------- 7.47s
spark : Present users - [u'spark', u'swift', u'andy'] ------------------------------------------------------------------------------------------------- 3.72s
basic/sources : (CentOS) Update repo cache ------------------------------------------------------------------------------------------------------------ 3.21s
spark : Present SPARK_LOG_DIR - /home/[u'spark', u'swift', u'andy']/logs ------------------------------------------------------------------------------ 2.12s
spark : Export LOG_DIRs for - [u'spark', u'swift', u'andy'] ------------------------------------------------------------------------------------------- 2.03s
basic/hosts : Set hostname ---------------------------------------------------------------------------------------------------------------------------- 1.86s
spark : Copy Spark Conf Dir --------------------------------------------------------------------------------------------------------------------------- 1.63s
spark : Present group - spark ------------------------------------------------------------------------------------------------------------------------- 1.53s
basic/hosts : Update /etc/hosts : add hostnames ------------------------------------------------------------------------------------------------------- 1.36s
spark : Enable Spark Config files --------------------------------------------------------------------------------------------------------------------- 1.28s
basic/sources : (CentOS) Use new CentOS-Base.repo ----------------------------------------------------------------------------------------------------- 1.28s
Gathering Facts --------------------------------------------------------------------------------------------------------------------------------------- 1.06s
basic/disable_firewall : stop firewalld service ------------------------------------------------------------------------------------------------------- 1.04s
spark : Export SPARK_HOME ... ------------------------------------------------------------------------------------------------------------------------- 0.87s
jdk : Fetch java version ------------------------------------------------------------------------------------------------------------------------------ 0.86s
jdk : Fetch JAVA_HOME, setup if absent ---------------------------------------------------------------------------------------------------------------- 0.85s
davar@home ~/LABS/ansible-hadoop-spark-playground-multi-node $ cat inventories/hadoop/_groups.yml 
---

# https://gist.github.com/sivel/3c0745243787b9899486
# ansible_connection: ssh
group_default_vars: {}

groups:
  - name: hdfs_namenode
    hosts: [node_00]
  - name: hdfs_datanode
    hosts: [node_00, node_01]
  - name: hdfs
    children: [hdfs_namenode, hdfs_datanode]

  - name: yarn_resource_mgr
    hosts: [node_00]
  - name: yarn_node_mgr
    hosts: [node_00, node_01]
  - name: yarn_proxyserver
    hosts: [node_00]
  - name: yarn
    children: [yarn_resource_mgr, yarn_node_mgr, yarn_proxyserver]

  - name: historyserver
    hosts: [node_01]

  - name: hadoop_cluster
    children: [hdfs, yarn, historyserver]


  - name: hadoop_client_as_mapred
    hosts: [node_01]
  - name: hadoop_client_as_andy
    hosts: [node_01]

  - name: hadoop_all_nodes
    children: [hadoop_cluster, hadoop_client_as_mapred, hadoop_client_as_andy]



davar@home ~/LABS/ansible-hadoop-spark-playground-multi-node $ cat inventories/
hadoop/                _hosts.yml             on-yarn/               standalone/            standalone_cluster_ha/ XInv.pyc
hadoop-single/         __init__.py            sample/                standalone_cluster/    XInv.py                
davar@home ~/LABS/ansible-hadoop-spark-playground-multi-node $ cat inventories/standalone_cluster/_groups.yml 
---

# https://gist.github.com/sivel/3c0745243787b9899486
# ansible_connection: ssh
group_default_vars: {}

groups:
  - name: spark_masters
    hosts: [node_00]
  - name: spark_slaves
    hosts: [node_00, node_01]
  - name: spark_nodes
    children: [spark_masters, spark_slaves]

  - name: history_server_runner
    hosts: [node_01]
    vars:
      spark_run_history_server: True
  - name: demo_runner
    hosts: [node_01]
    vars:
      spark_run_demo: True


======
[vagrant@cluster-node-00 ~]$ sudo netstat -nlpt|grep java|grep LIST
tcp        0      0 127.0.0.1:33465         0.0.0.0:*               LISTEN      24456/java          
tcp        0      0 0.0.0.0:50010           0.0.0.0:*               LISTEN      24456/java          
tcp        0      0 0.0.0.0:50075           0.0.0.0:*               LISTEN      24456/java          
tcp        0      0 0.0.0.0:50020           0.0.0.0:*               LISTEN      24456/java          
tcp        0      0 192.168.102.100:9000    0.0.0.0:*               LISTEN      24357/java          
tcp        0      0 0.0.0.0:50090           0.0.0.0:*               LISTEN      24642/java          
tcp        0      0 0.0.0.0:50070           0.0.0.0:*               LISTEN      24357/java          
tcp6       0      0 192.168.102.100:8088    :::*                    LISTEN      24953/java          
tcp6       0      0 :::13562                :::*                    LISTEN      25051/java          
tcp6       0      0 192.168.102.100:8030    :::*                    LISTEN      24953/java          
tcp6       0      0 192.168.102.100:8031    :::*                    LISTEN      24953/java          
tcp6       0      0 192.168.102.100:8032    :::*                    LISTEN      24953/java          
tcp6       0      0 192.168.102.100:8033    :::*                    LISTEN      24953/java          
tcp6       0      0 :::8040                 :::*                    LISTEN      25051/java          
tcp6       0      0 :::8042                 :::*                    LISTEN      25051/java          
tcp6       0      0 :::33142                :::*                    LISTEN      25051/java  

[vagrant@cluster-node-01 ~]$ sudo netstat -nlpt|grep java|grep LIST
tcp        0      0 0.0.0.0:50010           0.0.0.0:*               LISTEN      22251/java          
tcp        0      0 0.0.0.0:50075           0.0.0.0:*               LISTEN      22251/java          
tcp        0      0 0.0.0.0:10020           0.0.0.0:*               LISTEN      22480/java          
tcp        0      0 0.0.0.0:50020           0.0.0.0:*               LISTEN      22251/java          
tcp        0      0 0.0.0.0:19888           0.0.0.0:*               LISTEN      22480/java          
tcp        0      0 0.0.0.0:10033           0.0.0.0:*               LISTEN      22480/java          
tcp        0      0 127.0.0.1:40242         0.0.0.0:*               LISTEN      22251/java          
tcp6       0      0 :::13562                :::*                    LISTEN      22388/java          
tcp6       0      0 :::8040                 :::*                    LISTEN      22388/java          
tcp6       0      0 :::8042                 :::*                    LISTEN      22388/java          
tcp6       0      0 :::40978                :::*                    LISTEN      22388/java       

davar@home ~/LABS/ansible-hadoop-spark-playground-multi-node $ cat Vagrantfile
# -*- mode: ruby -*-
# vi: set ft=ruby :

SUPPORTED_OS = {
  "ubuntu-16" => {box: "bento/ubuntu-16.04",  box_v: ""},
  "centos-7"  => {box: "centos/7",            box_v: ""},
  # "debian/jessie64",
  # "ubuntu/precise64",
  # "ubuntu/trusty64",
  # "bento/opensuse-13.2",
  # "scotch/box",
}

$subnet = "192.168.102"
$num_instances = 2
$vm_memory = 1024
$vm_cpus = 1
$instance_name_prefix = "hadoop"

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  config.vm.box_check_update = false

oses = [
  "centos-7",
]
  max_id = $num_instances - 1
  (0..max_id).each do |i|
    subip = 100 + i
    ip = "#{$subnet}.#{subip}"
    config.vm.define node_name = "%s-%02d" % [$instance_name_prefix, i] do |node|
      os_name = oses[i % oses.length]
      os_def = SUPPORTED_OS[os_name]
      node.vm.hostname = node_name

      node.vm.box = os_def[:box]
      if os_def.has_key? :box_v
        node.vm.box_version = os_def[:box_v]
      end

      node.vm.network "private_network" , ip: "#{ip}"
      node.vm.provider "virtualbox" do |v|
        v.name = node_name
        v.cpus = $vm_cpus
        v.memory = $vm_memory
      end
      # copy private key so hosts can ssh using key authentication (the script below sets permissions to 600)
      node.vm.provision "file", source: "~/.ssh/id_rsa.pub", destination: "host_id_rsa.pub"
      node.vm.provision "shell", path: "vm_bootstrap.sh"
    end
  end
end
```
