#!/usr/bin/env python

# Pandagen

import os
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('requirements.txt') as r:
    requirements = r.readlines()

setup(
    name='pandagen',
    version='0.1.0',
    description='Static resource parsing and generation pipeline',
    long_description=readme,
    zip_safe=True,
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],

    author='Maxime Petazzoni',
    author_email='maxime.petazzoni@bulix.org',
    license='GNU General Public License v3',
    keywords='pandagen website static generator blog markdown wiki',
    url='http://github.com/mpetazzoni/pandagen'
)
