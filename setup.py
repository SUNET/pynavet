#!/usr/bin/env python

from setuptools import setup, find_packages

__author__ = 'Stefan Wold'

version = '0.5'

install_requires = [
    'suds >= 0.4.1',
    'requests >= 1.2.3',
    'xmltodict == 0.8.6',
    'lxml >= 3.0',
]

testing_extras = [
    'nose==1.2.1',
    'nosexcover==1.0.8',
    'coverage==3.6',
    'mock==1.0.1',
    'suds>=0.4.1',
]

setup(
    name='pynavet',
    version=version,
    description='Python client for the Swedish government service NAVET',
    keywords='NAVET',
    author='Stefan Wold',
    author_email='swold@sunet.se',
    url='https://github.com/SUNET/pynavet',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    package_data={
	'pynavet': ['wsdl/*.wsdl', 'schema/*.xsd', 'xslt/*.xsl']
    },
    zip_safe=False,
    install_requires=install_requires,
    extras_require={
        'testing': testing_extras,
    }
)
