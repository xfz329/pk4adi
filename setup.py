#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   setup.py
@Contact :   Jiang Feng(silencejiang@zju.edu.cn)
@License :   (C)Copyright 2004-2020, Zhejiang University
"""


import os
import re
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

version_file = open(os.path.join(here, 'pk4adi', '__init__.py'), 'r')
__version__ = re.sub(
    r".*\b__version__\s+=\s+'([^']+)'.*",
    r'\1',
    [line.strip() for line in version_file if '__version__' in line].pop(0)
)
version_file.close()

short_description = """Using PK to Measure the Performance of Anesthetic Depth Indicators."""

try:
    long_description = open('README.md', encoding="utf-8").read(),
except IOError:
    long_description = "See README.md where installed."


def get_install_requires():
    reqs = [
        'pandas>=0.18.0',
        'numpy>=1.21.6',
        'scipy>=1.9.0',
        'tabulate'
    ]
    return reqs


setup(
    name="pk4adi",
    version=__version__,
    author="silencejiang",
    author_email="silencejiang@zju.edu.cn",
    url='https://github.com/xfz329/pk.git',
    description=short_description,
    long_description_content_type="text/markdown",
    long_description=long_description,
    python_requires=">=3.8",
    install_requires=get_install_requires(),
    packages=find_packages(),
    license='MIT License',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    package_data={'': ['*.csv', '*.txt', '.toml']},
    include_package_data=True
)
