#!/usr/bin/env python
'''
    steno3d_surfer: Steno3D parser plugin for Surfer .grd files
'''

from distutils.core import setup
from setuptools import find_packages

CLASSIFIERS = [
'Development Status :: 4 - Beta',
'Programming Language :: Python',
'Topic :: Scientific/Engineering',
'Topic :: Scientific/Engineering :: Mathematics',
'Topic :: Scientific/Engineering :: Physics',
'Operating System :: Microsoft :: Windows',
'Operating System :: POSIX',
'Operating System :: Unix',
'Operating System :: MacOS',
'Natural Language :: English',
]

with open('README.rst') as f:
    LONG_DESCRIPTION = ''.join(f.readlines())

setup(
    name = 'steno3d_surfer',
    version = '0.0.2',
    packages = find_packages(),
    install_requires = ['numpy>=1.7',
                        'steno3d>=0.2.9'],
    author = '3point Science',
    author_email = 'info@3ptscience.com',
    description = 'steno3d_surfer',
    long_description = LONG_DESCRIPTION,
    keywords = 'visualization',
    url = 'https://steno3d.com/',
    download_url = 'http://github.com/3ptscience/steno3d-surfer',
    classifiers=CLASSIFIERS,
    platforms = ['Windows', 'Linux', 'Solaris', 'Mac OS-X', 'Unix'],
    license = 'MIT License',
    use_2to3 = False,
)
