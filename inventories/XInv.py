#!/usr/bin/env python

__version__ = '1.1'
__all__ = [
  'XInv'
]

import sys
import os
import argparse
import re
from time import time
from six import iteritems
import yaml
import copy

try:
  import json
except ImportError:
  import simplejson as json

class XInv(object):

  def __init__(self, host_files = [], group_files = [], with_controller=False):
    # self.
    self.all_hosts = dict()
    self.all_groups = list()
    self.result = self._empty_inventory()
    self.with_controller = with_controller
    self._load_resource( host_files , group_files )
    self._write_meta()
    self._write_groups()
    print(json.dumps(self.result, indent=2))

  def _empty_inventory(self):
    return {"_meta": {"hostvars": {}}}

  def parse_cli_args(self):
    parser = argparse.ArgumentParser(description='Produce an Ansible Inventory file based on ...')
    parser.add_argument('--list', action='store_true', default=True,
                        help='List instances (default: True)')
    parser.add_argument('--host', action='store',
                        help='Get all the variables about a specific instance')
    self.args = parser.parse_args()

  def _load_hostfile(self, hostfile):
    _host_default_vars = "host_default_vars"
    _hosts = "hosts"
    with open(hostfile, 'r') as stream:
      file_content = {_host_default_vars : {}, _hosts: {}}
      try:
        file_content = yaml.load(stream)
        host_default = file_content[_host_default_vars]
        host_nodes = file_content[_hosts]
        for _node in host_nodes:
          host = copy.deepcopy(host_nodes[_node])
          vars_cp = copy.deepcopy(host_default)
          vars_cp["hostname"] = host["hostname"]
          vars_cp["ansible_host"] = host["address"]
          vars_cp.update(host.get("vars", {}))
          host["alias"] = _node
          host["vars"] = vars_cp
          self.all_hosts[_node] = host
      except yaml.YAMLError as exc:
        setattr(self, hostfile, "load failed.");

  def _load_groupfile(self, groupfile):
    with open(groupfile, 'r') as stream:
      file_content = {"group_default_vars": {}, "groups": []}
      try:
        file_content = yaml.load(stream)
        group_vars = file_content.get("group_default_vars", {})
        _groups = file_content["groups"]
        for _group in _groups:
          group = copy.deepcopy(_group)
          vars_cp = copy.deepcopy(group_vars)
          vars_cp.update(_group.get("vars", {}))
          group["vars"] = vars_cp
          self.all_groups.append(group)
      except yaml.YAMLError as exc:
        setattr(self, groupfile, "load failed.");

  def _load_resource(self, host_files = [], group_files = []):
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # dir_path = os.path.join(dir_path, "conf")
    for hostfile in host_files:
      # hostfile = os.path.join(dir_path, hostfile)
      self._load_hostfile(hostfile)
    for groupfile in group_files:
      # groupfile = os.path.join(dir_path, groupfile)
      self._load_groupfile(groupfile)

  def _write_meta(self):
    hostvars = {}
    if self.with_controller:
      hostvars["controller"] = {"ansible_connection": "local"}
    for host_key in self.all_hosts:
      host = self.all_hosts[host_key]
      hostvars[host_key] = host.get("vars", {})
    self.result["_meta"] = {"hostvars": hostvars}

  def _write_groups(self):
    if self.with_controller:
      self.result["local"] = {"hosts": ["controller"]}
    for _group in self.all_groups:
      grp_name = _group["name"]
      group = {"children" : _group.get("children", []),
               "hosts": _group.get("hosts", []),
               "vars" : _group.get("vars", {})}
      self.result[grp_name] = group



