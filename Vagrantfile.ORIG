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
$num_instances = 7
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
