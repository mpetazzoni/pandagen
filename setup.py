#!/usr/bin/env python

# Pandagen

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('requirements.txt') as r:
    requirements = r.readlines()

with open('pandagen/version.py') as v:
    exec(v.read())

setup(
    name=name,  # noqa
    version=version,  # noqa
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
