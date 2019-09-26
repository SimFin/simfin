# -*- coding: utf-8 -*-
from setuptools import setup

# This is also defined in simfin/__init__.py and must be
# updated in both places.
MY_VERSION = '0.1.0'

setup(
    name='simfin',
    packages=['simfin'],
    version=MY_VERSION,
    description='Simple financial data from www.simfin.com',
    author=['Hvass-Labs', 'SimFin'],
    author_email='info@simfin.com',
    url='https://github.com/simfin/simfin',
    license='MIT',
    keywords=['financial data', 'finance'],
    install_requires=[
        'pandas',
        'numpy',
        'requests',
        'nbval'
    ],
)
