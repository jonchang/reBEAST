#!/usr/bin/env python

import codecs
import os
import re
from setuptools import setup, find_packages


def read(*parts):
    return codecs.open(os.path.join(os.path.dirname(__file__), *parts), encoding='utf8').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='reBEAST',
    description='update the starting parameters in a BEAST 1.x XML file based on an existing tracelog',
    long_description=read('README.md'),
    version=find_version('rebeast/rebeast.py'),
    packages=['rebeast'],
    author='Jonathan Chang',
    author_email='jonathan.chang@ucla.edu',
    url='https://github.com/jonchang/reBEAST',
    license='AGPLv3',
    entry_points={
      'console_scripts':[
          'rebeast = rebeast.rebeast:main'
      ]
   }
)
