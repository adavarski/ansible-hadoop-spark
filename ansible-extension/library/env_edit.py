#!/usr/bin/python
# coding: utf-8

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'nobody'}


DOCUMENTATION = """
---
module: env_edit
author:
    - 'Gao Yuan (@altiplanogao)'
short_description: Insert/update/remove a text block
                   for environment variables.
description:
  - This module will insert/update/remove a set of environment variables.
    The module implementation relies on module 'blockinfile'.
options:
  varlist:
    required: true
    description:
      - The environment variables (key-value pair) to set.
  marker:
    required: false
    format: '{mark} TASK DESCRIPTION'
    default: None, will use default setting of module 'blockinfile'
    description:
      - The marker line template.
        "{mark}" will be replaced with "BEGIN" or "END".
  comment:
    required: false
    description: arbitrary comments.
  state:
    required: false
    choices: [ present, absent ]
    default: present
    description:
      - Whether the block should be there or not.
  profile_filename:
    required: false
    default: ''
    description:
      - Setting system environment variables will possibly result in writing
        file under /etc/profile.d/. The profile_filename indicates the .sh file to write to.
  insertafter:
    required: false
    default: EOF
    description:
      - Please refer to module 'blockinfile'
    choices: [ 'EOF', '*regex*' ]
  insertbefore:
    required: false
    default: None
    description:
      - Please refer to module 'blockinfile'
    choices: [ 'BOF', '*regex*' ]
  owner:
  	required: false
  	default: ''
  	description:
  	  - Specify the owner name of the environment variables
  group:
  	required: false
  	default: ''
  	description:
  	  - Specify the group name of the owner of the environment variables
notes:
  - This module has limited os platform support, error may shown on error.
"""

EXAMPLES = r"""
- name: set JAVA_HOME=/opt/jdk1.8, and export to PATH
  env_edit:
    varlist:
      - JAVA_HOME: /opt/jdk1.8
      - PATH: $JAVA_HOME/bin/:$PATH
    marker: "{mark} JAVA BLOCK"
    comment: "Java environment by ansible"
    state: present
    profile_filename: jdk.sh

- name: set MY_JAVA_HOME=/opt/jdk1.9, and override JAVA_HOME
  env_edit:
    varlist:
      - MY_JAVA_HOME: /opt/jdk1.9
      - JAVA_HOME: $MY_JAVA_HOME
    marker: "{mark} JAVA BLOCK"
    comment: "Java environment by ansible"
    state: present
    owner: andy
    group: wheel
"""
