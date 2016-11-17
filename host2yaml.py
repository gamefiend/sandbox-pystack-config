import os
import yaml

hosts_dict = {}

# read the hosts file
with open('test_hosts', mode='r') as hosts_source:

# split the file by space
# make a dictionary.....
#   1st index of the split is the key, everything is a list on that line.
