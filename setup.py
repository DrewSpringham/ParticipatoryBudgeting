# -*- coding: utf-8 -*-


from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

setup(
    name='PBProject',
    version='0.1.0',
    description='Participatory Budgeting with Location Conflicts',
    long_description=readme,
    author='Drew Springham',
    author_email='drew.springham@cs.ox.ac.uk',
    url='',
    packages=find_packages(exclude=('tests',))
)
