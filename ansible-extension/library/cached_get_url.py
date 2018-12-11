#!/usr/bin/python
# coding: utf-8

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'nobody'}

DOCUMENTATION = """
---
module: cached_get_url
author:
    - 'Gao Yuan (@altiplanogao)'
short_description: get_url with local cache support.
description:
  - When use get_url, the module will download file from remote server, it costs time.
  	This module tries to save time by following steps:
  		1. check local cache (on ansible controller)
  		2. if cache exists, invoke 'copy'
  		3. if cache not exists, call module 'get_url' on ansible controller, and call 'copy' again
  	Thus, we do 'copy' prior to 'get_url', and 'get_url' called only once in the worst.
options:
  cached:
    required: true
    description:
      - The cache file location on ansible controller node.
      	Note: ansible user should has write permission to the file path.
  <get_url options>:
  	The module is a combination of get_url and copy, all get_url options are supported.
  <copy options>:
  	The module is a combination of get_url and copy, all copy options are supported, except:
  		- src: The option will be override by option 'cached'.
note:
  Local get_url is achieved by module delegation.
  Some task options (like 'become', 'become_method') will not affect this step.
"""

EXAMPLES = r"""
- name: Download file abc.zip from http://www.abc.com/abc.zip
  cached_get_url:
    cached: /cachedir/abc.zip
    url: http://www.abc.com/abc.zip
    dest: /temp/abc.zip
"""
