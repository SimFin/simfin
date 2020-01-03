##########################################################################
#
# Unit tests (pytest) for load.py
#
##########################################################################
# SimFin - Simple financial data for Python.
# www.simfin.com - www.github.com/simfin/simfin
# See README.md for instructions and LICENSE.txt for license details.
##########################################################################

import simfin as sf
from simfin.datasets import iter_all_datasets

##########################################################################
# Test configuration.

# Set data directory.
sf.set_data_dir(data_dir='~/simfin_data/')

# Load API key or use default 'free' if key-file doesn't exist.
sf.load_api_key(path='~/simfin_api_key.txt', default_key='free')

# Set number of days before refreshing data from SimFin server.
refresh_days = 30

##########################################################################
# Helper functions.

def _create_kwargs(variant, market):
    """
    Create a dict with keyword args for sf.load() functions that take
    variant, market and refresh_days as kwargs.
    """
    kwargs = \
        {
            'variant': variant,
            'market': market,
            'refresh_days': refresh_days,
        }

    return kwargs

##########################################################################
# Test functions.

def test_load():
    """Test simfin.bulk.load()"""
    for dataset, variant, market in iter_all_datasets():
        sf.load(dataset=dataset,
                variant=variant,
                market=market,
                refresh_days=refresh_days)


def test_load_income():
    """Test simfin.bulk.load_income()"""
    for dataset, variant, market in iter_all_datasets(datasets='income'):
        kwargs = _create_kwargs(variant=variant, market=market)

        sf.load_income(**kwargs)
        sf.load_income_banks(**kwargs)
        sf.load_income_insurance(**kwargs)


def test_load_balance():
    """Test simfin.bulk.load_balance()"""
    for dataset, variant, market in iter_all_datasets(datasets='balance'):
        kwargs = _create_kwargs(variant=variant, market=market)

        sf.load_balance(**kwargs)
        sf.load_balance_banks(**kwargs)
        sf.load_balance_insurance(**kwargs)


def test_load_cashflow():
    """Test simfin.bulk.load_cashflow()"""
    for dataset, variant, market in iter_all_datasets(datasets='cashflow'):
        kwargs = _create_kwargs(variant=variant, market=market)

        sf.load_cashflow(**kwargs)
        sf.load_cashflow_banks(**kwargs)
        sf.load_cashflow_insurance(**kwargs)


def test_load_shareprices():
    """Test simfin.bulk.load_shareprices()"""
    for dataset, variant, market in iter_all_datasets(datasets='shareprices'):
        kwargs = _create_kwargs(variant=variant, market=market)

        sf.load_shareprices(**kwargs)


def test_load_companies():
    """Test simfin.bulk.load_companies()"""
    for dataset, variant, market in iter_all_datasets(datasets='companies'):
        kwargs = _create_kwargs(variant=variant, market=market)

        sf.load_companies(**kwargs)


def test_load_industries():
    """Test simfin.bulk.load_industries()"""
    sf.load_industries(refresh_days=refresh_days)

##########################################################################
