#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os.path
import warnings

requirements = [
    'requests',
    'django',
]

dependency_links = []
classifiers = []


def readme():
    try:
        root = os.path.abspath(os.path.dirname(__file__))
        with open(os.path.join(root, 'README.md')) as f:
            return f.read()
    except IOError:
        warnings.warn("Couldn't found README.md", RuntimeWarning)
        return ''


setup(
    name='SSAPI-Supapi',
    version='0.0.8',
    author='PerhapsSPY',
    author_email='py+d9@smartstudy.co.kr',
    maintainer='DevOps Team, SMARTSTUDY',
    maintainer_email='d9@smartstudy.co.kr',
    url='http://smartstudy.co.kr/',
    license='Proprietary',
    platforms='POSIX',
    description='',
    long_description=readme(),
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    entry_points={
    },
    install_requires=requirements,
    dependency_links=dependency_links,
    classifiers=classifiers,
)
