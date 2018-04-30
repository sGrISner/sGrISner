#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from requirements import parse

from sGrISner import config


def readme():
    """
    Longer description from readme.
    """
    with open('README.md', 'r', encoding='utf-8') as readmefile:
        return readmefile.read()


def requirements():
    """
    Get requirements to install.
    """
    with open('requirements.txt', 'r') as req:
        return [dep.name for dep in parse(req)]


setup(
    name='sgrisner',
    version=config.__version__,
    description='Active GIS annotator',
    long_description=readme(),
    classifiers=[
        'License :: GNU GPL v3.0',
        'Programming Language :: Python :: 3.5'
    ],
    keywords='annotation gis pyqt5',
    url='https://github.com/sgrisner/sgrisner',
    author='Oussama Ennafii',
    author_email='oussama.ennafii@ign.fr',
    license='GNU GPL',
    packages=find_packages(exclude=['tests']),
    scripts=['sGrISner-app'],
    install_requires=requirements(),
    include_package_data=False,
    zip_safe=False
)
