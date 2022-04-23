#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import setuptools
from setuptools import setup

from RoundBox.version import __version__


def parse_requirements(filename):
    """load requirements from a pip requirements file

    :param filename:
    :return:
    """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

install_reqs = parse_requirements('requirements.txt')
reqs = install_reqs

setup(
    name='RoundBox',
    version=__version__,
    description='Just a small framework inspired by Django and HomeAssistant used for IoT monitoring and automation',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='GPL-3',
    author='Constantin Zaharia',
    author_email='constantin.zaharia@progeek.ro',
    url='https://github.com/soulraven/roundBox',
    project_urls={
        "Source": "https://github.com/soulraven/roundbox",
        "Issues": "https://github.com/soulraven/roundbox/issues",
        "Discussions": "https://github.com/soulraven/roundbox/discussions",
        "Documentation": "https://soulraven.github.io/roundbox/",
    },
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
    zip_safe=True,
    python_requires=">=3.10",
)
