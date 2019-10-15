##########################################################################
#
# Unit tests (pytest) for bulk.py
#
##########################################################################
# SimFin - Simple financial data for Python.
# www.simfin.com - www.github.com/simfin/simfin
# See README.md for instructions and LICENSE.txt for license details.
##########################################################################

import simfin as sf
from simfin.datasets import iter_all_datasets, valid_variants, valid_markets

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
        sf.bulk.load(dataset=dataset,
                     variant=variant,
                     market=market,
                     refresh_days=refresh_days)


def test_load_income():
    """Test simfin.bulk.load_income()"""
    dataset = 'income'
    for variant in valid_variants[dataset]:
        for market in valid_markets[dataset]:
            kwargs = _create_kwargs(variant=variant, market=market)

            sf.bulk.load_income(**kwargs)
            sf.bulk.load_income_banks(**kwargs)
            sf.bulk.load_income_insurance(**kwargs)


def test_load_balance():
    """Test simfin.bulk.load_balance()"""
    dataset = 'balance'
    for variant in valid_variants[dataset]:
        for market in valid_markets[dataset]:
            kwargs = _create_kwargs(variant=variant, market=market)

            sf.bulk.load_balance(**kwargs)
            sf.bulk.load_balance_banks(**kwargs)
            sf.bulk.load_balance_insurance(**kwargs)


def test_load_cashflow():
    """Test simfin.bulk.load_cashflow()"""
    dataset = 'cashflow'
    for variant in valid_variants[dataset]:
        for market in valid_markets[dataset]:
            kwargs = _create_kwargs(variant=variant, market=market)

            sf.bulk.load_cashflow(**kwargs)
            sf.bulk.load_cashflow_banks(**kwargs)
            sf.bulk.load_cashflow_insurance(**kwargs)


def test_load_shareprices():
    """Test simfin.bulk.load_shareprices()"""
    dataset = 'shareprices'
    for variant in valid_variants[dataset]:
        for market in valid_markets[dataset]:
            kwargs = _create_kwargs(variant=variant, market=market)

            sf.bulk.load_shareprices(**kwargs)


def test_load_companies():
    """Test simfin.bulk.load_companies()"""
    dataset = 'companies'
    for market in valid_markets[dataset]:
        sf.bulk.load_companies(market=market, refresh_days=refresh_days)


def test_load_industries():
    """Test simfin.bulk.load_industries()"""
    sf.bulk.load_industries(refresh_days=refresh_days)

##########################################################################
