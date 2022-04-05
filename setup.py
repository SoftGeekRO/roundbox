#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import setuptools
from setuptools import setup


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


with open("README.md", "r") as fh:
    long_description = fh.read()

install_reqs = parse_requirements('requirements.txt')
reqs = install_reqs

setup(
      name='RoundBox',
      version='1.0',
      description='Just a small framework inspired by Django and HomeAssistant used for IoT monitoring and automation',
      license='GPL-3',
      author='Constantin Zaharia',
      author_email='constantin.zaharia@github.com',
      url='https://github.com/soulraven/roundBox',
      packages=setuptools.find_packages(),
      install_requires=reqs,
      provides=['RoundBox'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Topic :: Software Development :: Libraries',
          'License :: OSI Approved :: GPLv3 License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
      ],
      zip_safe=True
)
