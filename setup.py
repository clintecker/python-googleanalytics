import sys
if sys.version_info < (2, 5):
  print >> sys.stderr, '%s: need Python 2.5 or later.' % sys.argv[0]
  print >> sys.stderror, 'Your python is %s' % sys.version
  sys.exit(1)

import os
from setuptools import setup, find_packages

setup(
  name = "python-googleanalytics",
  version = "1.0.2",
  url = 'http://github.com/clintecker/python-googleanalytics',
  license = 'BSD',
  description = "A python library for talking to the Google Analytics API",
  
  author = 'Clint Ecker',
  author_email = 'me@clintecker.com',
  
  packages = find_packages('src'),
  package_dir = {'': 'src'},
  
  install_requires = ['setuptools',],
  
  classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.5',
    'Topic :: Internet',
  ]
)
