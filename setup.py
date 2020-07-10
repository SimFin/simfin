# -*- coding: utf-8 -*-
from setuptools import setup

# This is also defined in simfin/__init__.py and must be
# updated in both places.
MY_VERSION = '0.8.1'

setup(
    name='simfin',
    packages=['simfin'],
    version=MY_VERSION,
    description='Simple financial data for Python',
    long_description='SimFin makes it easy to obtain and use financial and '
                     'stock-market data in Python. It automatically downloads '
                     'share-prices and fundamental data from the '
                     '[SimFin](https://www.simfin.com/) server, '
                     'saves the data to disk for future use, and loads '
                     'the data into Pandas DataFrames.',
    long_description_content_type="text/markdown",
    author='SimFin',
    author_email='info@simfin.com',
    url='https://github.com/simfin/simfin',
    license='MIT',
    keywords=['financial data', 'finance'],
    install_requires=[
        'pandas',
        'numpy',
        'requests',
    ],
)
