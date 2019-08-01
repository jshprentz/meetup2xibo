#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
        'requests', 'requests-toolbelt', 'oauthlib', 'jinja2',
        'requests_oauthlib', 'pyahocorasick', 'parsley', 'pytz']

setup_requirements = ['pytest-runner', ]

test_requirements = [
        'pytest', 'pytest-mock', 'hypothesis', 'tox', 'flake8',
        'freezegun']

setup(
    author="Joel Shprentz",
    author_email='jshprentz@his.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
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
            'meetup2xibo=meetup2xibo.updater.__main__:main',
            'summarize-m2x-logs=meetup2xibo.log_summarizer.__main__:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords='meetup2xibo',
    name='meetup2xibo',
    packages=find_packages(include=['meetup2xibo']),
    project_urls={
        'Documentation': 'https://meetup2xibo.readthedocs.io/',
        'Source Code': 'https://github.com/jshprentz/meetup2xibo'
    },
    scripts=[
	'bin/yesterday',
	],
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/jshprentz/meetup2xibo',
    version='3.2.1',
    zip_safe=False,
)
