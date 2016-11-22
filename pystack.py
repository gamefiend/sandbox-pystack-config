#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project: sandbox-pystack-config
File:    pystack.py
"""

import glob
import json
import os
import sys
import yaml


class PyStack(object):

    def __init__(self, datadir, templatedir, metafile):
        self.datadir = datadir
        self.templatedir = templatedir
        self.metafile = metafile
        self.datafiles = {}
        self.os_config = {}
        # Read metadata and yaml files in directory into os_config dict
        self.load_metadata()

    def list_files(self, directory, extensions=('*.yml', '*.yaml')):
        _files = []
        if not os.path.isdir(directory):
            raise Exception("'{}' directory does not exist".format(directory))
        else:
            for ext in extensions:
                _files.extend(glob.glob(os.path.join(directory, ext)))
            if not _files:
                raise Exception("Directory list is empty: .{}/".format(directory))
            return _files

    def read_yamlconfig(self, filepath):
        with open(os.path.join(self.datadir, filepath), 'r') as f:
            yamlconfig = yaml.load(f)
        return yamlconfig

    def load_metadata(self):
        """Read metadata file, for example in data/pystack-meta.yaml"""
        self.datafiles = self.list_files(self.datadir)
        with open(os.path.join(self.datadir, self.metafile), 'r') as f:
            metadata = yaml.load(f)
            for service in metadata:
                if metadata[service]['data'] in [os.path.basename(x) for x in self.datafiles]:
                    # Initialize nested dict, such as os_config['nova']
                    self.os_config[service] = {}
                    # Set OpenStack service configuration, excluding redundant service name section by adding [service]
                    self.os_config[service]['data'] = self.read_yamlconfig(metadata[service]['data'])[service]
                    # Set service template file from metadata configuration
                    self.os_config[service]['config'] = metadata[service]['config']

    def load_servicedata(self):
        """Read service.yaml file, for example in data/nova.yaml"""
        self.datafiles = self.list_files(self.datadir)
        with open(os.path.join(self.datadir, self.metafile), 'r') as f:
            metadata = yaml.load(f)
            for service in metadata:
                if metadata[service]['data'] in [os.path.basename(x) for x in self.datafiles]:
                    # Initialize nested dict, such as os_config['nova']
                    self.os_config[service] = {}
                    # Set OpenStack service configuration, excluding redundant service name section by adding [service]
                    self.os_config[service]['data'] = self.read_yamlconfig(metadata[service]['data'])[service]
                    # Set service template file from metadata configuration
                    self.os_config[service]['config'] = metadata[service]['config']

    def service_data(self, service):
        """Returns service data from self.os_config"""
        return json.dumps(self.os_config[service]['data'], indent=4, sort_keys=True)

    def service_config(self, service):
        """Returns service configuration files from self.os_config"""
        return json.dumps(self.os_config[service]['config'], indent=4, sort_keys=True)

    def __str__(self):
        """
        String representation of PyStack object.
        Prints all os_config dictionary in human readable format
        """
        return json.dumps(self.os_config, indent=4, sort_keys=True)


def main():
    """Python script entrypoint"""
    settings = PyStack(datadir="data", templatedir="config", metafile="pystack-meta.yaml")
    print(settings.service_data('nova'))
    print(settings.service_config('nova'))
    print(settings)
    sys.exit(0)

if __name__ == '__main__':
    main()
else:
    print("PyStack loaded as a module")
