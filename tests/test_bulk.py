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
from simfin.datasets import iter_all_datasets, valid_variants

##########################################################################
# Test configuration.

# Set data directory.
sf.set_data_dir(data_dir='~/simfin_data/')

# Load API key or use default 'free' if key-file doesn't exist.
sf.load_api_key(path='~/simfin_api_key.txt', default_key='free')

# Set number of days before refreshing data from SimFin server.
refresh_days = 30

##########################################################################
# Test functions.

def test_load():
    """Test simfin.bulk.load()"""
    for dataset, variant in iter_all_datasets():
        sf.bulk.load(dataset=dataset,
                     variant=variant,
                     refresh_days=refresh_days)


def test_load_income():
    """Test simfin.bulk.load_income()"""
    for variant in valid_variants['income']:
        sf.bulk.load_income(variant=variant, refresh_days=refresh_days)
        sf.bulk.load_income_banks(variant=variant, refresh_days=refresh_days)
        sf.bulk.load_income_insurance(variant=variant, refresh_days=refresh_days)


def test_load_balance():
    """Test simfin.bulk.load_balance()"""
    for variant in valid_variants['balance']:
        sf.bulk.load_balance(variant=variant, refresh_days=refresh_days)
        sf.bulk.load_balance_banks(variant=variant, refresh_days=refresh_days)
        sf.bulk.load_balance_insurance(variant=variant, refresh_days=refresh_days)


def test_load_cashflow():
    """Test simfin.bulk.load_cashflow()"""
    for variant in valid_variants['cashflow']:
        sf.bulk.load_cashflow(variant=variant, refresh_days=refresh_days)
        sf.bulk.load_cashflow_banks(variant=variant, refresh_days=refresh_days)
        sf.bulk.load_cashflow_insurance(variant=variant, refresh_days=refresh_days)


def test_load_shareprices():
    """Test simfin.bulk.load_shareprices()"""
    for variant in valid_variants['shareprices']:
        sf.bulk.load_shareprices(variant=variant, refresh_days=refresh_days)


def test_load_companies():
    """Test simfin.bulk.load_companies()"""
    sf.bulk.load_companies(refresh_days=refresh_days)


def test_load_industries():
    """Test simfin.bulk.load_industries()"""
    sf.bulk.load_industries(refresh_days=refresh_days)

##########################################################################
