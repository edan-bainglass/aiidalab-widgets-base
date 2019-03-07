#!/usr/bin/env python

from __future__ import absolute_import
from setuptools import setup, find_packages
import json

# pylint: disable=syntax-error
if __name__ == '__main__':
    # Provide static information in setup.json
    # such that it can be discovered automatically
    with open('metadata.json', 'r') as info:
        metadata = json.load(info)

    with open('setup.json', 'r') as info:
        kwargs = json.load(info)

    setup(
        packages=find_packages(),
        long_description=open('README.md').read(),
        long_description_content_type='text/markdown',
        author=metadata['authors'],
        description=metadata['description'],
        version=metadata['version'],
        **kwargs)
