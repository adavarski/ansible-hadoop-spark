from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import AnsibleError, AnsibleFilterError

from ansible.plugins.filter.json_query import json_query
from jinja2 import filters, contextfilter
# - name: Gather Nodes with property 'xxx_installed' == true
#   set_fact:
#     xxx_nodes: '{{ hostvars.values() | json_query("[*].{id: inventory_hostname, x_prop: xxx_installed}")
#                       | selectattr("x_prop", "equalto", true)
#                       | list | json_query("[*].id") }}'



@contextfilter
def keys_of_prop(a, obj_list, id_prop, prop, val):
    # get a simple list
    make_simple_list = json_query(obj_list, "[*].{id: %s, x_prop: %s}" % (id_prop, prop))
    select = filters.do_selectattr(a, make_simple_list, "x_prop", "equalto", val)
    new_list = filters.do_list(select)
    result = json_query(new_list, "[*].id")
    return result

@contextfilter
def hosts_with(a, hostvars, prop, val):
    return keys_of_prop(a, hostvars.values(), id_prop='inventory_hostname', prop=prop, val=val)

# ---- Ansible filters ----
class FilterModule(object):
    ''' By Prop filter '''

    def filters(self):
        return {
            'keys_of_prop': keys_of_prop,
            'hosts_with': hosts_with,
        }
