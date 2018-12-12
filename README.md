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
==> hadoop-00: Importing base box 'centos/7'...
==> hadoop-00: Matching MAC address for NAT networking...
==> hadoop-00: Setting the name of the VM: hadoop-00
==> hadoop-00: Clearing any previously set network interfaces...
==> hadoop-00: Preparing network interfaces based on configuration...
    hadoop-00: Adapter 1: nat
    hadoop-00: Adapter 2: hostonly
==> hadoop-00: Forwarding ports...
    hadoop-00: 22 (guest) => 2222 (host) (adapter 1)
==> hadoop-00: Running 'pre-boot' VM customizations...
==> hadoop-00: Booting VM...
==> hadoop-00: Waiting for machine to boot. This may take a few minutes...
    hadoop-00: SSH address: 127.0.0.1:2222
    hadoop-00: SSH username: vagrant
    hadoop-00: SSH auth method: private key
    hadoop-00: Warning: Connection reset. Retrying...
    hadoop-00: Warning: Remote connection disconnect. Retrying...
    hadoop-00: Warning: Connection reset. Retrying...
    hadoop-00: Warning: Remote connection disconnect. Retrying...
    hadoop-00: Warning: Connection reset. Retrying...
    hadoop-00: Warning: Remote connection disconnect. Retrying...
    hadoop-00: Warning: Connection reset. Retrying...
    hadoop-00: Warning: Remote connection disconnect. Retrying...
    hadoop-00: Warning: Connection reset. Retrying...
    hadoop-00: Warning: Remote connection disconnect. Retrying...
    hadoop-00: Warning: Connection reset. Retrying...
    hadoop-00: Warning: Remote connection disconnect. Retrying...
    hadoop-00: Warning: Connection reset. Retrying...
    hadoop-00: Warning: Remote connection disconnect. Retrying...
    hadoop-00: Warning: Connection reset. Retrying...
    hadoop-00: Warning: Remote connection disconnect. Retrying...
    hadoop-00: Warning: Connection reset. Retrying...
    hadoop-00: Warning: Remote connection disconnect. Retrying...
    hadoop-00: Warning: Connection reset. Retrying...
    hadoop-00: Warning: Remote connection disconnect. Retrying...
    hadoop-00: Warning: Connection reset. Retrying...
    hadoop-00: Warning: Remote connection disconnect. Retrying...
    hadoop-00: Warning: Connection reset. Retrying...
    hadoop-00: Warning: Remote connection disconnect. Retrying...
    hadoop-00: Warning: Connection reset. Retrying...
    hadoop-00: Warning: Remote connection disconnect. Retrying...
    hadoop-00: Warning: Connection reset. Retrying...
    hadoop-00: Warning: Remote connection disconnect. Retrying...
    hadoop-00: Warning: Connection reset. Retrying...
    hadoop-00: Warning: Remote connection disconnect. Retrying...
    hadoop-00: Warning: Connection reset. Retrying...
    hadoop-00: Warning: Remote connection disconnect. Retrying...
    hadoop-00: Warning: Connection reset. Retrying...
    hadoop-00: 
    hadoop-00: Vagrant insecure key detected. Vagrant will automatically replace
    hadoop-00: this with a newly generated keypair for better security.
    hadoop-00: 
    hadoop-00: Inserting generated public key within guest...
    hadoop-00: Removing insecure key from the guest if it's present...
    hadoop-00: Key inserted! Disconnecting and reconnecting using new SSH key...
==> hadoop-00: Machine booted and ready!
[hadoop-00] No installation found.
Loaded plugins: fastestmirror
Determining fastest mirrors
 * base: mirror.host.ag
 * extras: mirror.host.ag
 * updates: mirror.host.ag
No package kernel-devel-3.10.0-862.14.4.el7.x86_64 available.
Package 1:make-3.82-23.el7.x86_64 already installed and latest version
Package bzip2-1.0.6-13.el7.x86_64 already installed and latest version
Resolving Dependencies
--> Running transaction check
---> Package binutils.x86_64 0:2.27-28.base.el7_5.1 will be updated
---> Package binutils.x86_64 0:2.27-34.base.el7 will be an update
---> Package gcc.x86_64 0:4.8.5-36.el7 will be installed
--> Processing Dependency: libgomp = 4.8.5-36.el7 for package: gcc-4.8.5-36.el7.x86_64
--> Processing Dependency: cpp = 4.8.5-36.el7 for package: gcc-4.8.5-36.el7.x86_64
--> Processing Dependency: libgcc >= 4.8.5-36.el7 for package: gcc-4.8.5-36.el7.x86_64
--> Processing Dependency: glibc-devel >= 2.2.90-12 for package: gcc-4.8.5-36.el7.x86_64
--> Processing Dependency: libmpfr.so.4()(64bit) for package: gcc-4.8.5-36.el7.x86_64
--> Processing Dependency: libmpc.so.3()(64bit) for package: gcc-4.8.5-36.el7.x86_64
---> Package kernel-devel.x86_64 0:3.10.0-957.1.3.el7 will be installed
---> Package perl.x86_64 4:5.16.3-293.el7 will be installed
--> Processing Dependency: perl-libs = 4:5.16.3-293.el7 for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(Socket) >= 1.3 for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(Scalar::Util) >= 1.10 for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl-macros for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl-libs for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(threads::shared) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(threads) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(constant) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(Time::Local) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(Time::HiRes) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(Storable) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(Socket) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(Scalar::Util) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(Pod::Simple::XHTML) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(Pod::Simple::Search) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(Getopt::Long) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(Filter::Util::Call) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(File::Temp) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(File::Spec::Unix) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(File::Spec::Functions) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(File::Spec) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(File::Path) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(Exporter) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(Cwd) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(Carp) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: libperl.so()(64bit) for package: 4:perl-5.16.3-293.el7.x86_64
--> Running transaction check
---> Package cpp.x86_64 0:4.8.5-36.el7 will be installed
---> Package glibc-devel.x86_64 0:2.17-260.el7 will be installed
--> Processing Dependency: glibc-headers = 2.17-260.el7 for package: glibc-devel-2.17-260.el7.x86_64
--> Processing Dependency: glibc = 2.17-260.el7 for package: glibc-devel-2.17-260.el7.x86_64
--> Processing Dependency: glibc-headers for package: glibc-devel-2.17-260.el7.x86_64
---> Package libgcc.x86_64 0:4.8.5-28.el7_5.1 will be updated
---> Package libgcc.x86_64 0:4.8.5-36.el7 will be an update
---> Package libgomp.x86_64 0:4.8.5-28.el7_5.1 will be updated
---> Package libgomp.x86_64 0:4.8.5-36.el7 will be an update
---> Package libmpc.x86_64 0:1.0.1-3.el7 will be installed
---> Package mpfr.x86_64 0:3.1.1-4.el7 will be installed
---> Package perl-Carp.noarch 0:1.26-244.el7 will be installed
---> Package perl-Exporter.noarch 0:5.68-3.el7 will be installed
---> Package perl-File-Path.noarch 0:2.09-2.el7 will be installed
---> Package perl-File-Temp.noarch 0:0.23.01-3.el7 will be installed
---> Package perl-Filter.x86_64 0:1.49-3.el7 will be installed
---> Package perl-Getopt-Long.noarch 0:2.40-3.el7 will be installed
--> Processing Dependency: perl(Pod::Usage) >= 1.14 for package: perl-Getopt-Long-2.40-3.el7.noarch
--> Processing Dependency: perl(Text::ParseWords) for package: perl-Getopt-Long-2.40-3.el7.noarch
---> Package perl-PathTools.x86_64 0:3.40-5.el7 will be installed
---> Package perl-Pod-Simple.noarch 1:3.28-4.el7 will be installed
--> Processing Dependency: perl(Pod::Escapes) >= 1.04 for package: 1:perl-Pod-Simple-3.28-4.el7.noarch
--> Processing Dependency: perl(Encode) for package: 1:perl-Pod-Simple-3.28-4.el7.noarch
---> Package perl-Scalar-List-Utils.x86_64 0:1.27-248.el7 will be installed
---> Package perl-Socket.x86_64 0:2.010-4.el7 will be installed
---> Package perl-Storable.x86_64 0:2.45-3.el7 will be installed
---> Package perl-Time-HiRes.x86_64 4:1.9725-3.el7 will be installed
---> Package perl-Time-Local.noarch 0:1.2300-2.el7 will be installed
---> Package perl-constant.noarch 0:1.27-2.el7 will be installed
---> Package perl-libs.x86_64 4:5.16.3-293.el7 will be installed
---> Package perl-macros.x86_64 4:5.16.3-293.el7 will be installed
---> Package perl-threads.x86_64 0:1.87-4.el7 will be installed
---> Package perl-threads-shared.x86_64 0:1.43-6.el7 will be installed
--> Running transaction check
---> Package glibc.x86_64 0:2.17-222.el7 will be updated
--> Processing Dependency: glibc = 2.17-222.el7 for package: glibc-common-2.17-222.el7.x86_64
---> Package glibc.x86_64 0:2.17-260.el7 will be an update
---> Package glibc-headers.x86_64 0:2.17-260.el7 will be installed
--> Processing Dependency: kernel-headers >= 2.2.1 for package: glibc-headers-2.17-260.el7.x86_64
--> Processing Dependency: kernel-headers for package: glibc-headers-2.17-260.el7.x86_64
---> Package perl-Encode.x86_64 0:2.51-7.el7 will be installed
---> Package perl-Pod-Escapes.noarch 1:1.04-293.el7 will be installed
---> Package perl-Pod-Usage.noarch 0:1.63-3.el7 will be installed
--> Processing Dependency: perl(Pod::Text) >= 3.15 for package: perl-Pod-Usage-1.63-3.el7.noarch
--> Processing Dependency: perl-Pod-Perldoc for package: perl-Pod-Usage-1.63-3.el7.noarch
---> Package perl-Text-ParseWords.noarch 0:3.29-4.el7 will be installed
--> Running transaction check
---> Package glibc-common.x86_64 0:2.17-222.el7 will be updated
---> Package glibc-common.x86_64 0:2.17-260.el7 will be an update
---> Package kernel-headers.x86_64 0:3.10.0-957.1.3.el7 will be installed
---> Package perl-Pod-Perldoc.noarch 0:3.20-4.el7 will be installed
--> Processing Dependency: perl(parent) for package: perl-Pod-Perldoc-3.20-4.el7.noarch
--> Processing Dependency: perl(HTTP::Tiny) for package: perl-Pod-Perldoc-3.20-4.el7.noarch
---> Package perl-podlators.noarch 0:2.5.1-3.el7 will be installed
--> Running transaction check
---> Package perl-HTTP-Tiny.noarch 0:0.033-3.el7 will be installed
---> Package perl-parent.noarch 1:0.225-244.el7 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

================================================================================
 Package                    Arch       Version                Repository   Size
================================================================================
Installing:
 gcc                        x86_64     4.8.5-36.el7           base         16 M
 kernel-devel               x86_64     3.10.0-957.1.3.el7     updates      17 M
 perl                       x86_64     4:5.16.3-293.el7       base        8.0 M
Updating:
 binutils                   x86_64     2.27-34.base.el7       base        5.9 M
Installing for dependencies:
 cpp                        x86_64     4.8.5-36.el7           base        5.9 M
 glibc-devel                x86_64     2.17-260.el7           base        1.1 M
 glibc-headers              x86_64     2.17-260.el7           base        683 k
 kernel-headers             x86_64     3.10.0-957.1.3.el7     updates     8.0 M
 libmpc                     x86_64     1.0.1-3.el7            base         51 k
 mpfr                       x86_64     3.1.1-4.el7            base        203 k
 perl-Carp                  noarch     1.26-244.el7           base         19 k
 perl-Encode                x86_64     2.51-7.el7             base        1.5 M
 perl-Exporter              noarch     5.68-3.el7             base         28 k
 perl-File-Path             noarch     2.09-2.el7             base         26 k
 perl-File-Temp             noarch     0.23.01-3.el7          base         56 k
 perl-Filter                x86_64     1.49-3.el7             base         76 k
 perl-Getopt-Long           noarch     2.40-3.el7             base         56 k
 perl-HTTP-Tiny             noarch     0.033-3.el7            base         38 k
 perl-PathTools             x86_64     3.40-5.el7             base         82 k
 perl-Pod-Escapes           noarch     1:1.04-293.el7         base         51 k
 perl-Pod-Perldoc           noarch     3.20-4.el7             base         87 k
 perl-Pod-Simple            noarch     1:3.28-4.el7           base        216 k
 perl-Pod-Usage             noarch     1.63-3.el7             base         27 k
 perl-Scalar-List-Utils     x86_64     1.27-248.el7           base         36 k
 perl-Socket                x86_64     2.010-4.el7            base         49 k
 perl-Storable              x86_64     2.45-3.el7             base         77 k
 perl-Text-ParseWords       noarch     3.29-4.el7             base         14 k
 perl-Time-HiRes            x86_64     4:1.9725-3.el7         base         45 k
 perl-Time-Local            noarch     1.2300-2.el7           base         24 k
 perl-constant              noarch     1.27-2.el7             base         19 k
 perl-libs                  x86_64     4:5.16.3-293.el7       base        688 k
 perl-macros                x86_64     4:5.16.3-293.el7       base         44 k
 perl-parent                noarch     1:0.225-244.el7        base         12 k
 perl-podlators             noarch     2.5.1-3.el7            base        112 k
 perl-threads               x86_64     1.87-4.el7             base         49 k
 perl-threads-shared        x86_64     1.43-6.el7             base         39 k
Updating for dependencies:
 glibc                      x86_64     2.17-260.el7           base        3.6 M
 glibc-common               x86_64     2.17-260.el7           base         11 M
 libgcc                     x86_64     4.8.5-36.el7           base        102 k
 libgomp                    x86_64     4.8.5-36.el7           base        157 k

Transaction Summary
================================================================================
Install  3 Packages (+32 Dependent packages)
Upgrade  1 Package  (+ 4 Dependent packages)

Total download size: 81 M
Downloading packages:
No Presto metadata available for base
Public key for glibc-2.17-260.el7.x86_64.rpm is not installed
warning: /var/cache/yum/x86_64/7/base/packages/glibc-2.17-260.el7.x86_64.rpm: Header V3 RSA/SHA256 Signature, key ID f4a80eb5: NOKEY
Public key for kernel-headers-3.10.0-957.1.3.el7.x86_64.rpm is not installed
--------------------------------------------------------------------------------
Total                                              2.4 MB/s |  81 MB  00:34     
Retrieving key from file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7
Importing GPG key 0xF4A80EB5:
 Userid     : "CentOS-7 Key (CentOS 7 Official Signing Key) <security@centos.org>"
 Fingerprint: 6341 ab27 53d7 8a78 a7c2 7bb1 24c6 a8a7 f4a8 0eb5
 Package    : centos-release-7-5.1804.4.el7.centos.x86_64 (@koji-override-1)
 From       : /etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Updating   : libgcc-4.8.5-36.el7.x86_64                                  1/45 
  Updating   : glibc-common-2.17-260.el7.x86_64                            2/45 
  Updating   : glibc-2.17-260.el7.x86_64                                   3/45 
  Installing : mpfr-3.1.1-4.el7.x86_64                                     4/45 
  Installing : libmpc-1.0.1-3.el7.x86_64                                   5/45 
  Installing : cpp-4.8.5-36.el7.x86_64                                     6/45 
  Installing : 1:perl-parent-0.225-244.el7.noarch                          7/45 
  Installing : perl-HTTP-Tiny-0.033-3.el7.noarch                           8/45 
  Installing : perl-podlators-2.5.1-3.el7.noarch                           9/45 
  Installing : perl-Pod-Perldoc-3.20-4.el7.noarch                         10/45 
  Installing : 1:perl-Pod-Escapes-1.04-293.el7.noarch                     11/45 
  Installing : perl-Encode-2.51-7.el7.x86_64                              12/45 
  Installing : perl-Text-ParseWords-3.29-4.el7.noarch                     13/45 
  Installing : perl-Pod-Usage-1.63-3.el7.noarch                           14/45 
  Installing : 4:perl-macros-5.16.3-293.el7.x86_64                        15/45 
  Installing : 4:perl-Time-HiRes-1.9725-3.el7.x86_64                      16/45 
  Installing : perl-constant-1.27-2.el7.noarch                            17/45 
  Installing : perl-Carp-1.26-244.el7.noarch                              18/45 
  Installing : perl-Time-Local-1.2300-2.el7.noarch                        19/45 
  Installing : perl-Socket-2.010-4.el7.x86_64                             20/45 
  Installing : perl-Storable-2.45-3.el7.x86_64                            21/45 
  Installing : perl-PathTools-3.40-5.el7.x86_64                           22/45 
  Installing : perl-Scalar-List-Utils-1.27-248.el7.x86_64                 23/45 
  Installing : 1:perl-Pod-Simple-3.28-4.el7.noarch                        24/45 
  Installing : perl-Exporter-5.68-3.el7.noarch                            25/45 
  Installing : perl-File-Temp-0.23.01-3.el7.noarch                        26/45 
  Installing : perl-File-Path-2.09-2.el7.noarch                           27/45 
  Installing : perl-threads-shared-1.43-6.el7.x86_64                      28/45 
  Installing : perl-threads-1.87-4.el7.x86_64                             29/45 
  Installing : perl-Filter-1.49-3.el7.x86_64                              30/45 
  Installing : 4:perl-libs-5.16.3-293.el7.x86_64                          31/45 
  Installing : perl-Getopt-Long-2.40-3.el7.noarch                         32/45 
  Installing : 4:perl-5.16.3-293.el7.x86_64                               33/45 
  Updating   : binutils-2.27-34.base.el7.x86_64                           34/45 
  Updating   : libgomp-4.8.5-36.el7.x86_64                                35/45 
  Installing : kernel-headers-3.10.0-957.1.3.el7.x86_64                   36/45 
  Installing : glibc-headers-2.17-260.el7.x86_64                          37/45 
  Installing : glibc-devel-2.17-260.el7.x86_64                            38/45 
  Installing : gcc-4.8.5-36.el7.x86_64                                    39/45 
  Installing : kernel-devel-3.10.0-957.1.3.el7.x86_64                     40/45 
  Cleanup    : libgomp-4.8.5-28.el7_5.1.x86_64                            41/45 
  Cleanup    : binutils-2.27-28.base.el7_5.1.x86_64                       42/45 
  Cleanup    : glibc-common-2.17-222.el7.x86_64                           43/45 
  Cleanup    : glibc-2.17-222.el7.x86_64                                  44/45 
  Cleanup    : libgcc-4.8.5-28.el7_5.1.x86_64                             45/45 
  Verifying  : perl-HTTP-Tiny-0.033-3.el7.noarch                           1/45 
  Verifying  : perl-threads-shared-1.43-6.el7.x86_64                       2/45 
  Verifying  : 4:perl-Time-HiRes-1.9725-3.el7.x86_64                       3/45 
  Verifying  : mpfr-3.1.1-4.el7.x86_64                                     4/45 
  Verifying  : libgcc-4.8.5-36.el7.x86_64                                  5/45 
  Verifying  : perl-constant-1.27-2.el7.noarch                             6/45 
  Verifying  : perl-PathTools-3.40-5.el7.x86_64                            7/45 
  Verifying  : kernel-headers-3.10.0-957.1.3.el7.x86_64                    8/45 
  Verifying  : perl-Carp-1.26-244.el7.noarch                               9/45 
  Verifying  : 4:perl-macros-5.16.3-293.el7.x86_64                        10/45 
  Verifying  : 1:perl-parent-0.225-244.el7.noarch                         11/45 
  Verifying  : glibc-2.17-260.el7.x86_64                                  12/45 
  Verifying  : gcc-4.8.5-36.el7.x86_64                                    13/45 
  Verifying  : binutils-2.27-34.base.el7.x86_64                           14/45 
  Verifying  : 1:perl-Pod-Simple-3.28-4.el7.noarch                        15/45 
  Verifying  : perl-Time-Local-1.2300-2.el7.noarch                        16/45 
  Verifying  : 1:perl-Pod-Escapes-1.04-293.el7.noarch                     17/45 
  Verifying  : perl-Socket-2.010-4.el7.x86_64                             18/45 
  Verifying  : cpp-4.8.5-36.el7.x86_64                                    19/45 
  Verifying  : libgomp-4.8.5-36.el7.x86_64                                20/45 
  Verifying  : glibc-common-2.17-260.el7.x86_64                           21/45 
  Verifying  : perl-Storable-2.45-3.el7.x86_64                            22/45 
  Verifying  : perl-Scalar-List-Utils-1.27-248.el7.x86_64                 23/45 
  Verifying  : libmpc-1.0.1-3.el7.x86_64                                  24/45 
  Verifying  : perl-File-Temp-0.23.01-3.el7.noarch                        25/45 
  Verifying  : perl-Pod-Usage-1.63-3.el7.noarch                           26/45 
  Verifying  : perl-Encode-2.51-7.el7.x86_64                              27/45 
  Verifying  : perl-Exporter-5.68-3.el7.noarch                            28/45 
  Verifying  : kernel-devel-3.10.0-957.1.3.el7.x86_64                     29/45 
  Verifying  : glibc-devel-2.17-260.el7.x86_64                            30/45 
  Verifying  : perl-Pod-Perldoc-3.20-4.el7.noarch                         31/45 
  Verifying  : perl-podlators-2.5.1-3.el7.noarch                          32/45 
  Verifying  : 4:perl-5.16.3-293.el7.x86_64                               33/45 
  Verifying  : perl-File-Path-2.09-2.el7.noarch                           34/45 
  Verifying  : perl-threads-1.87-4.el7.x86_64                             35/45 
  Verifying  : perl-Filter-1.49-3.el7.x86_64                              36/45 
  Verifying  : perl-Getopt-Long-2.40-3.el7.noarch                         37/45 
  Verifying  : perl-Text-ParseWords-3.29-4.el7.noarch                     38/45 
  Verifying  : 4:perl-libs-5.16.3-293.el7.x86_64                          39/45 
  Verifying  : glibc-headers-2.17-260.el7.x86_64                          40/45 
  Verifying  : libgomp-4.8.5-28.el7_5.1.x86_64                            41/45 
  Verifying  : glibc-2.17-222.el7.x86_64                                  42/45 
  Verifying  : libgcc-4.8.5-28.el7_5.1.x86_64                             43/45 
  Verifying  : glibc-common-2.17-222.el7.x86_64                           44/45 
  Verifying  : binutils-2.27-28.base.el7_5.1.x86_64                       45/45 

Installed:
  gcc.x86_64 0:4.8.5-36.el7        kernel-devel.x86_64 0:3.10.0-957.1.3.el7    
  perl.x86_64 4:5.16.3-293.el7    

Dependency Installed:
  cpp.x86_64 0:4.8.5-36.el7                                                     
  glibc-devel.x86_64 0:2.17-260.el7                                             
  glibc-headers.x86_64 0:2.17-260.el7                                           
  kernel-headers.x86_64 0:3.10.0-957.1.3.el7                                    
  libmpc.x86_64 0:1.0.1-3.el7                                                   
  mpfr.x86_64 0:3.1.1-4.el7                                                     
  perl-Carp.noarch 0:1.26-244.el7                                               
  perl-Encode.x86_64 0:2.51-7.el7                                               
  perl-Exporter.noarch 0:5.68-3.el7                                             
  perl-File-Path.noarch 0:2.09-2.el7                                            
  perl-File-Temp.noarch 0:0.23.01-3.el7                                         
  perl-Filter.x86_64 0:1.49-3.el7                                               
  perl-Getopt-Long.noarch 0:2.40-3.el7                                          
  perl-HTTP-Tiny.noarch 0:0.033-3.el7                                           
  perl-PathTools.x86_64 0:3.40-5.el7                                            
  perl-Pod-Escapes.noarch 1:1.04-293.el7                                        
  perl-Pod-Perldoc.noarch 0:3.20-4.el7                                          
  perl-Pod-Simple.noarch 1:3.28-4.el7                                           
  perl-Pod-Usage.noarch 0:1.63-3.el7                                            
  perl-Scalar-List-Utils.x86_64 0:1.27-248.el7                                  
  perl-Socket.x86_64 0:2.010-4.el7                                              
  perl-Storable.x86_64 0:2.45-3.el7                                             
  perl-Text-ParseWords.noarch 0:3.29-4.el7                                      
  perl-Time-HiRes.x86_64 4:1.9725-3.el7                                         
  perl-Time-Local.noarch 0:1.2300-2.el7                                         
  perl-constant.noarch 0:1.27-2.el7                                             
  perl-libs.x86_64 4:5.16.3-293.el7                                             
  perl-macros.x86_64 4:5.16.3-293.el7                                           
  perl-parent.noarch 1:0.225-244.el7                                            
  perl-podlators.noarch 0:2.5.1-3.el7                                           
  perl-threads.x86_64 0:1.87-4.el7                                              
  perl-threads-shared.x86_64 0:1.43-6.el7                                       

Updated:
  binutils.x86_64 0:2.27-34.base.el7                                            

Dependency Updated:
  glibc.x86_64 0:2.17-260.el7         glibc-common.x86_64 0:2.17-260.el7       
  libgcc.x86_64 0:4.8.5-36.el7        libgomp.x86_64 0:4.8.5-36.el7            

Complete!
Downloading VirtualBox Guest Additions ISO from http://download.virtualbox.org/virtualbox/5.2.10/VBoxGuestAdditions_5.2.10.iso
Copy iso file /home/davar/.vagrant.d/tmp/VBoxGuestAdditions_5.2.10.iso into the box /tmp/VBoxGuestAdditions.iso
Mounting Virtualbox Guest Additions ISO to: /mnt
mount: /dev/loop0 is write-protected, mounting read-only
Installing Virtualbox Guest Additions 5.2.10 - guest version is unknown
Verifying archive integrity... All good.
Uncompressing VirtualBox 5.2.10 Guest Additions for Linux........
VirtualBox Guest Additions installer
Copying additional installer modules ...
Installing additional modules ...
VirtualBox Guest Additions: Building the VirtualBox Guest Additions kernel modules.
This system is currently not set up to build kernel modules.
Please install the Linux kernel "header" files matching the current kernel
for adding new hardware support to the system.
The distribution packages containing the headers are probably:
    kernel-devel kernel-devel-3.10.0-862.14.4.el7.x86_64
VirtualBox Guest Additions: Starting.
VirtualBox Guest Additions: Building the VirtualBox Guest Additions kernel modules.
This system is currently not set up to build kernel modules.
Please install the Linux kernel "header" files matching the current kernel
for adding new hardware support to the system.
The distribution packages containing the headers are probably:
    kernel-devel kernel-devel-3.10.0-862.14.4.el7.x86_64
An error occurred during installation of VirtualBox Guest Additions 5.2.10. Some functionality may not work as intended.
In most cases it is OK that the "Window System drivers" installation failed.
Redirecting to /bin/systemctl start vboxadd.service
Job for vboxadd.service failed because the control process exited with error code. See "systemctl status vboxadd.service" and "journalctl -xe" for details.
Unmounting Virtualbox Guest Additions ISO from: /mnt
Cleaning up downloaded VirtualBox Guest Additions ISO...
==> hadoop-00: Checking for guest additions in VM...
    hadoop-00: No guest additions were detected on the base box for this VM! Guest
    hadoop-00: additions are required for forwarded ports, shared folders, host only
    hadoop-00: networking, and more. If SSH fails on this machine, please install
    hadoop-00: the guest additions and repackage the box to continue.
    hadoop-00: 
    hadoop-00: This is not an error message; everything may continue to work properly,
    hadoop-00: in which case you may ignore this message.
==> hadoop-00: Setting hostname...
==> hadoop-00: Configuring and enabling network interfaces...
    hadoop-00: SSH address: 127.0.0.1:2222
    hadoop-00: SSH username: vagrant
    hadoop-00: SSH auth method: private key
==> hadoop-00: Rsyncing folder: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/ => /vagrant
==> hadoop-00: Running provisioner: file...
==> hadoop-00: Running provisioner: shell...
    hadoop-00: Running: /tmp/vagrant-shell20181212-22415-lg1xn5.sh
    hadoop-00: Generating public/private rsa key pair.
    hadoop-00: Your identification has been saved in /home/swift/.ssh/id_rsa.
    hadoop-00: Your public key has been saved in /home/swift/.ssh/id_rsa.pub.
    hadoop-00: The key fingerprint is:
    hadoop-00: SHA256:w8yh7aggqsja737hbVjFUMoWP1Qg53a+cRqErfCah4E root@hadoop-00
    hadoop-00: The key's randomart image is:
    hadoop-00: +---[RSA 2048]----+
    hadoop-00: |        o.=o.    |
    hadoop-00: |       ..O o     |
    hadoop-00: |        *o* +    |
    hadoop-00: |       O =o*     |
    hadoop-00: |      E S.o + .  |
    hadoop-00: |      .o.*   *   |
    hadoop-00: |. .  ..== . o    |
    hadoop-00: |+o . .+ o.       |
    hadoop-00: |B..+=. .         |
    hadoop-00: +----[SHA256]-----+
==> hadoop-01: Importing base box 'centos/7'...
==> hadoop-01: Matching MAC address for NAT networking...
==> hadoop-01: Setting the name of the VM: hadoop-01
==> hadoop-01: Fixed port collision for 22 => 2222. Now on port 2200.
==> hadoop-01: Clearing any previously set network interfaces...
==> hadoop-01: Preparing network interfaces based on configuration...
    hadoop-01: Adapter 1: nat
    hadoop-01: Adapter 2: hostonly
==> hadoop-01: Forwarding ports...
    hadoop-01: 22 (guest) => 2200 (host) (adapter 1)
==> hadoop-01: Running 'pre-boot' VM customizations...
==> hadoop-01: Booting VM...
==> hadoop-01: Waiting for machine to boot. This may take a few minutes...
    hadoop-01: SSH address: 127.0.0.1:2200
    hadoop-01: SSH username: vagrant
    hadoop-01: SSH auth method: private key
    hadoop-01: 
    hadoop-01: Vagrant insecure key detected. Vagrant will automatically replace
    hadoop-01: this with a newly generated keypair for better security.
    hadoop-01: 
    hadoop-01: Inserting generated public key within guest...
    hadoop-01: Removing insecure key from the guest if it's present...
    hadoop-01: Key inserted! Disconnecting and reconnecting using new SSH key...
==> hadoop-01: Machine booted and ready!
[hadoop-01] No installation found.
Loaded plugins: fastestmirror
Determining fastest mirrors
 * base: mirrors.netix.net
 * extras: mirrors.pidginhost.com
 * updates: mirrors.pidginhost.com
No package kernel-devel-3.10.0-862.14.4.el7.x86_64 available.
Package 1:make-3.82-23.el7.x86_64 already installed and latest version
Package bzip2-1.0.6-13.el7.x86_64 already installed and latest version
Resolving Dependencies
--> Running transaction check
---> Package binutils.x86_64 0:2.27-28.base.el7_5.1 will be updated
---> Package binutils.x86_64 0:2.27-34.base.el7 will be an update
---> Package gcc.x86_64 0:4.8.5-36.el7 will be installed
--> Processing Dependency: libgomp = 4.8.5-36.el7 for package: gcc-4.8.5-36.el7.x86_64
--> Processing Dependency: cpp = 4.8.5-36.el7 for package: gcc-4.8.5-36.el7.x86_64
--> Processing Dependency: libgcc >= 4.8.5-36.el7 for package: gcc-4.8.5-36.el7.x86_64
--> Processing Dependency: glibc-devel >= 2.2.90-12 for package: gcc-4.8.5-36.el7.x86_64
--> Processing Dependency: libmpfr.so.4()(64bit) for package: gcc-4.8.5-36.el7.x86_64
--> Processing Dependency: libmpc.so.3()(64bit) for package: gcc-4.8.5-36.el7.x86_64
---> Package kernel-devel.x86_64 0:3.10.0-957.1.3.el7 will be installed
---> Package perl.x86_64 4:5.16.3-293.el7 will be installed
--> Processing Dependency: perl-libs = 4:5.16.3-293.el7 for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(Socket) >= 1.3 for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(Scalar::Util) >= 1.10 for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl-macros for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl-libs for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(threads::shared) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(threads) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(constant) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(Time::Local) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(Time::HiRes) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(Storable) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(Socket) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(Scalar::Util) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(Pod::Simple::XHTML) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(Pod::Simple::Search) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(Getopt::Long) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(Filter::Util::Call) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(File::Temp) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(File::Spec::Unix) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(File::Spec::Functions) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(File::Spec) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(File::Path) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(Exporter) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(Cwd) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: perl(Carp) for package: 4:perl-5.16.3-293.el7.x86_64
--> Processing Dependency: libperl.so()(64bit) for package: 4:perl-5.16.3-293.el7.x86_64
--> Running transaction check
---> Package cpp.x86_64 0:4.8.5-36.el7 will be installed
---> Package glibc-devel.x86_64 0:2.17-260.el7 will be installed
--> Processing Dependency: glibc-headers = 2.17-260.el7 for package: glibc-devel-2.17-260.el7.x86_64
--> Processing Dependency: glibc = 2.17-260.el7 for package: glibc-devel-2.17-260.el7.x86_64
--> Processing Dependency: glibc-headers for package: glibc-devel-2.17-260.el7.x86_64
---> Package libgcc.x86_64 0:4.8.5-28.el7_5.1 will be updated
---> Package libgcc.x86_64 0:4.8.5-36.el7 will be an update
---> Package libgomp.x86_64 0:4.8.5-28.el7_5.1 will be updated
---> Package libgomp.x86_64 0:4.8.5-36.el7 will be an update
---> Package libmpc.x86_64 0:1.0.1-3.el7 will be installed
---> Package mpfr.x86_64 0:3.1.1-4.el7 will be installed
---> Package perl-Carp.noarch 0:1.26-244.el7 will be installed
---> Package perl-Exporter.noarch 0:5.68-3.el7 will be installed
---> Package perl-File-Path.noarch 0:2.09-2.el7 will be installed
---> Package perl-File-Temp.noarch 0:0.23.01-3.el7 will be installed
---> Package perl-Filter.x86_64 0:1.49-3.el7 will be installed
---> Package perl-Getopt-Long.noarch 0:2.40-3.el7 will be installed
--> Processing Dependency: perl(Pod::Usage) >= 1.14 for package: perl-Getopt-Long-2.40-3.el7.noarch
--> Processing Dependency: perl(Text::ParseWords) for package: perl-Getopt-Long-2.40-3.el7.noarch
---> Package perl-PathTools.x86_64 0:3.40-5.el7 will be installed
---> Package perl-Pod-Simple.noarch 1:3.28-4.el7 will be installed
--> Processing Dependency: perl(Pod::Escapes) >= 1.04 for package: 1:perl-Pod-Simple-3.28-4.el7.noarch
--> Processing Dependency: perl(Encode) for package: 1:perl-Pod-Simple-3.28-4.el7.noarch
---> Package perl-Scalar-List-Utils.x86_64 0:1.27-248.el7 will be installed
---> Package perl-Socket.x86_64 0:2.010-4.el7 will be installed
---> Package perl-Storable.x86_64 0:2.45-3.el7 will be installed
---> Package perl-Time-HiRes.x86_64 4:1.9725-3.el7 will be installed
---> Package perl-Time-Local.noarch 0:1.2300-2.el7 will be installed
---> Package perl-constant.noarch 0:1.27-2.el7 will be installed
---> Package perl-libs.x86_64 4:5.16.3-293.el7 will be installed
---> Package perl-macros.x86_64 4:5.16.3-293.el7 will be installed
---> Package perl-threads.x86_64 0:1.87-4.el7 will be installed
---> Package perl-threads-shared.x86_64 0:1.43-6.el7 will be installed
--> Running transaction check
---> Package glibc.x86_64 0:2.17-222.el7 will be updated
--> Processing Dependency: glibc = 2.17-222.el7 for package: glibc-common-2.17-222.el7.x86_64
---> Package glibc.x86_64 0:2.17-260.el7 will be an update
---> Package glibc-headers.x86_64 0:2.17-260.el7 will be installed
--> Processing Dependency: kernel-headers >= 2.2.1 for package: glibc-headers-2.17-260.el7.x86_64
--> Processing Dependency: kernel-headers for package: glibc-headers-2.17-260.el7.x86_64
---> Package perl-Encode.x86_64 0:2.51-7.el7 will be installed
---> Package perl-Pod-Escapes.noarch 1:1.04-293.el7 will be installed
---> Package perl-Pod-Usage.noarch 0:1.63-3.el7 will be installed
--> Processing Dependency: perl(Pod::Text) >= 3.15 for package: perl-Pod-Usage-1.63-3.el7.noarch
--> Processing Dependency: perl-Pod-Perldoc for package: perl-Pod-Usage-1.63-3.el7.noarch
---> Package perl-Text-ParseWords.noarch 0:3.29-4.el7 will be installed
--> Running transaction check
---> Package glibc-common.x86_64 0:2.17-222.el7 will be updated
---> Package glibc-common.x86_64 0:2.17-260.el7 will be an update
---> Package kernel-headers.x86_64 0:3.10.0-957.1.3.el7 will be installed
---> Package perl-Pod-Perldoc.noarch 0:3.20-4.el7 will be installed
--> Processing Dependency: perl(parent) for package: perl-Pod-Perldoc-3.20-4.el7.noarch
--> Processing Dependency: perl(HTTP::Tiny) for package: perl-Pod-Perldoc-3.20-4.el7.noarch
---> Package perl-podlators.noarch 0:2.5.1-3.el7 will be installed
--> Running transaction check
---> Package perl-HTTP-Tiny.noarch 0:0.033-3.el7 will be installed
---> Package perl-parent.noarch 1:0.225-244.el7 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

================================================================================
 Package                    Arch       Version                Repository   Size
================================================================================
Installing:
 gcc                        x86_64     4.8.5-36.el7           base         16 M
 kernel-devel               x86_64     3.10.0-957.1.3.el7     updates      17 M
 perl                       x86_64     4:5.16.3-293.el7       base        8.0 M
Updating:
 binutils                   x86_64     2.27-34.base.el7       base        5.9 M
Installing for dependencies:
 cpp                        x86_64     4.8.5-36.el7           base        5.9 M
 glibc-devel                x86_64     2.17-260.el7           base        1.1 M
 glibc-headers              x86_64     2.17-260.el7           base        683 k
 kernel-headers             x86_64     3.10.0-957.1.3.el7     updates     8.0 M
 libmpc                     x86_64     1.0.1-3.el7            base         51 k
 mpfr                       x86_64     3.1.1-4.el7            base        203 k
 perl-Carp                  noarch     1.26-244.el7           base         19 k
 perl-Encode                x86_64     2.51-7.el7             base        1.5 M
 perl-Exporter              noarch     5.68-3.el7             base         28 k
 perl-File-Path             noarch     2.09-2.el7             base         26 k
 perl-File-Temp             noarch     0.23.01-3.el7          base         56 k
 perl-Filter                x86_64     1.49-3.el7             base         76 k
 perl-Getopt-Long           noarch     2.40-3.el7             base         56 k
 perl-HTTP-Tiny             noarch     0.033-3.el7            base         38 k
 perl-PathTools             x86_64     3.40-5.el7             base         82 k
 perl-Pod-Escapes           noarch     1:1.04-293.el7         base         51 k
 perl-Pod-Perldoc           noarch     3.20-4.el7             base         87 k
 perl-Pod-Simple            noarch     1:3.28-4.el7           base        216 k
 perl-Pod-Usage             noarch     1.63-3.el7             base         27 k
 perl-Scalar-List-Utils     x86_64     1.27-248.el7           base         36 k
 perl-Socket                x86_64     2.010-4.el7            base         49 k
 perl-Storable              x86_64     2.45-3.el7             base         77 k
 perl-Text-ParseWords       noarch     3.29-4.el7             base         14 k
 perl-Time-HiRes            x86_64     4:1.9725-3.el7         base         45 k
 perl-Time-Local            noarch     1.2300-2.el7           base         24 k
 perl-constant              noarch     1.27-2.el7             base         19 k
 perl-libs                  x86_64     4:5.16.3-293.el7       base        688 k
 perl-macros                x86_64     4:5.16.3-293.el7       base         44 k
 perl-parent                noarch     1:0.225-244.el7        base         12 k
 perl-podlators             noarch     2.5.1-3.el7            base        112 k
 perl-threads               x86_64     1.87-4.el7             base         49 k
 perl-threads-shared        x86_64     1.43-6.el7             base         39 k
Updating for dependencies:
 glibc                      x86_64     2.17-260.el7           base        3.6 M
 glibc-common               x86_64     2.17-260.el7           base         11 M
 libgcc                     x86_64     4.8.5-36.el7           base        102 k
 libgomp                    x86_64     4.8.5-36.el7           base        157 k

Transaction Summary
================================================================================
Install  3 Packages (+32 Dependent packages)
Upgrade  1 Package  (+ 4 Dependent packages)

Total download size: 81 M
Downloading packages:
No Presto metadata available for base
Public key for glibc-2.17-260.el7.x86_64.rpm is not installed
warning: /var/cache/yum/x86_64/7/base/packages/glibc-2.17-260.el7.x86_64.rpm: Header V3 RSA/SHA256 Signature, key ID f4a80eb5: NOKEY
Public key for kernel-headers-3.10.0-957.1.3.el7.x86_64.rpm is not installed
--------------------------------------------------------------------------------
Total                                              2.5 MB/s |  81 MB  00:33     
Retrieving key from file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7
Importing GPG key 0xF4A80EB5:
 Userid     : "CentOS-7 Key (CentOS 7 Official Signing Key) <security@centos.org>"
 Fingerprint: 6341 ab27 53d7 8a78 a7c2 7bb1 24c6 a8a7 f4a8 0eb5
 Package    : centos-release-7-5.1804.4.el7.centos.x86_64 (@koji-override-1)
 From       : /etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Updating   : libgcc-4.8.5-36.el7.x86_64                                  1/45 
  Updating   : glibc-common-2.17-260.el7.x86_64                            2/45 
  Updating   : glibc-2.17-260.el7.x86_64                                   3/45 
  Installing : mpfr-3.1.1-4.el7.x86_64                                     4/45 
  Installing : libmpc-1.0.1-3.el7.x86_64                                   5/45 
  Installing : cpp-4.8.5-36.el7.x86_64                                     6/45 
  Installing : 1:perl-parent-0.225-244.el7.noarch                          7/45 
  Installing : perl-HTTP-Tiny-0.033-3.el7.noarch                           8/45 
  Installing : perl-podlators-2.5.1-3.el7.noarch                           9/45 
  Installing : perl-Pod-Perldoc-3.20-4.el7.noarch                         10/45 
  Installing : 1:perl-Pod-Escapes-1.04-293.el7.noarch                     11/45 
  Installing : perl-Encode-2.51-7.el7.x86_64                              12/45 
  Installing : perl-Text-ParseWords-3.29-4.el7.noarch                     13/45 
  Installing : perl-Pod-Usage-1.63-3.el7.noarch                           14/45 
  Installing : 4:perl-macros-5.16.3-293.el7.x86_64                        15/45 
  Installing : 4:perl-Time-HiRes-1.9725-3.el7.x86_64                      16/45 
  Installing : perl-constant-1.27-2.el7.noarch                            17/45 
  Installing : perl-Carp-1.26-244.el7.noarch                              18/45 
  Installing : perl-Time-Local-1.2300-2.el7.noarch                        19/45 
  Installing : perl-Socket-2.010-4.el7.x86_64                             20/45 
  Installing : perl-Storable-2.45-3.el7.x86_64                            21/45 
  Installing : perl-PathTools-3.40-5.el7.x86_64                           22/45 
  Installing : perl-Scalar-List-Utils-1.27-248.el7.x86_64                 23/45 
  Installing : 1:perl-Pod-Simple-3.28-4.el7.noarch                        24/45 
  Installing : perl-Exporter-5.68-3.el7.noarch                            25/45 
  Installing : perl-File-Temp-0.23.01-3.el7.noarch                        26/45 
  Installing : perl-File-Path-2.09-2.el7.noarch                           27/45 
  Installing : perl-threads-shared-1.43-6.el7.x86_64                      28/45 
  Installing : perl-threads-1.87-4.el7.x86_64                             29/45 
  Installing : perl-Filter-1.49-3.el7.x86_64                              30/45 
  Installing : 4:perl-libs-5.16.3-293.el7.x86_64                          31/45 
  Installing : perl-Getopt-Long-2.40-3.el7.noarch                         32/45 
  Installing : 4:perl-5.16.3-293.el7.x86_64                               33/45 
  Updating   : binutils-2.27-34.base.el7.x86_64                           34/45 
  Updating   : libgomp-4.8.5-36.el7.x86_64                                35/45 
  Installing : kernel-headers-3.10.0-957.1.3.el7.x86_64                   36/45 
  Installing : glibc-headers-2.17-260.el7.x86_64                          37/45 
  Installing : glibc-devel-2.17-260.el7.x86_64                            38/45 
  Installing : gcc-4.8.5-36.el7.x86_64                                    39/45 
  Installing : kernel-devel-3.10.0-957.1.3.el7.x86_64                     40/45 
  Cleanup    : libgomp-4.8.5-28.el7_5.1.x86_64                            41/45 
  Cleanup    : binutils-2.27-28.base.el7_5.1.x86_64                       42/45 
  Cleanup    : glibc-common-2.17-222.el7.x86_64                           43/45 
  Cleanup    : glibc-2.17-222.el7.x86_64                                  44/45 
  Cleanup    : libgcc-4.8.5-28.el7_5.1.x86_64                             45/45 
  Verifying  : perl-HTTP-Tiny-0.033-3.el7.noarch                           1/45 
  Verifying  : perl-threads-shared-1.43-6.el7.x86_64                       2/45 
  Verifying  : 4:perl-Time-HiRes-1.9725-3.el7.x86_64                       3/45 
  Verifying  : mpfr-3.1.1-4.el7.x86_64                                     4/45 
  Verifying  : libgcc-4.8.5-36.el7.x86_64                                  5/45 
  Verifying  : perl-constant-1.27-2.el7.noarch                             6/45 
  Verifying  : perl-PathTools-3.40-5.el7.x86_64                            7/45 
  Verifying  : kernel-headers-3.10.0-957.1.3.el7.x86_64                    8/45 
  Verifying  : perl-Carp-1.26-244.el7.noarch                               9/45 
  Verifying  : 4:perl-macros-5.16.3-293.el7.x86_64                        10/45 
  Verifying  : 1:perl-parent-0.225-244.el7.noarch                         11/45 
  Verifying  : glibc-2.17-260.el7.x86_64                                  12/45 
  Verifying  : gcc-4.8.5-36.el7.x86_64                                    13/45 
  Verifying  : binutils-2.27-34.base.el7.x86_64                           14/45 
  Verifying  : 1:perl-Pod-Simple-3.28-4.el7.noarch                        15/45 
  Verifying  : perl-Time-Local-1.2300-2.el7.noarch                        16/45 
  Verifying  : 1:perl-Pod-Escapes-1.04-293.el7.noarch                     17/45 
  Verifying  : perl-Socket-2.010-4.el7.x86_64                             18/45 
  Verifying  : cpp-4.8.5-36.el7.x86_64                                    19/45 
  Verifying  : libgomp-4.8.5-36.el7.x86_64                                20/45 
  Verifying  : glibc-common-2.17-260.el7.x86_64                           21/45 
  Verifying  : perl-Storable-2.45-3.el7.x86_64                            22/45 
  Verifying  : perl-Scalar-List-Utils-1.27-248.el7.x86_64                 23/45 
  Verifying  : libmpc-1.0.1-3.el7.x86_64                                  24/45 
  Verifying  : perl-File-Temp-0.23.01-3.el7.noarch                        25/45 
  Verifying  : perl-Pod-Usage-1.63-3.el7.noarch                           26/45 
  Verifying  : perl-Encode-2.51-7.el7.x86_64                              27/45 
  Verifying  : perl-Exporter-5.68-3.el7.noarch                            28/45 
  Verifying  : kernel-devel-3.10.0-957.1.3.el7.x86_64                     29/45 
  Verifying  : glibc-devel-2.17-260.el7.x86_64                            30/45 
  Verifying  : perl-Pod-Perldoc-3.20-4.el7.noarch                         31/45 
  Verifying  : perl-podlators-2.5.1-3.el7.noarch                          32/45 
  Verifying  : 4:perl-5.16.3-293.el7.x86_64                               33/45 
  Verifying  : perl-File-Path-2.09-2.el7.noarch                           34/45 
  Verifying  : perl-threads-1.87-4.el7.x86_64                             35/45 
  Verifying  : perl-Filter-1.49-3.el7.x86_64                              36/45 
  Verifying  : perl-Getopt-Long-2.40-3.el7.noarch                         37/45 
  Verifying  : perl-Text-ParseWords-3.29-4.el7.noarch                     38/45 
  Verifying  : 4:perl-libs-5.16.3-293.el7.x86_64                          39/45 
  Verifying  : glibc-headers-2.17-260.el7.x86_64                          40/45 
  Verifying  : libgomp-4.8.5-28.el7_5.1.x86_64                            41/45 
  Verifying  : glibc-2.17-222.el7.x86_64                                  42/45 
  Verifying  : libgcc-4.8.5-28.el7_5.1.x86_64                             43/45 
  Verifying  : glibc-common-2.17-222.el7.x86_64                           44/45 
  Verifying  : binutils-2.27-28.base.el7_5.1.x86_64                       45/45 

Installed:
  gcc.x86_64 0:4.8.5-36.el7        kernel-devel.x86_64 0:3.10.0-957.1.3.el7    
  perl.x86_64 4:5.16.3-293.el7    

Dependency Installed:
  cpp.x86_64 0:4.8.5-36.el7                                                     
  glibc-devel.x86_64 0:2.17-260.el7                                             
  glibc-headers.x86_64 0:2.17-260.el7                                           
  kernel-headers.x86_64 0:3.10.0-957.1.3.el7                                    
  libmpc.x86_64 0:1.0.1-3.el7                                                   
  mpfr.x86_64 0:3.1.1-4.el7                                                     
  perl-Carp.noarch 0:1.26-244.el7                                               
  perl-Encode.x86_64 0:2.51-7.el7                                               
  perl-Exporter.noarch 0:5.68-3.el7                                             
  perl-File-Path.noarch 0:2.09-2.el7                                            
  perl-File-Temp.noarch 0:0.23.01-3.el7                                         
  perl-Filter.x86_64 0:1.49-3.el7                                               
  perl-Getopt-Long.noarch 0:2.40-3.el7                                          
  perl-HTTP-Tiny.noarch 0:0.033-3.el7                                           
  perl-PathTools.x86_64 0:3.40-5.el7                                            
  perl-Pod-Escapes.noarch 1:1.04-293.el7                                        
  perl-Pod-Perldoc.noarch 0:3.20-4.el7                                          
  perl-Pod-Simple.noarch 1:3.28-4.el7                                           
  perl-Pod-Usage.noarch 0:1.63-3.el7                                            
  perl-Scalar-List-Utils.x86_64 0:1.27-248.el7                                  
  perl-Socket.x86_64 0:2.010-4.el7                                              
  perl-Storable.x86_64 0:2.45-3.el7                                             
  perl-Text-ParseWords.noarch 0:3.29-4.el7                                      
  perl-Time-HiRes.x86_64 4:1.9725-3.el7                                         
  perl-Time-Local.noarch 0:1.2300-2.el7                                         
  perl-constant.noarch 0:1.27-2.el7                                             
  perl-libs.x86_64 4:5.16.3-293.el7                                             
  perl-macros.x86_64 4:5.16.3-293.el7                                           
  perl-parent.noarch 1:0.225-244.el7                                            
  perl-podlators.noarch 0:2.5.1-3.el7                                           
  perl-threads.x86_64 0:1.87-4.el7                                              
  perl-threads-shared.x86_64 0:1.43-6.el7                                       

Updated:
  binutils.x86_64 0:2.27-34.base.el7                                            

Dependency Updated:
  glibc.x86_64 0:2.17-260.el7         glibc-common.x86_64 0:2.17-260.el7       
  libgcc.x86_64 0:4.8.5-36.el7        libgomp.x86_64 0:4.8.5-36.el7            

Complete!
Downloading VirtualBox Guest Additions ISO from http://download.virtualbox.org/virtualbox/5.2.10/VBoxGuestAdditions_5.2.10.iso
Copy iso file /home/davar/.vagrant.d/tmp/VBoxGuestAdditions_5.2.10.iso into the box /tmp/VBoxGuestAdditions.iso
Mounting Virtualbox Guest Additions ISO to: /mnt
mount: /dev/loop0 is write-protected, mounting read-only
Installing Virtualbox Guest Additions 5.2.10 - guest version is unknown
Verifying archive integrity... All good.
Uncompressing VirtualBox 5.2.10 Guest Additions for Linux........
VirtualBox Guest Additions installer
Copying additional installer modules ...
Installing additional modules ...
VirtualBox Guest Additions: Building the VirtualBox Guest Additions kernel modules.
This system is currently not set up to build kernel modules.
Please install the Linux kernel "header" files matching the current kernel
for adding new hardware support to the system.
The distribution packages containing the headers are probably:
    kernel-devel kernel-devel-3.10.0-862.14.4.el7.x86_64
VirtualBox Guest Additions: Starting.
VirtualBox Guest Additions: Building the VirtualBox Guest Additions kernel modules.
This system is currently not set up to build kernel modules.
Please install the Linux kernel "header" files matching the current kernel
for adding new hardware support to the system.
The distribution packages containing the headers are probably:
    kernel-devel kernel-devel-3.10.0-862.14.4.el7.x86_64
An error occurred during installation of VirtualBox Guest Additions 5.2.10. Some functionality may not work as intended.
In most cases it is OK that the "Window System drivers" installation failed.
Redirecting to /bin/systemctl start vboxadd.service
Job for vboxadd.service failed because the control process exited with error code. See "systemctl status vboxadd.service" and "journalctl -xe" for details.
Unmounting Virtualbox Guest Additions ISO from: /mnt
Cleaning up downloaded VirtualBox Guest Additions ISO...
==> hadoop-01: Checking for guest additions in VM...
    hadoop-01: No guest additions were detected on the base box for this VM! Guest
    hadoop-01: additions are required for forwarded ports, shared folders, host only
    hadoop-01: networking, and more. If SSH fails on this machine, please install
    hadoop-01: the guest additions and repackage the box to continue.
    hadoop-01: 
    hadoop-01: This is not an error message; everything may continue to work properly,
    hadoop-01: in which case you may ignore this message.
==> hadoop-01: Setting hostname...
==> hadoop-01: Configuring and enabling network interfaces...
    hadoop-01: SSH address: 127.0.0.1:2200
    hadoop-01: SSH username: vagrant
    hadoop-01: SSH auth method: private key
==> hadoop-01: Rsyncing folder: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/ => /vagrant
==> hadoop-01: Running provisioner: file...
==> hadoop-01: Running provisioner: shell...
    hadoop-01: Running: /tmp/vagrant-shell20181212-22415-1rqigwr.sh
    hadoop-01: Generating public/private rsa key pair.
    hadoop-01: Your identification has been saved in /home/swift/.ssh/id_rsa.
    hadoop-01: Your public key has been saved in /home/swift/.ssh/id_rsa.pub.
    hadoop-01: The key fingerprint is:
    hadoop-01: SHA256:4FZVV3TY0ygUbC+nYSxsl/It29YUGj29tO5FGNP+aCs root@hadoop-01
    hadoop-01: The key's randomart image is:
    hadoop-01: +---[RSA 2048]----+
    hadoop-01: |          .++..*=|
    hadoop-01: |         .  +.oo+|
    hadoop-01: |      . .. o ++ +|
    hadoop-01: |     . o  = B.oX.|
    hadoop-01: |      o S. * *= B|
    hadoop-01: |     .      +..=o|
    hadoop-01: |             ++oo|
    hadoop-01: |            E.ooo|
    hadoop-01: |             oo. |
    hadoop-01: +----[SHA256]-----+
davar@home ~/LABS/ansible-hadoop-spark-playground-multi-node/inventories/hadoop $ ansible-playbook -i inventories/hadoop hadoop.yaml
^C
davar@home ~/LABS/ansible-hadoop-spark-playground-multi-node/inventories/hadoop $ ls
_groups.yml  group_vars  hosts.py
davar@home ~/LABS/ansible-hadoop-spark-playground-multi-node/inventories/hadoop $ cat _groups.yml 
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



davar@home ~/LABS/ansible-hadoop-spark-playground-multi-node/inventories/hadoop $ grep node _groups.yml 
  - name: hdfs_namenode
    hosts: [node_00]
  - name: hdfs_datanode
    hosts: [node_00, node_01]
    children: [hdfs_namenode, hdfs_datanode]
    hosts: [node_00]
  - name: yarn_node_mgr
    hosts: [node_00, node_01]
    hosts: [node_00]
    children: [yarn_resource_mgr, yarn_node_mgr, yarn_proxyserver]
    hosts: [node_01]
    hosts: [node_01]
    hosts: [node_01]
  - name: hadoop_all_nodes
davar@home ~/LABS/ansible-hadoop-spark-playground-multi-node/inventories/hadoop $ cd ..
davar@home ~/LABS/ansible-hadoop-spark-playground-multi-node/inventories $ cd ..
davar@home ~/LABS/ansible-hadoop-spark-playground-multi-node $ ansible-playbook -i inventories/hadoop hadoop.yaml
 [ERROR]:


PLAY [Install Hadoop] ****************************************************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************************************************
Wednesday 12 December 2018  03:28:42 +0200 (0:00:00.622)       0:00:00.622 **** 
ok: [node_01]
ok: [node_00]

TASK [basic/system : debug] **********************************************************************************************************************************
Wednesday 12 December 2018  03:28:44 +0200 (0:00:02.949)       0:00:03.572 **** 
ok: [node_00] => {
    "msg": "osfamily:RedHat , distribution:CentOS , release:Core , version:7(7.5.1804) , pkg:yum\n"
}
ok: [node_01] => {
    "msg": "osfamily:RedHat , distribution:CentOS , release:Core , version:7(7.5.1804) , pkg:yum\n"
}

TASK [basic/system : include_vars] ***************************************************************************************************************************
Wednesday 12 December 2018  03:28:45 +0200 (0:00:00.108)       0:00:03.680 **** 
ok: [node_00] => (item=/home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/basic/system/vars/os/RedHat.yml)
ok: [node_01] => (item=/home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/basic/system/vars/os/RedHat.yml)

TASK [basic/hosts : debug] ***********************************************************************************************************************************
Wednesday 12 December 2018  03:28:45 +0200 (0:00:00.119)       0:00:03.799 **** 
ok: [node_00] => {
    "msg": "Will set hostname as cluster-node-00"
}
ok: [node_01] => {
    "msg": "Will set hostname as cluster-node-01"
}

TASK [basic/hosts : Set hostname] ****************************************************************************************************************************
Wednesday 12 December 2018  03:28:45 +0200 (0:00:00.105)       0:00:03.905 **** 
changed: [node_01]
changed: [node_00]

TASK [basic/hosts : set_fact] ********************************************************************************************************************************
Wednesday 12 December 2018  03:28:46 +0200 (0:00:01.460)       0:00:05.365 **** 
ok: [node_00]
ok: [node_01]

TASK [basic/hosts : Update /etc/hosts : drop 127.0.0.1 to hostname (avoid address binding problem)] **********************************************************
Wednesday 12 December 2018  03:28:46 +0200 (0:00:00.156)       0:00:05.521 **** 
ok: [node_01]
ok: [node_00]

TASK [basic/hosts : Update /etc/hosts : add hostnames] *******************************************************************************************************
Wednesday 12 December 2018  03:28:47 +0200 (0:00:00.812)       0:00:06.334 **** 
changed: [node_00] => (item=node_00)
changed: [node_01] => (item=node_00)
changed: [node_00] => (item=node_01)
changed: [node_01] => (item=node_01)

TASK [basic/sources : Setup proxy for package manager] *******************************************************************************************************
Wednesday 12 December 2018  03:28:49 +0200 (0:00:01.315)       0:00:07.649 **** 
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/basic/sources/tasks/proxy/yum.yml for node_00, node_01

TASK [basic/sources : Setup proxy for yum] *******************************************************************************************************************
Wednesday 12 December 2018  03:28:49 +0200 (0:00:00.108)       0:00:07.758 **** 
skipping: [node_00]
skipping: [node_01]

TASK [basic/sources : Disable proxy for yum] *****************************************************************************************************************
Wednesday 12 December 2018  03:28:49 +0200 (0:00:00.073)       0:00:07.832 **** 
changed: [node_01]
changed: [node_00]

TASK [basic/sources : Resolve vars] **************************************************************************************************************************
Wednesday 12 December 2018  03:28:49 +0200 (0:00:00.742)       0:00:08.575 **** 
ok: [node_00] => (item=/home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/basic/sources/vars/os_aware/CentOS.yml)
ok: [node_01] => (item=/home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/basic/sources/vars/os_aware/CentOS.yml)

TASK [basic/sources : Update repo] ***************************************************************************************************************************
Wednesday 12 December 2018  03:28:50 +0200 (0:00:00.121)       0:00:08.696 **** 
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/basic/sources/tasks/os_aware/CentOS.yml for node_00, node_01

TASK [basic/sources : (CentOS) Check CentOS-Base.repo.backup] ************************************************************************************************
Wednesday 12 December 2018  03:28:50 +0200 (0:00:00.120)       0:00:08.816 **** 
ok: [node_00]
ok: [node_01]

TASK [basic/sources : (CentOS) Backup CentOS-Base.repo] ******************************************************************************************************
Wednesday 12 December 2018  03:28:50 +0200 (0:00:00.715)       0:00:09.532 **** 
changed: [node_00]
changed: [node_01]

TASK [basic/sources : Pick Mirror config] ********************************************************************************************************************
Wednesday 12 December 2018  03:28:51 +0200 (0:00:00.672)       0:00:10.204 **** 
ok: [node_00] => (item=/home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/basic/sources/templates/mirrors/CentOS-7.repo.aliyun)
ok: [node_01] => (item=/home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/basic/sources/templates/mirrors/CentOS-7.repo.aliyun)

TASK [basic/sources : (CentOS) Use new CentOS-Base.repo] *****************************************************************************************************
Wednesday 12 December 2018  03:28:51 +0200 (0:00:00.122)       0:00:10.327 **** 
changed: [node_00]
changed: [node_01]

TASK [basic/sources : (CentOS) Update repo cache] ************************************************************************************************************
Wednesday 12 December 2018  03:28:52 +0200 (0:00:01.180)       0:00:11.508 **** 
ok: [node_01]
ok: [node_00]

TASK [basic/sources : (CentOS) Install the dependence packages] **********************************************************************************************
Wednesday 12 December 2018  03:28:54 +0200 (0:00:01.199)       0:00:12.708 **** 

TASK [jdk : Fetch JAVA_HOME, setup if absent] ****************************************************************************************************************
Wednesday 12 December 2018  03:28:54 +0200 (0:00:00.077)       0:00:12.786 **** 
ok: [node_01]
ok: [node_00]

TASK [jdk : Fetch java version] ******************************************************************************************************************************
Wednesday 12 December 2018  03:28:54 +0200 (0:00:00.794)       0:00:13.580 **** 
ok: [node_00]
ok: [node_01]

TASK [jdk : debug] *******************************************************************************************************************************************
Wednesday 12 December 2018  03:28:55 +0200 (0:00:00.635)       0:00:14.215 **** 
ok: [node_00] => {
    "msg": "os:RedHat , distribution:CentOS-7.5.1804(Core) , JAVA_HOME: , Java version:/bin/sh: java: command not found\n"
}
ok: [node_01] => {
    "msg": "os:RedHat , distribution:CentOS-7.5.1804(Core) , JAVA_HOME: , Java version:/bin/sh: java: command not found\n"
}

TASK [jdk : Install from repo] *******************************************************************************************************************************
Wednesday 12 December 2018  03:28:55 +0200 (0:00:00.109)       0:00:14.325 **** 
skipping: [node_00]
skipping: [node_01]

TASK [jdk : Install from tar] ********************************************************************************************************************************
Wednesday 12 December 2018  03:28:55 +0200 (0:00:00.083)       0:00:14.408 **** 
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/jdk/tasks/install_from_tar.yml for node_00, node_01

TASK [jdk : Concat jdk version string] ***********************************************************************************************************************
Wednesday 12 December 2018  03:28:55 +0200 (0:00:00.120)       0:00:14.529 **** 
ok: [node_00]
ok: [node_01]

TASK [jdk : Present install path '[/usr/lib/jdk]'] ***********************************************************************************************************
Wednesday 12 December 2018  03:28:56 +0200 (0:00:00.121)       0:00:14.650 **** 
changed: [node_01]
changed: [node_00]

TASK [jdk : Download jdk-8u192-linux-x64.tar.gz] *************************************************************************************************************
Wednesday 12 December 2018  03:28:56 +0200 (0:00:00.776)       0:00:15.427 **** 
changed: [node_01]
changed: [node_00]

TASK [jdk : Unarchive package] *******************************************************************************************************************************
Wednesday 12 December 2018  03:29:19 +0200 (0:00:23.083)       0:00:38.511 **** 
changed: [node_01]
changed: [node_00]

TASK [jdk : Export JAVA_HOME] ********************************************************************************************************************************
Wednesday 12 December 2018  03:29:43 +0200 (0:00:23.325)       0:01:01.837 **** 
changed: [node_01]
changed: [node_00]

TASK [jdk : Check java installation] *************************************************************************************************************************
Wednesday 12 December 2018  03:29:47 +0200 (0:00:04.059)       0:01:05.897 **** 
[DEPRECATION WARNING]: Using tests as filters is deprecated. Instead of using `result|failed` instead use `result is failed`. This feature will be removed in
 version 2.9. Deprecation warnings can be disabled by setting deprecation_warnings=False in ansible.cfg.
ok: [node_01]
[DEPRECATION WARNING]: Using tests as filters is deprecated. Instead of using `result|failed` instead use `result is failed`. This feature will be removed in
 version 2.9. Deprecation warnings can be disabled by setting deprecation_warnings=False in ansible.cfg.
ok: [node_00]

TASK [hadoop : Prepare variable] *****************************************************************************************************************************
Wednesday 12 December 2018  03:29:48 +0200 (0:00:01.053)       0:01:06.950 **** 
ok: [node_00]
ok: [node_01]

TASK [hadoop : Print variable] *******************************************************************************************************************************
Wednesday 12 December 2018  03:29:48 +0200 (0:00:00.113)       0:01:07.064 **** 
ok: [node_00] => {
    "pkg_setting": {
        "file": "hadoop-2.8.2.tar.gz", 
        "hadoop_home": "/usr/lib/hadoop", 
        "hadoop_path": "/usr/lib/hadoop-2.8.2", 
        "install_path": "/usr/lib", 
        "name": "hadoop", 
        "tmp_path": "/tmp/hadoop-2.8.2", 
        "url": "http://archive.apache.org/dist/hadoop/common/hadoop-2.8.2/hadoop-2.8.2.tar.gz", 
        "version": "2.8.2"
    }
}
ok: [node_01] => {
    "pkg_setting": {
        "file": "hadoop-2.8.2.tar.gz", 
        "hadoop_home": "/usr/lib/hadoop", 
        "hadoop_path": "/usr/lib/hadoop-2.8.2", 
        "install_path": "/usr/lib", 
        "name": "hadoop", 
        "tmp_path": "/tmp/hadoop-2.8.2", 
        "url": "http://archive.apache.org/dist/hadoop/common/hadoop-2.8.2/hadoop-2.8.2.tar.gz", 
        "version": "2.8.2"
    }
}

TASK [hadoop : Print hadoop_deploy_mode] *********************************************************************************************************************
Wednesday 12 December 2018  03:29:48 +0200 (0:00:00.102)       0:01:07.166 **** 
ok: [node_00] => {
    "hadoop_deploy_mode": "cluster"
}
ok: [node_01] => {
    "hadoop_deploy_mode": "cluster"
}

TASK [hadoop : Group Hadoop nodes (Step 1)] ******************************************************************************************************************
Wednesday 12 December 2018  03:29:48 +0200 (0:00:00.158)       0:01:07.325 **** 
ok: [node_00]
ok: [node_01]

TASK [hadoop : Group Hadoop nodes (Step 2)] ******************************************************************************************************************
Wednesday 12 December 2018  03:29:48 +0200 (0:00:00.222)       0:01:07.547 **** 
ok: [node_00]
ok: [node_01]

TASK [hadoop : Group Hadoop nodes (Step 3)] ******************************************************************************************************************
Wednesday 12 December 2018  03:29:49 +0200 (0:00:00.116)       0:01:07.664 **** 
ok: [node_00]
ok: [node_01]

TASK [hadoop : Group Hadoop nodes (Step 4)] ******************************************************************************************************************
Wednesday 12 December 2018  03:29:49 +0200 (0:00:00.111)       0:01:07.775 **** 
ok: [node_00]
ok: [node_01]

TASK [hadoop : Group Hadoop nodes (Step 5)] ******************************************************************************************************************
Wednesday 12 December 2018  03:29:49 +0200 (0:00:00.169)       0:01:07.945 **** 
skipping: [node_00]
skipping: [node_01]

TASK [hadoop : Group Hadoop nodes (Step 5)] ******************************************************************************************************************
Wednesday 12 December 2018  03:29:49 +0200 (0:00:00.085)       0:01:08.030 **** 
skipping: [node_00]
skipping: [node_01]

TASK [hadoop : Print hadoop_group_up] ************************************************************************************************************************
Wednesday 12 December 2018  03:29:49 +0200 (0:00:00.074)       0:01:08.105 **** 
ok: [node_00] => {
    "hadoop_group_up": {
        "all": [
            "node_00", 
            "node_01"
        ], 
        "cluster": [
            "node_00", 
            "node_01"
        ], 
        "cluster_client": [
            "node_01"
        ], 
        "single": [], 
        "single_client": []
    }
}
ok: [node_01] => {
    "hadoop_group_up": {
        "all": [
            "node_00", 
            "node_01"
        ], 
        "cluster": [
            "node_00", 
            "node_01"
        ], 
        "cluster_client": [
            "node_01"
        ], 
        "single": [], 
        "single_client": []
    }
}

TASK [hadoop : List Hadoop Cluster nodes (cluster mode)] *****************************************************************************************************
Wednesday 12 December 2018  03:29:49 +0200 (0:00:00.110)       0:01:08.216 **** 
ok: [node_00]
ok: [node_01]

TASK [hadoop : List Hadoop nodes (single mode)] **************************************************************************************************************
Wednesday 12 December 2018  03:29:50 +0200 (0:00:00.427)       0:01:08.643 **** 
skipping: [node_00]
skipping: [node_01]

TASK [hadoop : List Hadoop nodes (single client mode)] *******************************************************************************************************
Wednesday 12 December 2018  03:29:50 +0200 (0:00:00.077)       0:01:08.720 **** 
skipping: [node_00]
skipping: [node_01]

TASK [hadoop : Get Namenode and Resource Manager] ************************************************************************************************************
Wednesday 12 December 2018  03:29:50 +0200 (0:00:00.076)       0:01:08.797 **** 
ok: [node_00]
ok: [node_01]

TASK [hadoop : Set OS dependened vars] ***********************************************************************************************************************
Wednesday 12 December 2018  03:29:50 +0200 (0:00:00.205)       0:01:09.002 **** 
ok: [node_00] => (item=/home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/hadoop/vars/os/RedHat.yml)
ok: [node_01] => (item=/home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/hadoop/vars/os/RedHat.yml)

TASK [hadoop : Install dependence packages] ******************************************************************************************************************
Wednesday 12 December 2018  03:29:50 +0200 (0:00:00.240)       0:01:09.243 **** 
ok: [node_00] => (item=openssh-server)
ok: [node_01] => (item=openssh-server)
ok: [node_00] => (item=openssh-clients)
ok: [node_01] => (item=openssh-clients)
ok: [node_00] => (item=rsync)
ok: [node_01] => (item=rsync)
ok: [node_00] => (item=python)
ok: [node_01] => (item=python)

TASK [hadoop : include_tasks] ********************************************************************************************************************************
Wednesday 12 December 2018  03:29:57 +0200 (0:00:07.162)       0:01:16.405 **** 
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/hadoop/tasks/config_firewall.yml for node_00, node_01

TASK [hadoop : Stop firewall] ********************************************************************************************************************************
Wednesday 12 December 2018  03:29:58 +0200 (0:00:00.196)       0:01:16.601 **** 
ok: [node_00]
ok: [node_01]

TASK [hadoop : include_tasks] ********************************************************************************************************************************
Wednesday 12 December 2018  03:29:59 +0200 (0:00:01.301)       0:01:17.903 **** 
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/hadoop/tasks/cleanup.yml for node_00, node_01

TASK [hadoop : (Cleanup) Kill java] **************************************************************************************************************************
Wednesday 12 December 2018  03:29:59 +0200 (0:00:00.170)       0:01:18.074 **** 
changed: [node_01]
changed: [node_00]

TASK [hadoop : (Cleanup) Delete hadoop installation] *********************************************************************************************************
Wednesday 12 December 2018  03:30:00 +0200 (0:00:00.835)       0:01:18.910 **** 
skipping: [node_00] => (item=/usr/lib/hadoop-2.8.2) 
skipping: [node_00] => (item=/usr/lib/hadoop) 
skipping: [node_01] => (item=/usr/lib/hadoop-2.8.2) 
skipping: [node_01] => (item=/usr/lib/hadoop) 

TASK [hadoop : (Cleanup) Delete Hadoop configuration - /etc/hadoop] ******************************************************************************************
Wednesday 12 December 2018  03:30:00 +0200 (0:00:00.088)       0:01:18.998 **** 
skipping: [node_00]
skipping: [node_01]

TASK [hadoop : (Cleanup) Delete Hadoop Data & Log] ***********************************************************************************************************
Wednesday 12 December 2018  03:30:00 +0200 (0:00:00.076)       0:01:19.074 **** 
ok: [node_01] => (item=/home/hdfs/name)
ok: [node_00] => (item=/home/hdfs/name)
ok: [node_00] => (item=/home/hdfs/data)
ok: [node_01] => (item=/home/hdfs/data)
ok: [node_01] => (item=/var/hadoop/hadoop/logs)
ok: [node_00] => (item=/var/hadoop/hadoop/logs)
ok: [node_01] => (item=/var/hadoop/yarn/logs)
ok: [node_00] => (item=/var/hadoop/yarn/logs)
ok: [node_01] => (item=/var/hadoop/mapred/logs)
ok: [node_00] => (item=/var/hadoop/mapred/logs)

TASK [hadoop : include_tasks] ********************************************************************************************************************************
Wednesday 12 December 2018  03:30:03 +0200 (0:00:02.844)       0:01:21.919 **** 
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/hadoop/tasks/extract_hadoop.yml for node_00, node_01

TASK [hadoop : Download hadoop-2.8.2.tar.gz] *****************************************************************************************************************
Wednesday 12 December 2018  03:30:03 +0200 (0:00:00.155)       0:01:22.074 **** 
changed: [node_01]
changed: [node_00]

TASK [hadoop : Present Hadoop installation path - /usr/lib] **************************************************************************************************
Wednesday 12 December 2018  03:30:33 +0200 (0:00:30.407)       0:01:52.482 **** 
ok: [node_01]
ok: [node_00]

TASK [hadoop : Unarchive package - /usr/lib] *****************************************************************************************************************
Wednesday 12 December 2018  03:30:34 +0200 (0:00:00.657)       0:01:53.140 **** 
changed: [node_00]
changed: [node_01]

TASK [hadoop : Create link] **********************************************************************************************************************************
Wednesday 12 December 2018  03:31:36 +0200 (0:01:02.199)       0:02:55.339 **** 
changed: [node_00]
changed: [node_01]

TASK [hadoop : Export HADOOP_HOME, HADOOP_PREFIX ...] ********************************************************************************************************
Wednesday 12 December 2018  03:31:40 +0200 (0:00:03.567)       0:02:58.907 **** 
changed: [node_01]
changed: [node_00]

TASK [hadoop : include_tasks] ********************************************************************************************************************************
Wednesday 12 December 2018  03:31:40 +0200 (0:00:00.673)       0:02:59.580 **** 
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/hadoop/tasks/config_context_users.yml for node_00, node_01

TASK [hadoop : Gather Hadoop Users] **************************************************************************************************************************
Wednesday 12 December 2018  03:31:41 +0200 (0:00:00.209)       0:02:59.790 **** 
ok: [node_00]
ok: [node_01]

TASK [hadoop : Present Hadoop Group] *************************************************************************************************************************
Wednesday 12 December 2018  03:31:41 +0200 (0:00:00.111)       0:02:59.901 **** 
changed: [node_00]
changed: [node_01]

TASK [hadoop : Present Hadoop Users, "hadoop,hdfs,yarn,mapred,spark,demo_runner"] ****************************************************************************
Wednesday 12 December 2018  03:31:43 +0200 (0:00:02.611)       0:03:02.513 **** 
changed: [node_01] => (item=hadoop)
changed: [node_00] => (item=hadoop)
changed: [node_01] => (item=hdfs)
changed: [node_00] => (item=hdfs)
changed: [node_00] => (item=yarn)
changed: [node_01] => (item=yarn)
changed: [node_00] => (item=mapred)
changed: [node_01] => (item=mapred)
changed: [node_00] => (item=spark)
changed: [node_01] => (item=spark)
changed: [node_00] => (item=demo_runner)
changed: [node_01] => (item=demo_runner)

TASK [hadoop : Config hdfs users] ****************************************************************************************************************************
Wednesday 12 December 2018  03:31:48 +0200 (0:00:04.555)       0:03:07.069 **** 
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/hadoop/tasks/config_context_user_trust.yml for node_00, node_01
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/hadoop/tasks/config_context_user_trust.yml for node_00, node_01

TASK [hadoop : (HDFS) Present ssh_key for "hadoop"] **********************************************************************************************************
Wednesday 12 December 2018  03:31:48 +0200 (0:00:00.187)       0:03:07.256 **** 
skipping: [node_01]
changed: [node_00]

TASK [hadoop : (HDFS) Trust "hadoop"] ************************************************************************************************************************
Wednesday 12 December 2018  03:31:49 +0200 (0:00:00.742)       0:03:07.999 **** 
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/hadoop/tasks/trust_a_host.yml for node_00, node_01

TASK [hadoop : (HDFS) Read users[hadoop]' pub key from [node_00]] ********************************************************************************************
Wednesday 12 December 2018  03:31:49 +0200 (0:00:00.164)       0:03:08.164 **** 
ok: [node_00 -> 192.168.102.100] => (item=hadoop)
ok: [node_01 -> 192.168.102.100] => (item=hadoop)

TASK [hadoop : (HDFS) Trust users[hadoop] from [node_00] to [node_00,node_01]] *******************************************************************************
Wednesday 12 December 2018  03:31:50 +0200 (0:00:01.044)       0:03:09.208 **** 
changed: [node_01] => (item=hadoop)
changed: [node_00] => (item=hadoop)

TASK [hadoop : (HDFS) Present ssh_key for "hdfs"] ************************************************************************************************************
Wednesday 12 December 2018  03:31:51 +0200 (0:00:01.282)       0:03:10.491 **** 
skipping: [node_01]
changed: [node_00]

TASK [hadoop : (HDFS) Trust "hdfs"] **************************************************************************************************************************
Wednesday 12 December 2018  03:31:52 +0200 (0:00:00.722)       0:03:11.214 **** 
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/hadoop/tasks/trust_a_host.yml for node_00, node_01

TASK [hadoop : (HDFS) Read users[hdfs]' pub key from [node_00]] **********************************************************************************************
Wednesday 12 December 2018  03:31:52 +0200 (0:00:00.145)       0:03:11.359 **** 
ok: [node_00 -> 192.168.102.100] => (item=hdfs)
ok: [node_01 -> 192.168.102.100] => (item=hdfs)

TASK [hadoop : (HDFS) Trust users[hdfs] from [node_00] to [node_00,node_01]] *********************************************************************************
Wednesday 12 December 2018  03:31:53 +0200 (0:00:00.934)       0:03:12.294 **** 
changed: [node_00] => (item=hdfs)
changed: [node_01] => (item=hdfs)

TASK [hadoop : Config yarn users] ****************************************************************************************************************************
Wednesday 12 December 2018  03:31:54 +0200 (0:00:00.773)       0:03:13.067 **** 
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/hadoop/tasks/config_context_user_trust.yml for node_00, node_01
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/hadoop/tasks/config_context_user_trust.yml for node_00, node_01

TASK [hadoop : (YARN) Present ssh_key for "hadoop"] **********************************************************************************************************
Wednesday 12 December 2018  03:31:54 +0200 (0:00:00.222)       0:03:13.290 **** 
skipping: [node_01]
ok: [node_00]

TASK [hadoop : (YARN) Trust "hadoop"] ************************************************************************************************************************
Wednesday 12 December 2018  03:31:55 +0200 (0:00:00.630)       0:03:13.920 **** 
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/hadoop/tasks/trust_a_host.yml for node_00, node_01

TASK [hadoop : (YARN) Read users[hadoop]' pub key from [node_00]] ********************************************************************************************
Wednesday 12 December 2018  03:31:55 +0200 (0:00:00.148)       0:03:14.068 **** 
ok: [node_00 -> 192.168.102.100] => (item=hadoop)
ok: [node_01 -> 192.168.102.100] => (item=hadoop)

TASK [hadoop : (YARN) Trust users[hadoop] from [node_00] to [node_00,node_01]] *******************************************************************************
Wednesday 12 December 2018  03:31:56 +0200 (0:00:00.930)       0:03:14.998 **** 
ok: [node_00] => (item=hadoop)
ok: [node_01] => (item=hadoop)

TASK [hadoop : (YARN) Present ssh_key for "yarn"] ************************************************************************************************************
Wednesday 12 December 2018  03:31:57 +0200 (0:00:00.710)       0:03:15.709 **** 
skipping: [node_01]
changed: [node_00]

TASK [hadoop : (YARN) Trust "yarn"] **************************************************************************************************************************
Wednesday 12 December 2018  03:31:57 +0200 (0:00:00.742)       0:03:16.451 **** 
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/hadoop/tasks/trust_a_host.yml for node_00, node_01

TASK [hadoop : (YARN) Read users[yarn]' pub key from [node_00]] **********************************************************************************************
Wednesday 12 December 2018  03:31:58 +0200 (0:00:00.148)       0:03:16.599 **** 
ok: [node_00 -> 192.168.102.100] => (item=yarn)
ok: [node_01 -> 192.168.102.100] => (item=yarn)

TASK [hadoop : (YARN) Trust users[yarn] from [node_00] to [node_00,node_01]] *********************************************************************************
Wednesday 12 December 2018  03:31:58 +0200 (0:00:00.945)       0:03:17.545 **** 
changed: [node_00] => (item=yarn)
changed: [node_01] => (item=yarn)

TASK [hadoop : Config mapred users] **************************************************************************************************************************
Wednesday 12 December 2018  03:31:59 +0200 (0:00:00.735)       0:03:18.281 **** 
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/hadoop/tasks/config_context_user_trust.yml for node_00, node_01
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/hadoop/tasks/config_context_user_trust.yml for node_00, node_01

TASK [hadoop : (MAPRED) Present ssh_key for "hadoop"] ********************************************************************************************************
Wednesday 12 December 2018  03:31:59 +0200 (0:00:00.187)       0:03:18.468 **** 
skipping: [node_01]
ok: [node_00]

TASK [hadoop : (MAPRED) Trust "hadoop"] **********************************************************************************************************************
Wednesday 12 December 2018  03:32:00 +0200 (0:00:00.628)       0:03:19.096 **** 
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/hadoop/tasks/trust_a_host.yml for node_00, node_01

TASK [hadoop : (MAPRED) Read users[hadoop]' pub key from [node_00]] ******************************************************************************************
Wednesday 12 December 2018  03:32:00 +0200 (0:00:00.154)       0:03:19.251 **** 
ok: [node_00 -> 192.168.102.100] => (item=hadoop)
ok: [node_01 -> 192.168.102.100] => (item=hadoop)

TASK [hadoop : (MAPRED) Trust users[hadoop] from [node_00] to [[,]]] *****************************************************************************************
Wednesday 12 December 2018  03:32:01 +0200 (0:00:00.938)       0:03:20.190 **** 
skipping: [node_00] => (item=hadoop) 
skipping: [node_01] => (item=hadoop) 

TASK [hadoop : (MAPRED) Present ssh_key for "mapred"] ********************************************************************************************************
Wednesday 12 December 2018  03:32:01 +0200 (0:00:00.087)       0:03:20.277 **** 
skipping: [node_01]
changed: [node_00]

TASK [hadoop : (MAPRED) Trust "mapred"] **********************************************************************************************************************
Wednesday 12 December 2018  03:32:02 +0200 (0:00:00.739)       0:03:21.016 **** 
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/hadoop/tasks/trust_a_host.yml for node_00, node_01

TASK [hadoop : (MAPRED) Read users[mapred]' pub key from [node_00]] ******************************************************************************************
Wednesday 12 December 2018  03:32:02 +0200 (0:00:00.146)       0:03:21.162 **** 
ok: [node_00 -> 192.168.102.100] => (item=mapred)
ok: [node_01 -> 192.168.102.100] => (item=mapred)

TASK [hadoop : (MAPRED) Trust users[mapred] from [node_00] to [[,]]] *****************************************************************************************
Wednesday 12 December 2018  03:32:03 +0200 (0:00:01.014)       0:03:22.177 **** 
skipping: [node_00] => (item=mapred) 
skipping: [node_01] => (item=mapred) 

TASK [hadoop : include_tasks] ********************************************************************************************************************************
Wednesday 12 December 2018  03:32:03 +0200 (0:00:00.082)       0:03:22.259 **** 
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/hadoop/tasks/config_context_hosts.yml for node_00, node_01

TASK [hadoop : Avoid Strict host key checking] ***************************************************************************************************************
Wednesday 12 December 2018  03:32:03 +0200 (0:00:00.245)       0:03:22.505 **** 
skipping: [node_00]
skipping: [node_01]

TASK [hadoop : Ssh-keyscan : localhost] **********************************************************************************************************************
Wednesday 12 December 2018  03:32:03 +0200 (0:00:00.078)       0:03:22.583 **** 
ok: [node_00] => (item=0.0.0.0)
ok: [node_01] => (item=0.0.0.0)
ok: [node_00] => (item=localhost)
ok: [node_01] => (item=localhost)

TASK [hadoop : Update known_hosts : add localhost] ***********************************************************************************************************
Wednesday 12 December 2018  03:32:05 +0200 (0:00:01.894)       0:03:24.477 **** 
changed: [node_01] => (item=hadoop@0.0.0.0)
changed: [node_00] => (item=hadoop@0.0.0.0)
changed: [node_01] => (item=hadoop@localhost)
changed: [node_00] => (item=hadoop@localhost)

TASK [hadoop : Ssh-keyscan : hostnames] **********************************************************************************************************************
Wednesday 12 December 2018  03:32:07 +0200 (0:00:01.236)       0:03:25.714 **** 
ok: [node_00] => (item=node_00 scans cluster-node-00)
ok: [node_01] => (item=node_01 scans cluster-node-00)
ok: [node_00] => (item=node_00 scans cluster-node-01)
ok: [node_01] => (item=node_01 scans cluster-node-01)

TASK [hadoop : Update known_hosts : add hostnames] ***********************************************************************************************************
Wednesday 12 December 2018  03:32:08 +0200 (0:00:01.505)       0:03:27.220 **** 
changed: [node_00] => (item=hadoop@node_00)
changed: [node_01] => (item=hadoop@node_00)
changed: [node_00] => (item=hadoop@node_01)
changed: [node_01] => (item=hadoop@node_01)

TASK [hadoop : Copy known_hosts, from hadoop to hdfs, yarn, mapred] ******************************************************************************************
Wednesday 12 December 2018  03:32:09 +0200 (0:00:01.280)       0:03:28.501 **** 
ok: [node_00] => (item=hdfs@node_00)
ok: [node_01] => (item=hdfs@node_01)
ok: [node_00] => (item=yarn@node_00)
ok: [node_01] => (item=yarn@node_01)
ok: [node_00] => (item=mapred@node_00)
ok: [node_01] => (item=mapred@node_01)

TASK [hadoop : include_tasks] ********************************************************************************************************************************
Wednesday 12 December 2018  03:32:11 +0200 (0:00:01.780)       0:03:30.281 **** 
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/hadoop/tasks/config_hadoop_common.yml for node_00, node_01

TASK [hadoop : Present LOG Directorys (HADOOP, YARN, MAPRED)] ************************************************************************************************
Wednesday 12 December 2018  03:32:11 +0200 (0:00:00.189)       0:03:30.471 **** 
changed: [node_00] => (item={u'owner': u'hdfs', u'path': u'/var/hadoop/hadoop/logs'})
changed: [node_01] => (item={u'owner': u'hdfs', u'path': u'/var/hadoop/hadoop/logs'})
changed: [node_00] => (item={u'owner': u'yarn', u'path': u'/var/hadoop/yarn/logs'})
changed: [node_01] => (item={u'owner': u'yarn', u'path': u'/var/hadoop/yarn/logs'})
changed: [node_00] => (item={u'owner': u'mapred', u'path': u'/var/hadoop/mapred/logs'})
changed: [node_01] => (item={u'owner': u'mapred', u'path': u'/var/hadoop/mapred/logs'})

TASK [hadoop : export HADOOP_LOG_DIR ...] ********************************************************************************************************************
Wednesday 12 December 2018  03:32:13 +0200 (0:00:01.768)       0:03:32.240 **** 
changed: [node_00]
changed: [node_01]

TASK [hadoop : Present hadoop_conf_dir - /etc/hadoop] ********************************************************************************************************
Wednesday 12 December 2018  03:32:14 +0200 (0:00:00.603)       0:03:32.843 **** 
changed: [node_00]
changed: [node_01]

TASK [hadoop : Raw Copy] *************************************************************************************************************************************
Wednesday 12 December 2018  03:32:14 +0200 (0:00:00.688)       0:03:33.531 **** 
 [WARNING]: Consider using the file module with state=absent rather than running rm.  If you need to use command because file is insufficient you can add
warn=False to this command task or set command_warnings=False in ansible.cfg to get rid of this message.

changed: [node_00]
changed: [node_01]

TASK [hadoop : Copy template file] ***************************************************************************************************************************
Wednesday 12 December 2018  03:32:15 +0200 (0:00:00.785)       0:03:34.317 **** 
changed: [node_01] => (item=mapred-queues.xml)
changed: [node_00] => (item=mapred-queues.xml)
changed: [node_01] => (item=mapred-site.xml)
changed: [node_00] => (item=mapred-site.xml)

TASK [hadoop : Export HADOOP_CONF_DIR ...] *******************************************************************************************************************
Wednesday 12 December 2018  03:32:16 +0200 (0:00:01.165)       0:03:35.483 **** 
changed: [node_00]
changed: [node_01]

TASK [hadoop : fetch JAVA_HOME] ******************************************************************************************************************************
Wednesday 12 December 2018  03:32:17 +0200 (0:00:00.738)       0:03:36.221 **** 
ok: [node_00]
ok: [node_01]

TASK [hadoop : debug] ****************************************************************************************************************************************
Wednesday 12 December 2018  03:32:18 +0200 (0:00:00.721)       0:03:36.943 **** 
ok: [node_00] => {
    "msg": "JAVA_HOME=/usr/lib/jdk/jdk1.8.0_192"
}
ok: [node_01] => {
    "msg": "JAVA_HOME=/usr/lib/jdk/jdk1.8.0_192"
}

TASK [hadoop : set hadoop JAVA_HOME] *************************************************************************************************************************
Wednesday 12 December 2018  03:32:18 +0200 (0:00:00.110)       0:03:37.054 **** 
changed: [node_00]
changed: [node_01]

TASK [hadoop : Set HADOOP_LOG_DIR to hadoop-env.sh] **********************************************************************************************************
Wednesday 12 December 2018  03:32:19 +0200 (0:00:00.639)       0:03:37.693 **** 
changed: [node_00]
changed: [node_01]

TASK [hadoop : Set HADOOP_MAPRED_LOG_DIR to mapred-env.sh] ***************************************************************************************************
Wednesday 12 December 2018  03:32:19 +0200 (0:00:00.645)       0:03:38.339 **** 
changed: [node_00]
changed: [node_01]

TASK [hadoop : Set YARN_LOG_DIR to yarn-env.sh] **************************************************************************************************************
Wednesday 12 December 2018  03:32:20 +0200 (0:00:00.632)       0:03:38.971 **** 
changed: [node_00]
changed: [node_01]

TASK [hadoop : include_tasks] ********************************************************************************************************************************
Wednesday 12 December 2018  03:32:21 +0200 (0:00:00.634)       0:03:39.606 **** 
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/hadoop/tasks/config_hadoop_daemons.yml for node_00, node_01

TASK [hadoop : Copy conf_editor] *****************************************************************************************************************************
Wednesday 12 December 2018  03:32:21 +0200 (0:00:00.272)       0:03:39.878 **** 
changed: [node_01]
changed: [node_00]

TASK [hadoop : Present Config Directorys] ********************************************************************************************************************
Wednesday 12 December 2018  03:32:23 +0200 (0:00:02.159)       0:03:42.038 **** 
changed: [node_00]
changed: [node_01]

TASK [hadoop : Configure Single Node Daemons] ****************************************************************************************************************
Wednesday 12 December 2018  03:32:24 +0200 (0:00:00.634)       0:03:42.672 **** 
skipping: [node_00]
skipping: [node_01]

TASK [hadoop : Configure HDFS Daemon] ************************************************************************************************************************
Wednesday 12 December 2018  03:32:24 +0200 (0:00:00.080)       0:03:42.752 **** 
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/hadoop/tasks/daemon_conf/hdfs.yml for node_00, node_01

TASK [hadoop : Present Namenode Directorys] ******************************************************************************************************************
Wednesday 12 December 2018  03:32:24 +0200 (0:00:00.129)       0:03:42.882 **** 
skipping: [node_01]
changed: [node_00]

TASK [hadoop : Present Datanode Directorys] ******************************************************************************************************************
Wednesday 12 December 2018  03:32:24 +0200 (0:00:00.552)       0:03:43.435 **** 
changed: [node_00]
changed: [node_01]

TASK [hadoop : Update hdfs slaves] ***************************************************************************************************************************
Wednesday 12 December 2018  03:32:25 +0200 (0:00:00.657)       0:03:44.093 **** 
skipping: [node_01]
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/hadoop/tasks/daemon_conf/_update_slaves.yml for node_00

TASK [hadoop : configure slaves] *****************************************************************************************************************************
Wednesday 12 December 2018  03:32:25 +0200 (0:00:00.108)       0:03:44.201 **** 
changed: [node_00]

TASK [hadoop : Setup namenode hadoop] ************************************************************************************************************************
Wednesday 12 December 2018  03:32:27 +0200 (0:00:01.428)       0:03:45.630 **** 
skipping: [node_01]
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/hadoop/tasks/daemon_conf/_setup_hadoop_do.yml for node_00

TASK [hadoop : Copy Namenode confs] **************************************************************************************************************************
Wednesday 12 December 2018  03:32:27 +0200 (0:00:00.127)       0:03:45.757 **** 
changed: [node_00]

TASK [hadoop : Setup Namenode hadoop] ************************************************************************************************************************
Wednesday 12 December 2018  03:32:28 +0200 (0:00:01.329)       0:03:47.086 **** 
changed: [node_00]

TASK [hadoop : Setup datanode hadoop] ************************************************************************************************************************
Wednesday 12 December 2018  03:32:29 +0200 (0:00:00.910)       0:03:47.997 **** 
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/hadoop/tasks/daemon_conf/_setup_hadoop_do.yml for node_00, node_01

TASK [hadoop : Copy Datanode confs] **************************************************************************************************************************
Wednesday 12 December 2018  03:32:29 +0200 (0:00:00.131)       0:03:48.128 **** 
changed: [node_00]
changed: [node_01]

TASK [hadoop : Setup Datanode hadoop] ************************************************************************************************************************
Wednesday 12 December 2018  03:32:30 +0200 (0:00:01.343)       0:03:49.471 **** 
changed: [node_00]
changed: [node_01]

TASK [hadoop : Configure YARN Daemon] ************************************************************************************************************************
Wednesday 12 December 2018  03:32:31 +0200 (0:00:00.981)       0:03:50.453 **** 
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/hadoop/tasks/daemon_conf/yarn.yml for node_00, node_01

TASK [hadoop : update yarn slaves] ***************************************************************************************************************************
Wednesday 12 December 2018  03:32:32 +0200 (0:00:00.162)       0:03:50.616 **** 
skipping: [node_01]
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/hadoop/tasks/daemon_conf/_update_slaves.yml for node_00

TASK [hadoop : configure slaves] *****************************************************************************************************************************
Wednesday 12 December 2018  03:32:32 +0200 (0:00:00.105)       0:03:50.721 **** 
ok: [node_00]

TASK [hadoop : Setup Resourcemanager hadoop] *****************************************************************************************************************
Wednesday 12 December 2018  03:32:33 +0200 (0:00:01.162)       0:03:51.883 **** 
skipping: [node_01]
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/hadoop/tasks/daemon_conf/_setup_hadoop_do.yml for node_00

TASK [hadoop : Copy Resourcemanager confs] *******************************************************************************************************************
Wednesday 12 December 2018  03:32:33 +0200 (0:00:00.107)       0:03:51.990 **** 
changed: [node_00]

TASK [hadoop : Setup Resourcemanager hadoop] *****************************************************************************************************************
Wednesday 12 December 2018  03:32:34 +0200 (0:00:01.213)       0:03:53.204 **** 
changed: [node_00]

TASK [hadoop : Setup Nodemanager hadoop] *********************************************************************************************************************
Wednesday 12 December 2018  03:32:35 +0200 (0:00:00.692)       0:03:53.897 **** 
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/hadoop/tasks/daemon_conf/_setup_hadoop_do.yml for node_00, node_01

TASK [hadoop : Copy Nodemanager confs] ***********************************************************************************************************************
Wednesday 12 December 2018  03:32:35 +0200 (0:00:00.130)       0:03:54.027 **** 
changed: [node_00]
changed: [node_01]

TASK [hadoop : Setup Nodemanager hadoop] *********************************************************************************************************************
Wednesday 12 December 2018  03:32:36 +0200 (0:00:01.486)       0:03:55.513 **** 
changed: [node_00]
changed: [node_01]

TASK [hadoop : Configure MAPRED Daemon] **********************************************************************************************************************
Wednesday 12 December 2018  03:32:37 +0200 (0:00:00.834)       0:03:56.348 **** 
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/hadoop/tasks/daemon_conf/mapred.yml for node_00, node_01

TASK [hadoop : Setup Hadoop Client] **************************************************************************************************************************
Wednesday 12 December 2018  03:32:37 +0200 (0:00:00.157)       0:03:56.505 **** 
skipping: [node_00]
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/hadoop/tasks/daemon_conf/_setup_hadoop_do.yml for node_01

TASK [hadoop : Copy Mapred confs] ****************************************************************************************************************************
Wednesday 12 December 2018  03:32:38 +0200 (0:00:00.104)       0:03:56.610 **** 
changed: [node_01]

TASK [hadoop : Setup Mapred hadoop] **************************************************************************************************************************
Wednesday 12 December 2018  03:32:39 +0200 (0:00:01.332)       0:03:57.943 **** 
changed: [node_01]

TASK [hadoop : Configure Client] *****************************************************************************************************************************
Wednesday 12 December 2018  03:32:40 +0200 (0:00:00.755)       0:03:58.698 **** 
skipping: [node_00]
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/hadoop/tasks/daemon_conf/client.yml for node_01

TASK [hadoop : Setup Hadoop Client] **************************************************************************************************************************
Wednesday 12 December 2018  03:32:40 +0200 (0:00:00.147)       0:03:58.846 **** 
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/hadoop/tasks/daemon_conf/_setup_hadoop_do.yml for node_01

TASK [hadoop : Copy Client confs] ****************************************************************************************************************************
Wednesday 12 December 2018  03:32:40 +0200 (0:00:00.074)       0:03:58.920 **** 
ok: [node_01]

TASK [hadoop : Setup Client hadoop] **************************************************************************************************************************
Wednesday 12 December 2018  03:32:41 +0200 (0:00:01.244)       0:04:00.164 **** 
changed: [node_01]

TASK [hadoop : include_tasks] ********************************************************************************************************************************
Wednesday 12 December 2018  03:32:42 +0200 (0:00:00.756)       0:04:00.921 **** 
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/hadoop/tasks/run_daemons.yml for node_00, node_01

TASK [hadoop : prepare script directory] *********************************************************************************************************************
Wednesday 12 December 2018  03:32:42 +0200 (0:00:00.253)       0:04:01.174 **** 
changed: [node_00]
changed: [node_01]

TASK [hadoop : copy launch daemon script] ********************************************************************************************************************
Wednesday 12 December 2018  03:32:43 +0200 (0:00:00.689)       0:04:01.864 **** 
changed: [node_01]
changed: [node_00]

TASK [hadoop : check if namenode formatted] ******************************************************************************************************************
Wednesday 12 December 2018  03:32:48 +0200 (0:00:05.200)       0:04:07.065 **** 
skipping: [node_01]
ok: [node_00]

TASK [hadoop : debug] ****************************************************************************************************************************************
Wednesday 12 December 2018  03:32:49 +0200 (0:00:00.833)       0:04:07.898 **** 
skipping: [node_01]
ok: [node_00] => {
    "msg": "/home/hdfs/name/current/VERSION exist-{'failed': False, u'stat': {u'exists': False}, u'changed': False}"
}

TASK [hadoop : format namenode] ******************************************************************************************************************************
Wednesday 12 December 2018  03:32:49 +0200 (0:00:00.083)       0:04:07.981 **** 
skipping: [node_01]
changed: [node_00]

TASK [hadoop : start hdfs] ***********************************************************************************************************************************
Wednesday 12 December 2018  03:32:55 +0200 (0:00:06.131)       0:04:14.113 **** 
skipping: [node_01]
changed: [node_00]

TASK [hadoop : start yarn] ***********************************************************************************************************************************
Wednesday 12 December 2018  03:33:37 +0200 (0:00:42.346)       0:04:56.460 **** 
skipping: [node_01]
changed: [node_00]

TASK [hadoop : run mr history server] ************************************************************************************************************************
Wednesday 12 December 2018  03:33:44 +0200 (0:00:06.314)       0:05:02.774 **** 
skipping: [node_00]
changed: [node_01]

TASK [hadoop : include_tasks] ********************************************************************************************************************************
Wednesday 12 December 2018  03:33:47 +0200 (0:00:02.967)       0:05:05.742 **** 
skipping: [node_00]
included: /home/davar/LABS/ansible-hadoop-spark-playground-multi-node/roles/hadoop/tasks/run_demo.yml for node_01

TASK [hadoop : run mapred demo] ******************************************************************************************************************************
Wednesday 12 December 2018  03:33:47 +0200 (0:00:00.695)       0:05:06.437 **** 
fatal: [node_01]: FAILED! => {"changed": true, "msg": "non-zero return code", "rc": 1, "stderr": "Shared connection to 192.168.102.101 closed.\r\n", "stdout": "\r\n18/12/12 01:34:32 INFO client.RMProxy: Connecting to ResourceManager at cluster-node-00/192.168.102.100:8032\r\n18/12/12 01:34:34 INFO input.FileInputFormat: Total input files to process : 29\r\n18/12/12 01:34:35 INFO mapreduce.JobSubmitter: number of splits:29\r\n18/12/12 01:34:35 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1544578425790_0001\r\n18/12/12 01:34:36 INFO impl.YarnClientImpl: Submitted application application_1544578425790_0001\r\n18/12/12 01:34:37 INFO mapreduce.Job: The url to track the job: http://cluster-node-00:8088/proxy/application_1544578425790_0001/\r\n18/12/12 01:34:37 INFO mapreduce.Job: Running job: job_1544578425790_0001\r\n18/12/12 01:34:56 INFO mapreduce.Job: Job job_1544578425790_0001 running in uber mode : false\r\n18/12/12 01:34:56 INFO mapreduce.Job:  map 0% reduce 0%\r\n18/12/12 01:44:30 INFO mapreduce.Job:  map 32% reduce 0%\r\n18/12/12 01:44:40 INFO mapreduce.Job:  map 34% reduce 0%\r\n18/12/12 01:44:43 INFO mapreduce.Job:  map 36% reduce 0%\r\n18/12/12 01:44:45 INFO mapreduce.Job:  map 44% reduce 0%\r\n18/12/12 01:45:23 INFO mapreduce.Job:  map 48% reduce 0%\r\n18/12/12 01:53:40 INFO mapreduce.Job:  map 51% reduce 0%\r\n18/12/12 01:53:59 INFO mapreduce.Job:  map 68% reduce 0%\r\n18/12/12 01:54:10 INFO mapreduce.Job:  map 69% reduce 0%\r\n18/12/12 01:54:16 INFO mapreduce.Job:  map 76% reduce 0%\r\n18/12/12 01:54:22 INFO mapreduce.Job:  map 90% reduce 0%\r\n18/12/12 01:54:23 INFO mapreduce.Job:  map 93% reduce 0%\r\n18/12/12 01:54:46 INFO mapreduce.Job:  map 95% reduce 0%\r\n18/12/12 01:54:48 INFO mapreduce.Job:  map 97% reduce 0%\r\n18/12/12 01:56:00 INFO mapreduce.Job:  map 100% reduce 0%\r\n18/12/12 01:56:09 INFO mapreduce.Job:  map 100% reduce 100%\r\n18/12/12 01:56:17 INFO mapred.ClientServiceDelegate: Application state is completed. FinalApplicationStatus=SUCCEEDED. Redirecting to job history server\r\n18/12/12 01:56:26 INFO mapred.ClientServiceDelegate: Application state is completed. FinalApplicationStatus=SUCCEEDED. Redirecting to job history server\r\n18/12/12 01:56:26 INFO mapred.ClientServiceDelegate: Application state is completed. FinalApplicationStatus=SUCCEEDED. Redirecting to job history server\r\njava.io.IOException: java.io.IOException: Unknown Job job_1544578425790_0001\r\n\tat org.apache.hadoop.mapreduce.v2.hs.HistoryClientService$HSClientProtocolHandler.verifyAndGetJob(HistoryClientService.java:218)\r\n\tat org.apache.hadoop.mapreduce.v2.hs.HistoryClientService$HSClientProtocolHandler.getTaskAttemptCompletionEvents(HistoryClientService.java:281)\r\n\tat org.apache.hadoop.mapreduce.v2.api.impl.pb.service.MRClientProtocolPBServiceImpl.getTaskAttemptCompletionEvents(MRClientProtocolPBServiceImpl.java:173)\r\n\tat org.apache.hadoop.yarn.proto.MRClientProtocol$MRClientProtocolService$2.callBlockingMethod(MRClientProtocol.java:283)\r\n\tat org.apache.hadoop.ipc.ProtobufRpcEngine$Server$ProtoBufRpcInvoker.call(ProtobufRpcEngine.java:447)\r\n\tat org.apache.hadoop.ipc.RPC$Server.call(RPC.java:989)\r\n\tat org.apache.hadoop.ipc.Server$RpcCall.run(Server.java:847)\r\n\tat org.apache.hadoop.ipc.Server$RpcCall.run(Server.java:790)\r\n\tat java.security.AccessController.doPrivileged(Native Method)\r\n\tat javax.security.auth.Subject.doAs(Subject.java:422)\r\n\tat org.apache.hadoop.security.UserGroupInformation.doAs(UserGroupInformation.java:1836)\r\n\tat org.apache.hadoop.ipc.Server$Handler.run(Server.java:2486)\r\n\r\n\tat org.apache.hadoop.mapred.ClientServiceDelegate.invoke(ClientServiceDelegate.java:344)\r\n\tat org.apache.hadoop.mapred.ClientServiceDelegate.getTaskCompletionEvents(ClientServiceDelegate.java:396)\r\n\tat org.apache.hadoop.mapred.YARNRunner.getTaskCompletionEvents(YARNRunner.java:624)\r\n\tat org.apache.hadoop.mapreduce.Job$6.run(Job.java:724)\r\n\tat org.apache.hadoop.mapreduce.Job$6.run(Job.java:721)\r\n\tat java.security.AccessController.doPrivileged(Native Method)\r\n\tat javax.security.auth.Subject.doAs(Subject.java:422)\r\n\tat org.apache.hadoop.security.UserGroupInformation.doAs(UserGroupInformation.java:1836)\r\n\tat org.apache.hadoop.mapreduce.Job.getTaskCompletionEvents(Job.java:721)\r\n\tat org.apache.hadoop.mapreduce.Job.monitorAndPrintJob(Job.java:1422)\r\n\tat org.apache.hadoop.mapreduce.Job.waitForCompletion(Job.java:1362)\r\n\tat org.apache.hadoop.examples.Grep.run(Grep.java:78)\r\n\tat org.apache.hadoop.util.ToolRunner.run(ToolRunner.java:76)\r\n\tat org.apache.hadoop.examples.Grep.main(Grep.java:103)\r\n\tat sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)\r\n\tat sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)\r\n\tat sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)\r\n\tat java.lang.reflect.Method.invoke(Method.java:498)\r\n\tat org.apache.hadoop.util.ProgramDriver$ProgramDescription.invoke(ProgramDriver.java:71)\r\n\tat org.apache.hadoop.util.ProgramDriver.run(ProgramDriver.java:144)\r\n\tat org.apache.hadoop.examples.ExampleDriver.main(ExampleDriver.java:74)\r\n\tat sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)\r\n\tat sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)\r\n\tat sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)\r\n\tat java.lang.reflect.Method.invoke(Method.java:498)\r\n\tat org.apache.hadoop.util.RunJar.run(RunJar.java:234)\r\n\tat org.apache.hadoop.util.RunJar.main(RunJar.java:148)\r\nCaused by: java.io.IOException: Unknown Job job_1544578425790_0001\r\n\tat org.apache.hadoop.mapreduce.v2.hs.HistoryClientService$HSClientProtocolHandler.verifyAndGetJob(HistoryClientService.java:218)\r\n\tat org.apache.hadoop.mapreduce.v2.hs.HistoryClientService$HSClientProtocolHandler.getTaskAttemptCompletionEvents(HistoryClientService.java:281)\r\n\tat org.apache.hadoop.mapreduce.v2.api.impl.pb.service.MRClientProtocolPBServiceImpl.getTaskAttemptCompletionEvents(MRClientProtocolPBServiceImpl.java:173)\r\n\tat org.apache.hadoop.yarn.proto.MRClientProtocol$MRClientProtocolService$2.callBlockingMethod(MRClientProtocol.java:283)\r\n\tat org.apache.hadoop.ipc.ProtobufRpcEngine$Server$ProtoBufRpcInvoker.call(ProtobufRpcEngine.java:447)\r\n\tat org.apache.hadoop.ipc.RPC$Server.call(RPC.java:989)\r\n\tat org.apache.hadoop.ipc.Server$RpcCall.run(Server.java:847)\r\n\tat org.apache.hadoop.ipc.Server$RpcCall.run(Server.java:790)\r\n\tat java.security.AccessController.doPrivileged(Native Method)\r\n\tat javax.security.auth.Subject.doAs(Subject.java:422)\r\n\tat org.apache.hadoop.security.UserGroupInformation.doAs(UserGroupInformation.java:1836)\r\n\tat org.apache.hadoop.ipc.Server$Handler.run(Server.java:2486)\r\n\r\n\tat sun.reflect.NativeConstructorAccessorImpl.newInstance0(Native Method)\r\n\tat sun.reflect.NativeConstructorAccessorImpl.newInstance(NativeConstructorAccessorImpl.java:62)\r\n\tat sun.reflect.DelegatingConstructorAccessorImpl.newInstance(DelegatingConstructorAccessorImpl.java:45)\r\n\tat java.lang.reflect.Constructor.newInstance(Constructor.java:423)\r\n\tat org.apache.hadoop.ipc.RemoteException.instantiateException(RemoteException.java:121)\r\n\tat org.apache.hadoop.ipc.RemoteException.unwrapRemoteException(RemoteException.java:110)\r\n\tat org.apache.hadoop.mapreduce.v2.api.impl.pb.client.MRClientProtocolPBClientImpl.unwrapAndThrowException(MRClientProtocolPBClientImpl.java:291)\r\n\tat org.apache.hadoop.mapreduce.v2.api.impl.pb.client.MRClientProtocolPBClientImpl.getTaskAttemptCompletionEvents(MRClientProtocolPBClientImpl.java:179)\r\n\tat sun.reflect.GeneratedMethodAccessor4.invoke(Unknown Source)\r\n\tat sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)\r\n\tat java.lang.reflect.Method.invoke(Method.java:498)\r\n\tat org.apache.hadoop.mapred.ClientServiceDelegate.invoke(ClientServiceDelegate.java:325)\r\n\t... 26 more\r\nCaused by: org.apache.hadoop.ipc.RemoteException(java.io.IOException): Unknown Job job_1544578425790_0001\r\n\tat org.apache.hadoop.mapreduce.v2.hs.HistoryClientService$HSClientProtocolHandler.verifyAndGetJob(HistoryClientService.java:218)\r\n\tat org.apache.hadoop.mapreduce.v2.hs.HistoryClientService$HSClientProtocolHandler.getTaskAttemptCompletionEvents(HistoryClientService.java:281)\r\n\tat org.apache.hadoop.mapreduce.v2.api.impl.pb.service.MRClientProtocolPBServiceImpl.getTaskAttemptCompletionEvents(MRClientProtocolPBServiceImpl.java:173)\r\n\tat org.apache.hadoop.yarn.proto.MRClientProtocol$MRClientProtocolService$2.callBlockingMethod(MRClientProtocol.java:283)\r\n\tat org.apache.hadoop.ipc.ProtobufRpcEngine$Server$ProtoBufRpcInvoker.call(ProtobufRpcEngine.java:447)\r\n\tat org.apache.hadoop.ipc.RPC$Server.call(RPC.java:989)\r\n\tat org.apache.hadoop.ipc.Server$RpcCall.run(Server.java:847)\r\n\tat org.apache.hadoop.ipc.Server$RpcCall.run(Server.java:790)\r\n\tat java.security.AccessController.doPrivileged(Native Method)\r\n\tat javax.security.auth.Subject.doAs(Subject.java:422)\r\n\tat org.apache.hadoop.security.UserGroupInformation.doAs(UserGroupInformation.java:1836)\r\n\tat org.apache.hadoop.ipc.Server$Handler.run(Server.java:2486)\r\n\r\n\tat org.apache.hadoop.ipc.Client.getRpcResponse(Client.java:1483)\r\n\tat org.apache.hadoop.ipc.Client.call(Client.java:1429)\r\n\tat org.apache.hadoop.ipc.Client.call(Client.java:1339)\r\n\tat org.apache.hadoop.ipc.ProtobufRpcEngine$Invoker.invoke(ProtobufRpcEngine.java:227)\r\n\tat org.apache.hadoop.ipc.ProtobufRpcEngine$Invoker.invoke(ProtobufRpcEngine.java:116)\r\n\tat com.sun.proxy.$Proxy15.getTaskAttemptCompletionEvents(Unknown Source)\r\n\tat org.apache.hadoop.mapreduce.v2.api.impl.pb.client.MRClientProtocolPBClientImpl.getTaskAttemptCompletionEvents(MRClientProtocolPBClientImpl.java:177)\r\n\t... 30 more\r\ncat: `output/*': No such file or directory\r\n", "stdout_lines": ["", "18/12/12 01:34:32 INFO client.RMProxy: Connecting to ResourceManager at cluster-node-00/192.168.102.100:8032", "18/12/12 01:34:34 INFO input.FileInputFormat: Total input files to process : 29", "18/12/12 01:34:35 INFO mapreduce.JobSubmitter: number of splits:29", "18/12/12 01:34:35 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1544578425790_0001", "18/12/12 01:34:36 INFO impl.YarnClientImpl: Submitted application application_1544578425790_0001", "18/12/12 01:34:37 INFO mapreduce.Job: The url to track the job: http://cluster-node-00:8088/proxy/application_1544578425790_0001/", "18/12/12 01:34:37 INFO mapreduce.Job: Running job: job_1544578425790_0001", "18/12/12 01:34:56 INFO mapreduce.Job: Job job_1544578425790_0001 running in uber mode : false", "18/12/12 01:34:56 INFO mapreduce.Job:  map 0% reduce 0%", "18/12/12 01:44:30 INFO mapreduce.Job:  map 32% reduce 0%", "18/12/12 01:44:40 INFO mapreduce.Job:  map 34% reduce 0%", "18/12/12 01:44:43 INFO mapreduce.Job:  map 36% reduce 0%", "18/12/12 01:44:45 INFO mapreduce.Job:  map 44% reduce 0%", "18/12/12 01:45:23 INFO mapreduce.Job:  map 48% reduce 0%", "18/12/12 01:53:40 INFO mapreduce.Job:  map 51% reduce 0%", "18/12/12 01:53:59 INFO mapreduce.Job:  map 68% reduce 0%", "18/12/12 01:54:10 INFO mapreduce.Job:  map 69% reduce 0%", "18/12/12 01:54:16 INFO mapreduce.Job:  map 76% reduce 0%", "18/12/12 01:54:22 INFO mapreduce.Job:  map 90% reduce 0%", "18/12/12 01:54:23 INFO mapreduce.Job:  map 93% reduce 0%", "18/12/12 01:54:46 INFO mapreduce.Job:  map 95% reduce 0%", "18/12/12 01:54:48 INFO mapreduce.Job:  map 97% reduce 0%", "18/12/12 01:56:00 INFO mapreduce.Job:  map 100% reduce 0%", "18/12/12 01:56:09 INFO mapreduce.Job:  map 100% reduce 100%", "18/12/12 01:56:17 INFO mapred.ClientServiceDelegate: Application state is completed. FinalApplicationStatus=SUCCEEDED. Redirecting to job history server", "18/12/12 01:56:26 INFO mapred.ClientServiceDelegate: Application state is completed. FinalApplicationStatus=SUCCEEDED. Redirecting to job history server", "18/12/12 01:56:26 INFO mapred.ClientServiceDelegate: Application state is completed. FinalApplicationStatus=SUCCEEDED. Redirecting to job history server", "java.io.IOException: java.io.IOException: Unknown Job job_1544578425790_0001", "\tat org.apache.hadoop.mapreduce.v2.hs.HistoryClientService$HSClientProtocolHandler.verifyAndGetJob(HistoryClientService.java:218)", "\tat org.apache.hadoop.mapreduce.v2.hs.HistoryClientService$HSClientProtocolHandler.getTaskAttemptCompletionEvents(HistoryClientService.java:281)", "\tat org.apache.hadoop.mapreduce.v2.api.impl.pb.service.MRClientProtocolPBServiceImpl.getTaskAttemptCompletionEvents(MRClientProtocolPBServiceImpl.java:173)", "\tat org.apache.hadoop.yarn.proto.MRClientProtocol$MRClientProtocolService$2.callBlockingMethod(MRClientProtocol.java:283)", "\tat org.apache.hadoop.ipc.ProtobufRpcEngine$Server$ProtoBufRpcInvoker.call(ProtobufRpcEngine.java:447)", "\tat org.apache.hadoop.ipc.RPC$Server.call(RPC.java:989)", "\tat org.apache.hadoop.ipc.Server$RpcCall.run(Server.java:847)", "\tat org.apache.hadoop.ipc.Server$RpcCall.run(Server.java:790)", "\tat java.security.AccessController.doPrivileged(Native Method)", "\tat javax.security.auth.Subject.doAs(Subject.java:422)", "\tat org.apache.hadoop.security.UserGroupInformation.doAs(UserGroupInformation.java:1836)", "\tat org.apache.hadoop.ipc.Server$Handler.run(Server.java:2486)", "", "\tat org.apache.hadoop.mapred.ClientServiceDelegate.invoke(ClientServiceDelegate.java:344)", "\tat org.apache.hadoop.mapred.ClientServiceDelegate.getTaskCompletionEvents(ClientServiceDelegate.java:396)", "\tat org.apache.hadoop.mapred.YARNRunner.getTaskCompletionEvents(YARNRunner.java:624)", "\tat org.apache.hadoop.mapreduce.Job$6.run(Job.java:724)", "\tat org.apache.hadoop.mapreduce.Job$6.run(Job.java:721)", "\tat java.security.AccessController.doPrivileged(Native Method)", "\tat javax.security.auth.Subject.doAs(Subject.java:422)", "\tat org.apache.hadoop.security.UserGroupInformation.doAs(UserGroupInformation.java:1836)", "\tat org.apache.hadoop.mapreduce.Job.getTaskCompletionEvents(Job.java:721)", "\tat org.apache.hadoop.mapreduce.Job.monitorAndPrintJob(Job.java:1422)", "\tat org.apache.hadoop.mapreduce.Job.waitForCompletion(Job.java:1362)", "\tat org.apache.hadoop.examples.Grep.run(Grep.java:78)", "\tat org.apache.hadoop.util.ToolRunner.run(ToolRunner.java:76)", "\tat org.apache.hadoop.examples.Grep.main(Grep.java:103)", "\tat sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)", "\tat sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)", "\tat sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)", "\tat java.lang.reflect.Method.invoke(Method.java:498)", "\tat org.apache.hadoop.util.ProgramDriver$ProgramDescription.invoke(ProgramDriver.java:71)", "\tat org.apache.hadoop.util.ProgramDriver.run(ProgramDriver.java:144)", "\tat org.apache.hadoop.examples.ExampleDriver.main(ExampleDriver.java:74)", "\tat sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)", "\tat sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)", "\tat sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)", "\tat java.lang.reflect.Method.invoke(Method.java:498)", "\tat org.apache.hadoop.util.RunJar.run(RunJar.java:234)", "\tat org.apache.hadoop.util.RunJar.main(RunJar.java:148)", "Caused by: java.io.IOException: Unknown Job job_1544578425790_0001", "\tat org.apache.hadoop.mapreduce.v2.hs.HistoryClientService$HSClientProtocolHandler.verifyAndGetJob(HistoryClientService.java:218)", "\tat org.apache.hadoop.mapreduce.v2.hs.HistoryClientService$HSClientProtocolHandler.getTaskAttemptCompletionEvents(HistoryClientService.java:281)", "\tat org.apache.hadoop.mapreduce.v2.api.impl.pb.service.MRClientProtocolPBServiceImpl.getTaskAttemptCompletionEvents(MRClientProtocolPBServiceImpl.java:173)", "\tat org.apache.hadoop.yarn.proto.MRClientProtocol$MRClientProtocolService$2.callBlockingMethod(MRClientProtocol.java:283)", "\tat org.apache.hadoop.ipc.ProtobufRpcEngine$Server$ProtoBufRpcInvoker.call(ProtobufRpcEngine.java:447)", "\tat org.apache.hadoop.ipc.RPC$Server.call(RPC.java:989)", "\tat org.apache.hadoop.ipc.Server$RpcCall.run(Server.java:847)", "\tat org.apache.hadoop.ipc.Server$RpcCall.run(Server.java:790)", "\tat java.security.AccessController.doPrivileged(Native Method)", "\tat javax.security.auth.Subject.doAs(Subject.java:422)", "\tat org.apache.hadoop.security.UserGroupInformation.doAs(UserGroupInformation.java:1836)", "\tat org.apache.hadoop.ipc.Server$Handler.run(Server.java:2486)", "", "\tat sun.reflect.NativeConstructorAccessorImpl.newInstance0(Native Method)", "\tat sun.reflect.NativeConstructorAccessorImpl.newInstance(NativeConstructorAccessorImpl.java:62)", "\tat sun.reflect.DelegatingConstructorAccessorImpl.newInstance(DelegatingConstructorAccessorImpl.java:45)", "\tat java.lang.reflect.Constructor.newInstance(Constructor.java:423)", "\tat org.apache.hadoop.ipc.RemoteException.instantiateException(RemoteException.java:121)", "\tat org.apache.hadoop.ipc.RemoteException.unwrapRemoteException(RemoteException.java:110)", "\tat org.apache.hadoop.mapreduce.v2.api.impl.pb.client.MRClientProtocolPBClientImpl.unwrapAndThrowException(MRClientProtocolPBClientImpl.java:291)", "\tat org.apache.hadoop.mapreduce.v2.api.impl.pb.client.MRClientProtocolPBClientImpl.getTaskAttemptCompletionEvents(MRClientProtocolPBClientImpl.java:179)", "\tat sun.reflect.GeneratedMethodAccessor4.invoke(Unknown Source)", "\tat sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)", "\tat java.lang.reflect.Method.invoke(Method.java:498)", "\tat org.apache.hadoop.mapred.ClientServiceDelegate.invoke(ClientServiceDelegate.java:325)", "\t... 26 more", "Caused by: org.apache.hadoop.ipc.RemoteException(java.io.IOException): Unknown Job job_1544578425790_0001", "\tat org.apache.hadoop.mapreduce.v2.hs.HistoryClientService$HSClientProtocolHandler.verifyAndGetJob(HistoryClientService.java:218)", "\tat org.apache.hadoop.mapreduce.v2.hs.HistoryClientService$HSClientProtocolHandler.getTaskAttemptCompletionEvents(HistoryClientService.java:281)", "\tat org.apache.hadoop.mapreduce.v2.api.impl.pb.service.MRClientProtocolPBServiceImpl.getTaskAttemptCompletionEvents(MRClientProtocolPBServiceImpl.java:173)", "\tat org.apache.hadoop.yarn.proto.MRClientProtocol$MRClientProtocolService$2.callBlockingMethod(MRClientProtocol.java:283)", "\tat org.apache.hadoop.ipc.ProtobufRpcEngine$Server$ProtoBufRpcInvoker.call(ProtobufRpcEngine.java:447)", "\tat org.apache.hadoop.ipc.RPC$Server.call(RPC.java:989)", "\tat org.apache.hadoop.ipc.Server$RpcCall.run(Server.java:847)", "\tat org.apache.hadoop.ipc.Server$RpcCall.run(Server.java:790)", "\tat java.security.AccessController.doPrivileged(Native Method)", "\tat javax.security.auth.Subject.doAs(Subject.java:422)", "\tat org.apache.hadoop.security.UserGroupInformation.doAs(UserGroupInformation.java:1836)", "\tat org.apache.hadoop.ipc.Server$Handler.run(Server.java:2486)", "", "\tat org.apache.hadoop.ipc.Client.getRpcResponse(Client.java:1483)", "\tat org.apache.hadoop.ipc.Client.call(Client.java:1429)", "\tat org.apache.hadoop.ipc.Client.call(Client.java:1339)", "\tat org.apache.hadoop.ipc.ProtobufRpcEngine$Invoker.invoke(ProtobufRpcEngine.java:227)", "\tat org.apache.hadoop.ipc.ProtobufRpcEngine$Invoker.invoke(ProtobufRpcEngine.java:116)", "\tat com.sun.proxy.$Proxy15.getTaskAttemptCompletionEvents(Unknown Source)", "\tat org.apache.hadoop.mapreduce.v2.api.impl.pb.client.MRClientProtocolPBClientImpl.getTaskAttemptCompletionEvents(MRClientProtocolPBClientImpl.java:177)", "\t... 30 more", "cat: `output/*': No such file or directory"]}
...ignoring

PLAY RECAP ***************************************************************************************************************************************************
node_00                    : ok=133  changed=53   unreachable=0    failed=0   
node_01                    : ok=121  changed=45   unreachable=0    failed=0   

Wednesday 12 December 2018  03:56:38 +0200 (0:22:50.916)       0:27:57.353 **** 
=============================================================================== 
hadoop : run mapred demo --------------------------------------------------------------------------------------------------------------------------- 1370.92s
hadoop : Unarchive package - /usr/lib ---------------------------------------------------------------------------------------------------------------- 62.20s
hadoop : start hdfs ---------------------------------------------------------------------------------------------------------------------------------- 42.35s
hadoop : Download hadoop-2.8.2.tar.gz ---------------------------------------------------------------------------------------------------------------- 30.41s
jdk : Unarchive package ------------------------------------------------------------------------------------------------------------------------------ 23.33s
jdk : Download jdk-8u192-linux-x64.tar.gz ------------------------------------------------------------------------------------------------------------ 23.08s
hadoop : Install dependence packages ------------------------------------------------------------------------------------------------------------------ 7.16s
hadoop : start yarn ----------------------------------------------------------------------------------------------------------------------------------- 6.31s
hadoop : format namenode ------------------------------------------------------------------------------------------------------------------------------ 6.13s
hadoop : copy launch daemon script -------------------------------------------------------------------------------------------------------------------- 5.20s
hadoop : Present Hadoop Users, "hadoop,hdfs,yarn,mapred,spark,demo_runner" ---------------------------------------------------------------------------- 4.56s
jdk : Export JAVA_HOME -------------------------------------------------------------------------------------------------------------------------------- 4.06s
hadoop : Create link ---------------------------------------------------------------------------------------------------------------------------------- 3.57s
hadoop : run mr history server ------------------------------------------------------------------------------------------------------------------------ 2.97s
Gathering Facts --------------------------------------------------------------------------------------------------------------------------------------- 2.95s
hadoop : (Cleanup) Delete Hadoop Data & Log ----------------------------------------------------------------------------------------------------------- 2.84s
hadoop : Present Hadoop Group ------------------------------------------------------------------------------------------------------------------------- 2.61s
hadoop : Copy conf_editor ----------------------------------------------------------------------------------------------------------------------------- 2.16s
hadoop : Ssh-keyscan : localhost ---------------------------------------------------------------------------------------------------------------------- 1.89s
hadoop : Copy known_hosts, from hadoop to hdfs, yarn, mapred ------------------------------------------------------------------------------------------ 1.78s
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
