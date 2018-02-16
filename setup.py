#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


def readme():
    """
    Longer description from readme.
    """
    with open('README.md', 'r', encoding='utf-8') as readmefile:
        return readmefile.read()


setup(
    name='sgrisner',
    version='0.1.0',
    description='Active GIS annotator',
    long_description=readme(),
    classifiers=[
        'License :: GNU GPL v3.0',
        'Programming Language :: Python :: 3.5'
    ],
    keywords='qualification building 3d reconstruction graphs computer vision',
    url='https://github.com/sgrisner/sgrisner',
    author='Oussama Ennafii',
    author_email='oussama.ennafii@ign.fr',
    license='GNU GPL',
    packages=find_packages(exclude=['tests']),
    scripts=['sGrISner'],
    install_requires=[
            'PyQt5',
            'georasters',
            'pyshp',
            'numpy',
            'qimage2ndarray'
    ],
    include_package_data=False,
    zip_safe=False
)
