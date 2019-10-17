##########################################################################
#
# Functions for automatic downloading of bulk CSV-files from the SimFin
# server and loading the CSV-files as Pandas DataFrames.
#
##########################################################################
# SimFin - Simple financial data for Python.
# www.simfin.com - www.github.com/simfin/simfin
# See README.md for instructions and LICENSE.txt for license details.
##########################################################################

from simfin.config import get_data_dir, get_download_dir, get_api_key
from simfin.names import TICKER, DATE, REPORT_DATE, PUBLISH_DATE, INDUSTRY_ID
from simfin.names import MARKET_ID
from simfin.exceptions import ServerException

import pandas as pd
import zipfile
import requests
import sys
import os
import time

from functools import partial
from datetime import timedelta

##########################################################################
# Helper functions.

def _compose_filename(dataset, market=None, variant=None, extension=None):
    """
    Compose the filename for a dataset-file, given the
    dataset's name, variant, market, and filename extension.

    :param dataset: String with dataset name e.g. 'income'.
    :param market: Optional string with dataset market e.g. 'usa'.
    :param variant: Optional string with dataset variant e.g. 'ttm'.
    :param extension: Optional string with filename extension e.g. 'zip' or 'csv'.
    :return: String with filename for the dataset-file.
    """

    assert dataset is not None

    # Compose filename from market and dataset.
    if market is None:
        filename = dataset
    else:
        filename = "{}-{}".format(market, dataset)

    # Add variant to filename.
    if variant is not None:
        filename = "{}-{}".format(filename, variant)

    # Add extension to filename.
    if extension is not None:
        filename = "{}.{}".format(filename, extension)

    return filename


def _compose_path(*args, **kwargs):
    """
    Compose the full path for a dataset CSV-file on disk.

    :param market: String with dataset market e.g. 'usa'.
    :param dataset: String with dataset name e.g. 'income'.
    :param variant: Optional string with dataset variant e.g. 'ttm'.
    :return: String with full path for the dataset-file on disk.
    """

    # Compose the filename.
    filename = _compose_filename(extension='csv', *args, **kwargs)

    # Compose the full path.
    path = os.path.join(get_data_dir(), filename)

    return path


def _compose_download_path(*args, **kwargs):
    """
    Compose the full path for the downloaded dataset zip-file.

    :param market: String with dataset market e.g. 'usa'.
    :param dataset: String with dataset name e.g. 'income'.
    :param variant: Optional string with dataset variant e.g. 'ttm'.
    :return: String with full path for the dataset-file on disk.
    """

    # Compose the filename.
    filename = _compose_filename(extension="zip", *args, **kwargs)

    # Compose the full path.
    path = os.path.join(get_download_dir(), filename)

    return path


def _compose_url(dataset, market=None, variant=None):
    """
    Compose the URL for a dataset on the SimFin server.

    :param dataset: String with dataset name e.g. 'income'.
    :param variant: Optional string with dataset variant e.g. 'ttm'.
    :param market: String with dataset market e.g. 'usa'.
    :return: String with the full URL.
    """

    assert dataset is not None

    # Create string with the arguments.

    # Dataset.
    args = "dataset=" + dataset

    # Variant.
    if variant is not None:
        args += "&variant=" + variant

    # Market.
    if market is not None:
        args += "&market=" + market

    # API key.
    api_key = get_api_key()
    if api_key is not None:
        args += "&api-key=" + api_key

    # Base URL for the bulk-download API on the SimFin server.
    base_url = "https://simfin.com/api/bulk?"

    # Combine base URL and arguments.
    url = base_url + args

    return url


##########################################################################
# Download functions.


def _print_download_progress(downloaded_size, total_size):
    """
    Print the download progress.

    :param downloaded_size: Number of bytes downloaded so far.
    :param total_size: Total number of bytes to download.
    :return: None
    """

    if total_size > 0:
        # Show the progress as percentage completion.

        # Percentage completion.
        pct_complete = downloaded_size / total_size

        # Limit it because rounding errors may cause it to exceed 100%.
        pct_complete = min(1.0, pct_complete)

        # Status-message. Note the \r which means the line should overwrite itself.
        msg = '\r- Download progress: {0:.1%}'.format(pct_complete)
    else:
        # Show the progress as number of bytes downloaded,
        # because the total size is unknown.

        # Status-message. Note the \r which means the line should overwrite itself.
        msg = '\r- Downloaded bytes: {0:,}'.format(downloaded_size)

    # Print the status-message.
    sys.stdout.write(msg)
    sys.stdout.flush()


def _download(*args, **kwargs):
    """
    Download a dataset from the SimFin server.

    Accepts the same args as the function _compose_url().

    :return: String with full path for the downloaded file.
    :raises ServerException: If SimFin server returned an error.
    :raises HTTPError: If some other HTTP error occurred.
    """

    # URL to SimFin's server where the file is located.
    url = _compose_url(*args, **kwargs)

    # Local path for the downloaded file.
    download_path = _compose_download_path(*args, **kwargs)

    # Open a streaming connection to the SimFin server.
    with requests.get(url, stream=True) as response:
        # Get the status code for the connection.
        status_code = response.status_code

        # If connection is OK then download the file.
        if status_code == 200:
            # Total number of bytes to be downloaded.
            total_size = int(response.headers.get('content-length', default=0))

            # Number of bytes downloaded so far.
            downloaded_size = 0

            # Create local file and copy data from the server.
            with open(download_path, 'wb') as file:
                # Read the data in chunks from the server.
                # The chunk_size is set automatically if None,
                # but this can result in large files being downloaded
                # as one big chunk, so the progress is not shown.
                for chunk in response.iter_content(chunk_size=16384):
                    # Write the chunk to file.
                    file.write(chunk)

                    # Increase the number of bytes downloaded.
                    downloaded_size += len(chunk)

                    # Print download progress.
                    _print_download_progress(downloaded_size, total_size)

        # Or if the SimFin server returned an error.
        elif status_code == 400:
            # Get the error message reported by the SimFin server.
            error = response.json()['error']

            # Raise exception with the error message from the SimFin server.
            raise ServerException(error)

        # Or if another error occurred.
        else:
            # Raise the error as an exception.
            response.raise_for_status()

    return download_path


def _maybe_download(refresh_days, *args, **kwargs):
    """
    If the given dataset does not exist on disk or if it is too old, then
    download the new dataset from the SimFin server and save it to disk.

    Accepts the same args as the function _compose_url().

    :param refresh_days:
        Integer with the number of days before data is downloaded again.

        The data is updated daily on the SimFin server so you would normally
        use refresh_days >= 1. Free datasets are updated less frequently so
        you would normally use refresh_days >= 30 for free datasets.

        A value of refresh_days == 0 means the data is downloaded regardless
        of the age of the data-files saved on disk. This is mainly useful for
        the automated data-testing done by SimFin's own administrators.

    :return:
        True if data was downloaded, False otherwise.
    """

    # Name of the dataset.
    dataset_name = _compose_filename(*args, **kwargs)

    # Full path for the local data-file.
    path = _compose_path(*args, **kwargs)

    # Determine if the file must be downloaded.
    if refresh_days == 0:
        # File must always be downloaded.
        download = True

        # Status message.
        msg = 'Dataset \"{}\" downloading ... '
        msg = msg.format(dataset_name)

    elif os.path.exists(path):
        # If the file exists on local disk, then check its date.

        # Last time the file was modified.
        file_timestamp = os.path.getmtime(path)

        # Difference between now and when the file was last modified.
        time_dif = time.time() - file_timestamp
        time_dif = timedelta(seconds=int(round(time_dif)))

        # Download the file again, if it is too old.
        download = (time_dif.days >= refresh_days)

        # status message.
        if download:
            msg = 'Dataset \"{}\" on disk ({} days old), downloading new ...'
            msg = msg.format(dataset_name, time_dif.days)
        else:
            msg = 'Dataset \"{}\" on disk ({} days old), loading.'
            msg = msg.format(dataset_name, time_dif.days)

    else:
        # File does not exist on local disk, so we must download it.
        download = True

        # Status message.
        msg = 'Dataset \"{}\" not on disk, downloading ...'
        msg = msg.format(dataset_name)

    # Print status message.
    print(msg)

    if download:
        # Download the file from the SimFin server.
        download_path = _download(*args, **kwargs)

        # Print status message.
        print('\n- Extracting zip-file: ', end="")

        # Unpack the zip-file to the data_dir.
        zipfile.ZipFile(file=download_path, mode="r").extractall(get_data_dir())

        # Print status message.
        print('Done!')

    # Return boolean whether the file was downloaded or not.
    return download

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
    such as load_income() and load_shareprices(), which merely set some of
    the arguments in this function for convenience.

    A dataset is specified by its name e.g. 'income' for Income Statements,
    its variant e.g. 'annual' for annual reports, and the market e.g. 'us'
    for USA. All datasets have a name, but only some of them have options
    for variants and markets. For a full list of available datasets see:
    ??? link to simfin website with definition of all datasets, variants, etc.

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
            'income': Income statements.
            'balance': Balance sheets.
            'cashflow': Cash-flow statements.
            'shareprices': Share-prices.
            'companies': Company details.
            'industries': Sector and industry details.
            'markets': Market details.

    :param variant:
        String with the dataset's variant (always lowercase).
        The valid options depends on the dataset.

        Examples for datasets 'income', 'balance', and 'cashflow':
            'annual': Annual financial reports.
            'quarterly': Quarterly financial reports.
            'ttm': Trailing-Twelve-Months (TTM) reports.

        Valid options for dataset 'shareprices':
            'latest': Latest share-prices (small data-file).
            'daily': Daily share-prices (large data-file).

    :param market:
        String for the dataset's market (always lowercase).

        This is used to group the entire database into smaller sections
        for individual markets such as USA, Germany, etc.

        Examples of valid options:
            'us': USA
            'de': Germany
            'sg': Singapore

        Some datasets such as 'industries' do not support the market-keyword
        and will generate a server-error if the market is set.

    :param parse_dates:
        String or list of strings with column-names that contain dates
        to be parsed. This depends on the dataset.
        For fundamental data it is [REPORT_DATE, PUBLISH_DATE].
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
        of the age of the data-files saved on disk. This is mainly useful for
        the automated data-testing done by SimFin's own administrators.

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

    # Download file if it does not exist on local disk, or if it is too old.
    _maybe_download(dataset=dataset, variant=variant, market=market,
                    refresh_days=refresh_days)

    # Full path for the CSV-file on disk.
    path = _compose_path(dataset=dataset, variant=variant, market=market)

    # Lambda function for converting strings to dates. Format: YYYY-MM-DD
    date_parser = lambda x: pd.to_datetime(x, yearfirst=True, dayfirst=False)

    # Load dataset into Pandas DataFrame.
    df = pd.read_csv(path, sep=';', header=0,
                     parse_dates=parse_dates, date_parser=date_parser)

    # Set the index and sort the data.
    if index is not None:
        # Set the index.
        df.set_index(index, inplace=True)

        # Sort the rows of the DataFrame according to the index.
        df.sort_index(ascending=True, inplace=True)

    return df

##########################################################################
# Specialized functions for loading datasets with fundamental data:
# Income Statements, Balance Sheets and Cash-Flow Statements.

# These are implemented very easily using functools.partial() which sets
# some of the args in the load() function above. These args can still be
# changed when the user calls the specialized functions.

# Common doc-string for all the specialized load-functions.
_DOC_LOAD = ' See simfin.load() for valid args.'

# Load fundamental data i.e. Income Statements, Balance Sheets, Cash-Flow Stmt.
# This is used by load_income(), load_balance(), load_cashflow(), etc. because
# they all set the same args in load().
load_fundamental = partial(load, market='us', index=[TICKER, REPORT_DATE],
                           parse_dates=[REPORT_DATE, PUBLISH_DATE])
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
