#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
        'requests', 'requests-toolbelt', 'oauthlib',
        'requests_oauthlib', 'pyahocorasick', ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', 'pytest-mock', 'hypothesis', 'tox', 'flake8']

setup(
    author="Joel Shprentz",
    author_email='jshprentz@his.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Communications',
    ],
    description="Load Meetup events into a Xibo digital signage CMS.",
    entry_points={
        'console_scripts': [
            'meetup2xibo=meetup2xibo.__main__:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='meetup2xibo',
    name='meetup2xibo',
    packages=find_packages(include=['meetup2xibo']),
    scripts=['bin/location-log2csv'],
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/jshprentz/meetup2xibo',
    version='2.0.1',
    zip_safe=False,
)
