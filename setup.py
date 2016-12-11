# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='commit-simulator',
    version='0.0.1',
    description='Generate commit messages from markov chains',
    long_description=readme,
    author='Robin Suter',
    author_email='robin@cblog.ch',
    url='https://github.com/Excape/commit-simulator',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
