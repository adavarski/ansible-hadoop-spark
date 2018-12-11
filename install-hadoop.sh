#!/bin/bash

ansible-playbook -i inventories/hadoop-single hadoop.yaml

# ansible-playbook -i inventories/hadoop hadoop-cluster.yaml