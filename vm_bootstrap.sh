#!/usr/bin/env bash

#add-apt-repository -y ppa:openjdk-r/ppa
#apt-get update

if ! [ -L /var/www ]; then
  rm -rf /var/www
  ln -fs /vagrant /var/www
fi

#echo r00tpassw0rd | passwd --stdin
echo "root:passw0rd" | chpasswd
#sed -i 's/\%sudo/sudo/g' /etc/sudoers

groupadd -g 9999 swift
useradd -u 9999 -g swift -G swift -d /home/swift -s /bin/bash swift
if [ $(getent group sudo) ]; then
	usermod -a -G sudo swift
fi
#getent group wheel || 
if [ $(getent group wheel) ]; then
	usermod -a -G wheel swift
fi

mkdir -p /home/swift/.ssh
chown -R swift:swift /home/swift
#echo passw0rd | passwd swift --stdin
echo "swift:passw0rd"  | chpasswd

ssh-keygen -t rsa -P '' -f /home/swift/.ssh/id_rsa
touch /home/swift/.ssh/authorized_keys
chmod 0600 /home/swift/.ssh/authorized_keys

chown -R swift:swift /home/swift/
cat /home/swift/.ssh/id_rsa.pub >> /home/swift/.ssh/authorized_keys

#cat /home/vagrant/host_id_rsa.pub  >> /home/swift/.ssh/authorized_keys
cat /home/vagrant/host_id_rsa.pub  >> /home/swift/.ssh/authorized_keys

eth1_cnf_file=/etc/sysconfig/network-scripts/ifcfg-eth1
if [ -f $eth1_cnf_file ]; then
	chown root:root $eth1_cnf_file
	chmod 0644 $eth1_cnf_file
	ifup eth1
fi

if [ -f /root/.profile ]; then
#     sed -i '/tty/!s/mesg n/tty -s \\&\\& mesg n/' /root/.profile
      sed -i 's/^mesg n$/tty -s \&\& mesg n/g' /root/.profile
fi