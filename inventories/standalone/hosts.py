#!/usr/bin/env python


import sys, os, imp
# sys.path.append('..')
xinv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "XInv.py")
XInv = imp.load_source('XInv', xinv_path)

this_dir = os.path.dirname(os.path.realpath(__file__))
hostfile = this_dir

for hf in ['._hosts.yml','_hosts.yml','../._hosts.yml','../_hosts.yml' ] :
	hostfile = os.path.normpath(os.path.join(this_dir, hf))
	if os.path.exists(hostfile) :
		break

XInv.XInv(host_files = [
    hostfile
], group_files = [
    os.path.join(this_dir, "_groups.yml")
])