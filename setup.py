#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import djangocms_instagram

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = djangocms_instagram.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    print('Tagging the version on github:')
    os.system('git tag -a %s -m "version %s"' % (version, version))
    os.system('git push --tags')
    sys.exit()

readme = open('README.rst').read()

setup(
    name='djangocms-instagram',
    version=version,
    description="""A simple but versatile Instagram plugin for your django-cms powered sites.""",
    long_description=readme,
    author='Mishbah Razzaque',
    author_email='mishbahx@gmail.com',
    url='https://github.com/mishbahr/djangocms-instagram',
    packages=[
        'djangocms_instagram',
    ],
    include_package_data=True,
    install_requires=[
        'django-appconf',
        'django-connected',
        'django-cms>=3.0',
        'python-instagram',
    ],
    license="BSD",
    zip_safe=False,
    keywords='djangocms-instagram',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
