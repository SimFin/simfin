##########################################################################
#
# Unit tests (pytest) for load.py
#
##########################################################################
# SimFin - Simple financial data for Python.
# www.simfin.com - www.github.com/simfin/simfin
# See README.md for instructions and LICENSE.txt for license details.
##########################################################################
import datetime

import simfin as sf
from simfin.datasets import iter_all_datasets

##########################################################################
# Test configuration.

# Set data directory.
sf.set_data_dir(data_dir='~/simfin_data/')

# Load API key or use default 'free' if key-file doesn't exist.
sf.set_api_key("8fe38a8f-15a3-415d-abfc-87c05575c3cc")

# Set number of days before refreshing data from SimFin server.
refresh_days = 30

all_dataset_test = [{"dataset": "income", "variant": "quarterly", "market": "US", "premium": "false"},
                    {"dataset": "income", "variant": "annual", "market": "US", "premium": "false"},
                    {"dataset": "income", "variant": "ttm", "market": "US", "premium": "false"},
                    {"dataset": "income", "variant": "quarterly-full", "market": "US", "premium": "true"},
                    {"dataset": "income", "variant": "annual-full", "market": "US", "premium": "true"},
                    {"dataset": "income", "variant": "ttm-full", "market": "US", "premium": "true"},
                    {"dataset": "income", "variant": "quarterly-asreported", "market": "US", "premium": "true"},
                    {"dataset": "income", "variant": "annual-asreported", "market": "US", "premium": "true"},
                    {"dataset": "income", "variant": "ttm-asreported", "market": "US", "premium": "true"},
                    {"dataset": "income", "variant": "quarterly-full-asreported", "market": "US", "premium": "true"},
                    {"dataset": "income", "variant": "annual-full-asreported", "market": "US", "premium": "true"},
                    {"dataset": "income", "variant": "ttm-full-asreported", "market": "US", "premium": "true"},
                    {"dataset": "balance", "variant": "quarterly", "market": "US", "premium": "false"},
                    {"dataset": "balance", "variant": "annual", "market": "US", "premium": "false"},
                    {"dataset": "balance", "variant": "ttm", "market": "US", "premium": "false"},
                    {"dataset": "balance", "variant": "quarterly-full", "market": "US", "premium": "true"},
                    {"dataset": "balance", "variant": "annual-full", "market": "US", "premium": "true"},
                    {"dataset": "balance", "variant": "ttm-full", "market": "US", "premium": "true"},
                    {"dataset": "balance", "variant": "quarterly-asreported", "market": "US", "premium": "true"},
                    {"dataset": "balance", "variant": "annual-asreported", "market": "US", "premium": "true"},
                    {"dataset": "balance", "variant": "ttm-asreported", "market": "US", "premium": "true"},
                    {"dataset": "balance", "variant": "quarterly-full-asreported", "market": "US", "premium": "true"},
                    {"dataset": "balance", "variant": "annual-full-asreported", "market": "US", "premium": "true"},
                    {"dataset": "balance", "variant": "ttm-full-asreported", "market": "US", "premium": "true"},
                    {"dataset": "cashflow", "variant": "quarterly", "market": "US", "premium": "false"},
                    {"dataset": "cashflow", "variant": "annual", "market": "US", "premium": "false"},
                    {"dataset": "cashflow", "variant": "ttm", "market": "US", "premium": "false"},
                    {"dataset": "cashflow", "variant": "quarterly-full", "market": "US", "premium": "true"},
                    {"dataset": "cashflow", "variant": "annual-full", "market": "US", "premium": "true"},
                    {"dataset": "cashflow", "variant": "ttm-full", "market": "US", "premium": "true"},
                    {"dataset": "cashflow", "variant": "quarterly-asreported", "market": "US", "premium": "true"},
                    {"dataset": "cashflow", "variant": "annual-asreported", "market": "US", "premium": "true"},
                    {"dataset": "cashflow", "variant": "ttm-asreported", "market": "US", "premium": "true"},
                    {"dataset": "cashflow", "variant": "quarterly-full-asreported", "market": "US", "premium": "true"},
                    {"dataset": "cashflow", "variant": "annual-full-asreported", "market": "US", "premium": "true"},
                    {"dataset": "cashflow", "variant": "ttm-full-asreported", "market": "US", "premium": "true"},
                    {"dataset": "income-banks", "variant": "quarterly", "market": "US", "premium": "false"},
                    {"dataset": "income-banks", "variant": "annual", "market": "US", "premium": "false"},
                    {"dataset": "income-banks", "variant": "ttm", "market": "US", "premium": "false"},
                    {"dataset": "income-banks", "variant": "quarterly-full", "market": "US", "premium": "true"},
                    {"dataset": "income-banks", "variant": "annual-full", "market": "US", "premium": "true"},
                    {"dataset": "income-banks", "variant": "ttm-full", "market": "US", "premium": "true"},
                    {"dataset": "income-banks", "variant": "quarterly-asreported", "market": "US", "premium": "true"},
                    {"dataset": "income-banks", "variant": "annual-asreported", "market": "US", "premium": "true"},
                    {"dataset": "income-banks", "variant": "ttm-asreported", "market": "US", "premium": "true"},
                    {"dataset": "income-banks", "variant": "quarterly-full-asreported", "market": "US",
                     "premium": "true"},
                    {"dataset": "income-banks", "variant": "annual-full-asreported", "market": "US", "premium": "true"},
                    {"dataset": "income-banks", "variant": "ttm-full-asreported", "market": "US", "premium": "true"},
                    {"dataset": "balance-banks", "variant": "quarterly", "market": "US", "premium": "false"},
                    {"dataset": "balance-banks", "variant": "annual", "market": "US", "premium": "false"},
                    {"dataset": "balance-banks", "variant": "ttm", "market": "US", "premium": "false"},
                    {"dataset": "balance-banks", "variant": "quarterly-full", "market": "US", "premium": "true"},
                    {"dataset": "balance-banks", "variant": "annual-full", "market": "US", "premium": "true"},
                    {"dataset": "balance-banks", "variant": "ttm-full", "market": "US", "premium": "true"},
                    {"dataset": "balance-banks", "variant": "quarterly-asreported", "market": "US", "premium": "true"},
                    {"dataset": "balance-banks", "variant": "annual-asreported", "market": "US", "premium": "true"},
                    {"dataset": "balance-banks", "variant": "ttm-asreported", "market": "US", "premium": "true"},
                    {"dataset": "balance-banks", "variant": "quarterly-full-asreported", "market": "US",
                     "premium": "true"},
                    {"dataset": "balance-banks", "variant": "annual-full-asreported", "market": "US",
                     "premium": "true"},
                    {"dataset": "balance-banks", "variant": "ttm-full-asreported", "market": "US", "premium": "true"},
                    {"dataset": "cashflow-banks", "variant": "quarterly", "market": "US", "premium": "false"},
                    {"dataset": "cashflow-banks", "variant": "annual", "market": "US", "premium": "false"},
                    {"dataset": "cashflow-banks", "variant": "ttm", "market": "US", "premium": "false"},
                    {"dataset": "cashflow-banks", "variant": "quarterly-full", "market": "US", "premium": "true"},
                    {"dataset": "cashflow-banks", "variant": "annual-full", "market": "US", "premium": "true"},
                    {"dataset": "cashflow-banks", "variant": "ttm-full", "market": "US", "premium": "true"},
                    {"dataset": "cashflow-banks", "variant": "quarterly-asreported", "market": "US", "premium": "true"},
                    {"dataset": "cashflow-banks", "variant": "annual-asreported", "market": "US", "premium": "true"},
                    {"dataset": "cashflow-banks", "variant": "ttm-asreported", "market": "US", "premium": "true"},
                    {"dataset": "cashflow-banks", "variant": "quarterly-full-asreported", "market": "US",
                     "premium": "true"},
                    {"dataset": "cashflow-banks", "variant": "annual-full-asreported", "market": "US",
                     "premium": "true"},
                    {"dataset": "cashflow-banks", "variant": "ttm-full-asreported", "market": "US", "premium": "true"},
                    {"dataset": "income-insurance", "variant": "quarterly", "market": "US", "premium": "false"},
                    {"dataset": "income-insurance", "variant": "annual", "market": "US", "premium": "false"},
                    {"dataset": "income-insurance", "variant": "ttm", "market": "US", "premium": "false"},
                    {"dataset": "income-insurance", "variant": "quarterly-full", "market": "US", "premium": "true"},
                    {"dataset": "income-insurance", "variant": "annual-full", "market": "US", "premium": "true"},
                    {"dataset": "income-insurance", "variant": "ttm-full", "market": "US", "premium": "true"},
                    {"dataset": "income-insurance", "variant": "quarterly-asreported", "market": "US",
                     "premium": "true"},
                    {"dataset": "income-insurance", "variant": "annual-asreported", "market": "US", "premium": "true"},
                    {"dataset": "income-insurance", "variant": "ttm-asreported", "market": "US", "premium": "true"},
                    {"dataset": "income-insurance", "variant": "quarterly-full-asreported", "market": "US",
                     "premium": "true"},
                    {"dataset": "income-insurance", "variant": "annual-full-asreported", "market": "US",
                     "premium": "true"},
                    {"dataset": "income-insurance", "variant": "ttm-full-asreported", "market": "US",
                     "premium": "true"},
                    {"dataset": "balance-insurance", "variant": "quarterly", "market": "US", "premium": "false"},
                    {"dataset": "balance-insurance", "variant": "annual", "market": "US", "premium": "false"},
                    {"dataset": "balance-insurance", "variant": "ttm", "market": "US", "premium": "false"},
                    {"dataset": "balance-insurance", "variant": "quarterly-full", "market": "US", "premium": "true"},
                    {"dataset": "balance-insurance", "variant": "annual-full", "market": "US", "premium": "true"},
                    {"dataset": "balance-insurance", "variant": "ttm-full", "market": "US", "premium": "true"},
                    {"dataset": "balance-insurance", "variant": "quarterly-asreported", "market": "US",
                     "premium": "true"},
                    {"dataset": "balance-insurance", "variant": "annual-asreported", "market": "US", "premium": "true"},
                    {"dataset": "balance-insurance", "variant": "ttm-asreported", "market": "US", "premium": "true"},
                    {"dataset": "balance-insurance", "variant": "quarterly-full-asreported", "market": "US",
                     "premium": "true"},
                    {"dataset": "balance-insurance", "variant": "annual-full-asreported", "market": "US",
                     "premium": "true"},
                    {"dataset": "balance-insurance", "variant": "ttm-full-asreported", "market": "US",
                     "premium": "true"},
                    {"dataset": "cashflow-insurance", "variant": "quarterly", "market": "US", "premium": "false"},
                    {"dataset": "cashflow-insurance", "variant": "annual", "market": "US", "premium": "false"},
                    {"dataset": "cashflow-insurance", "variant": "ttm", "market": "US", "premium": "false"},
                    {"dataset": "cashflow-insurance", "variant": "quarterly-full", "market": "US", "premium": "true"},
                    {"dataset": "cashflow-insurance", "variant": "annual-full", "market": "US", "premium": "true"},
                    {"dataset": "cashflow-insurance", "variant": "ttm-full", "market": "US", "premium": "true"},
                    {"dataset": "cashflow-insurance", "variant": "quarterly-asreported", "market": "US",
                     "premium": "true"},
                    {"dataset": "cashflow-insurance", "variant": "annual-asreported", "market": "US",
                     "premium": "true"},
                    {"dataset": "cashflow-insurance", "variant": "ttm-asreported", "market": "US", "premium": "true"},
                    {"dataset": "cashflow-insurance", "variant": "quarterly-full-asreported", "market": "US",
                     "premium": "true"},
                    {"dataset": "cashflow-insurance", "variant": "annual-full-asreported", "market": "US",
                     "premium": "true"},
                    {"dataset": "cashflow-insurance", "variant": "ttm-full-asreported", "market": "US",
                     "premium": "true"},
                    {"dataset": "derived", "variant": "quarterly", "market": "US", "premium": "true"},
                    {"dataset": "derived", "variant": "annual", "market": "US", "premium": "true"},
                    {"dataset": "derived", "variant": "ttm", "market": "US", "premium": "true"},
                    {"dataset": "derived", "variant": "quarterly-asreported", "market": "US", "premium": "true"},
                    {"dataset": "derived", "variant": "annual-asreported", "market": "US", "premium": "true"},
                    {"dataset": "derived", "variant": "ttm-asreported", "market": "US", "premium": "true"},
                    {"dataset": "derived-banks", "variant": "quarterly", "market": "US", "premium": "true"},
                    {"dataset": "derived-banks", "variant": "annual", "market": "US", "premium": "true"},
                    {"dataset": "derived-banks", "variant": "ttm", "market": "US", "premium": "true"},
                    {"dataset": "derived-banks", "variant": "quarterly-asreported", "market": "US", "premium": "true"},
                    {"dataset": "derived-banks", "variant": "annual-asreported", "market": "US", "premium": "true"},
                    {"dataset": "derived-banks", "variant": "ttm-asreported", "market": "US", "premium": "true"},
                    {"dataset": "derived-insurance", "variant": "quarterly", "market": "US", "premium": "true"},
                    {"dataset": "derived-insurance", "variant": "annual", "market": "US", "premium": "true"},
                    {"dataset": "derived-insurance", "variant": "ttm", "market": "US", "premium": "true"},
                    {"dataset": "derived-insurance", "variant": "quarterly-asreported", "market": "US",
                     "premium": "true"},
                    {"dataset": "derived-insurance", "variant": "annual-asreported", "market": "US", "premium": "true"},
                    {"dataset": "derived-insurance", "variant": "ttm-asreported", "market": "US", "premium": "true"},
                    {"dataset": "shareprices", "variant": "daily", "market": "US", "premium": "false"},
                    {"dataset": "shareprices", "variant": "latest", "market": "US", "premium": "false"},
                    {"dataset": "derived-shareprices", "variant": "daily", "market": "US", "premium": "true"},
                    {"dataset": "derived-shareprices", "variant": "latest", "market": "US", "premium": "true"},
                    {"dataset": "derived-shareprices", "variant": "daily-asreported", "market": "US",
                     "premium": "true"},
                    {"dataset": "derived-shareprices", "variant": "latest-asreported", "market": "US",
                     "premium": "true"}]


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
def test_load_all():
    for i, item in enumerate(all_dataset_test):
        t = sf.load(dataset=item["dataset"],
                    variant=item["variant"],
                    market=item["market"],
                    start_date="2023-03-01",
                    end_date=datetime.datetime(2025, 5, 1),
                    refresh_days=refresh_days)

        print(t)


test_load_all()
