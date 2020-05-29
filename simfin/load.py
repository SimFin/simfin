##########################################################################
#
# Functions for loading financial datasets into Pandas DataFrames.
# The files will be automatically downloaded if they do not exist on disk.
#
##########################################################################
# SimFin - Simple financial data for Python.
# www.simfin.com - www.github.com/simfin/simfin
# See README.md for instructions and LICENSE.txt for license details.
##########################################################################

import pandas as pd
from functools import partial

from simfin.paths import _path_dataset
from simfin.download import _maybe_download_dataset
from simfin.names import TICKER, INDUSTRY_ID, MARKET_ID
from simfin.names import DATE, REPORT_DATE, PUBLISH_DATE, RESTATED_DATE

##########################################################################
# Load function.

def load(dataset, variant=None, market=None,
         parse_dates=None, index=None, refresh_days=30):
    """
    Load the dataset from local disk and return it as a Pandas DataFrame.
    If the dataset does not exist on local disk, or if it is too old, then it
    is automatically downloaded from the SimFin server.

    This is the main function for downloading and loading datasets. It is
    specialized in several so-called partial function definitions below,
    such as :obj:`~simfin.load.load_income` and
    :obj:`~simfin.load.load_shareprices`, which merely set some of the
    arguments in this function for convenience.

    A dataset is specified by its name e.g. 'income' for Income Statements,
    its variant e.g. 'annual' for annual reports, and the market e.g. 'us'
    for USA. All datasets have a name, but only some of them have options
    for variants and markets. For a full list of available datasets see:
    https://simfin.com/data/bulk

    All datasets are saved on disk as CSV-files, where the columns define
    the data-items such as Ticker, Revenue and Net Income, and the rows are
    data-points or records. The number of columns is typically fairly small
    (less than 100) but the number of rows may be thousands or even millions.

    This function can automatically parse and convert columns that contain
    strings with dates into proper date-types. You do this by passing the
    column-names as the argument `parse_dates`.

    This function can also use one or more of the columns as an index for
    the resulting Pandas DataFrame. You do this by passing the column-names
    as the argument `index`. The index will be sorted in ascending order.

    :param dataset:
        String with the name of the dataset (always lowercase).

        Examples:
            - 'income': Income statements.
            - 'balance': Balance sheets.
            - 'cashflow': Cash-flow statements.
            - 'shareprices': Share-prices.
            - 'companies': Company details.
            - 'industries': Sector and industry details.
            - 'markets': Market details.

    :param variant:
        String with the dataset's variant (always lowercase).
        The valid options depend on the dataset.

        Examples for datasets 'income', 'balance', and 'cashflow':
            - 'annual': Annual financial reports.
            - 'quarterly': Quarterly financial reports.
            - 'ttm': Trailing-Twelve-Months (TTM) reports.

        Valid options for dataset 'shareprices':
            - 'latest': Latest share-prices (small data-file).
            - 'daily': Daily share-prices (large data-file).

    :param market:
        String for the dataset's market (always lowercase).

        This is used to group the entire database into smaller sections
        for individual markets such as USA, Germany, etc.

        Examples of valid options:
            - 'us': USA
            - 'de': Germany
            - 'sg': Singapore

        Some datasets such as 'industries' do not support the market-keyword
        and will generate a server-error if the market is set.

    :param parse_dates:
        String or list of strings with column-names that contain dates
        to be parsed. This depends on the dataset.
        For fundamental data it is [REPORT_DATE, PUBLISH_DATE, RESTATED_DATE].
        For shareprices it is [DATE].
        Format is always assumed to be YYYY-MM-DD.

    :param index:
        String or list of strings with column-names that will be used as index.
        The index will automatically be sorted in ascending order.

    :param refresh_days:
        Integer with the number of days before data is downloaded again.

        The data is updated daily on the SimFin server so you would normally
        use refresh_days >= 1. Free datasets are updated less frequently so
        you would normally use refresh_days >= 30 for free datasets.

        A value of refresh_days == 0 means the data is downloaded regardless
        of the age of the data-files saved on disk.

    :return:
        Pandas DataFrame with the data.
    """

    assert dataset is not None

    # Convert dataset name, variant, and market to lower-case.
    dataset = dataset.lower()
    if variant is not None:
        variant = variant.lower()
    if market is not None:
        market = market.lower()

    # Dict with dataset arguments.
    dataset_args = {'dataset': dataset, 'variant': variant, 'market': market}

    # Download file if it does not exist on local disk, or if it is too old.
    _maybe_download_dataset(**dataset_args, refresh_days=refresh_days)

    # Lambda function for converting strings to dates. Format: YYYY-MM-DD
    date_parser = lambda x: pd.to_datetime(x, yearfirst=True, dayfirst=False)

    # Print status message.
    print('- Loading from disk ... ', end='')

    # Full path for the CSV-file on local disk.
    path = _path_dataset(**dataset_args)

    # Load dataset into Pandas DataFrame.
    df = pd.read_csv(path, sep=';', header=0,
                     parse_dates=parse_dates, date_parser=date_parser)

    # Set the index and sort the data.
    if index is not None:
        # Set the index.
        df.set_index(index, inplace=True)

        # Sort the rows of the DataFrame according to the index.
        df.sort_index(ascending=True, inplace=True)

    # Print status message.
    print('Done!')

    return df

##########################################################################
# Specialized functions for loading datasets with fundamental data:
# Income Statements, Balance Sheets and Cash-Flow Statements.

# These are implemented very easily using functools.partial() which sets
# some of the args in the load() function above. These args can still be
# changed when the user calls the specialized functions.

# Common doc-string for all the specialized load-functions.
_DOC_LOAD = ' See the :obj:`~simfin.load.load` function for valid args.'

# Load fundamental data i.e. Income Statements, Balance Sheets, Cash-Flow Stmt.
# This is used by load_income(), load_balance(), load_cashflow(), etc. because
# they all set the same args in load().
load_fundamental = partial(load, market='us', index=[TICKER, REPORT_DATE],
                           parse_dates=[REPORT_DATE, PUBLISH_DATE, RESTATED_DATE])
load_fundamental.__doc__ = 'Load fundamental data such as Income Statements, ' \
                           'Balance Sheets, or Cash-Flow Statements.' + _DOC_LOAD

# Load Income Statements for all companies except banks and insurance companies.
load_income = partial(load_fundamental, dataset='income')
load_income.__doc__ = 'Load Income Statements for all companies except banks ' \
                      'and insurance companies.' + _DOC_LOAD

# Load Income Statements for banks.
load_income_banks = partial(load_fundamental, dataset='income-banks')
load_income_banks.__doc__ = 'Load Income Statements for banks.' + _DOC_LOAD

# Load Income Statements for insurance companies.
load_income_insurance = partial(load_fundamental, dataset='income-insurance')
load_income_insurance.__doc__ = 'Load Income Statements for insurance ' \
                                'companies.' + _DOC_LOAD

# Load Balance Sheets for all companies except banks and insurance companies.
load_balance = partial(load_fundamental, dataset='balance')
load_balance.__doc__ = 'Load Balance Sheets for all companies except banks ' \
                       'and insurance companies.' + _DOC_LOAD

# Load Balance Sheets for banks.
load_balance_banks = partial(load_fundamental, dataset='balance-banks')
load_balance_banks.__doc__ = 'Load Balance Sheets for banks.' + _DOC_LOAD

# Load Balance Sheets for insurance companies.
load_balance_insurance = partial(load_fundamental, dataset='balance-insurance')
load_balance_insurance.__doc__ = 'Load Balance Sheets for insurance companies.' + _DOC_LOAD

# Load Cash-Flow Statements for all companies except banks and insurance companies.
load_cashflow = partial(load_fundamental, dataset='cashflow')
load_cashflow.__doc__ = 'Load Cash-Flow Statements for all companies except ' \
                        'banks and insurance companies.' + _DOC_LOAD

# Load Cash-Flow Statements for banks.
load_cashflow_banks = partial(load_fundamental, dataset='cashflow-banks')
load_cashflow_banks.__doc__ = 'Load Cash-Flow Statements for banks.' + _DOC_LOAD

# Load Cash-Flow Statements for insurance companies.
load_cashflow_insurance = partial(load_fundamental, dataset='cashflow-insurance')
load_cashflow_insurance.__doc__ = 'Load Cash-Flow Statements for insurance ' \
                                  'companies.' + _DOC_LOAD

##########################################################################
# Specialized functions for loading other datasets.

# Load details about companies.
load_companies = partial(load, dataset='companies', market='us', index=TICKER)
load_companies.__doc__ = 'Load details about companies.' + _DOC_LOAD

# Load details about markets.
load_markets = partial(load, dataset='markets', index=MARKET_ID)
load_markets.__doc__ = 'Load details about markets.' + _DOC_LOAD

# Load details about industries and sectors.
load_industries = partial(load, dataset='industries', index=INDUSTRY_ID)
load_industries.__doc__ = 'Load details about industries and sectors.' + _DOC_LOAD

# Load share-prices.
load_shareprices = partial(load, dataset='shareprices', variant='latest', market='us',
                           index=[TICKER, DATE], parse_dates=[DATE])
load_shareprices.__doc__ = 'Load share-prices.' + _DOC_LOAD

##########################################################################
