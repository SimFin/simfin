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
from simfin.exceptions import ServerException

import pandas as pd
import zipfile
import requests
import sys
import os
import time
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
        filename = "{}-{}".format(market.lower(), dataset.lower())

    # Add variant to filename.
    if variant is not None:
        filename = "{}-{}".format(filename, variant.lower())

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
        msg = "\r- Download progress: {0:.1%}".format(pct_complete)
    else:
        # Show the progress as number of bytes downloaded,
        # because the total size is unknown.

        # Status-message. Note the \r which means the line should overwrite itself.
        msg = "\r- Downloaded bytes: {0:,}".format(downloaded_size)

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
    with requests.get(url, stream=True) as r:
        # Get the status code for the connection.
        status_code = r.status_code

        # If connection is OK then download the file.
        if status_code == 200:
            # Total number of bytes to be downloaded.
            total_size = int(r.headers.get('content-length', default=0))

            # Number of bytes downloaded so far.
            downloaded_size = 0

            # Create local file and copy data from the server.
            with open(download_path, 'wb') as file:
                # Read the data in chunks from the server.
                # The chunk_size is set automatically when None.
                for chunk in r.iter_content(chunk_size=None):
                    # Write the chunk to file.
                    file.write(chunk)

                    # Increase the number of bytes downloaded.
                    downloaded_size += len(chunk)

                    # Print download progress.
                    _print_download_progress(downloaded_size, total_size)

        # Or if the SimFin server returned an error.
        elif status_code == 400:
            # Get the error message reported by the SimFin server.
            error = r.json()['error']

            # Raise exception with the error message from the SimFin server.
            raise ServerException(error)

        # Or if another error occurred.
        else:
            # Raise the error as an exception.
            r.raise_for_status()

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
        msg = "Dataset \"{}\" is being downloaded ... "
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
            msg = "Dataset \"{}\" on disk is {} days old, downloading new file ... "
            msg = msg.format(dataset_name, time_dif.days)
        else:
            msg = "Loading \"{}\" from disk ({} days old)."
            msg = msg.format(dataset_name, time_dif.days)

    else:
        # File does not exist on local disk, so we must download it.
        download = True

        # Status message.
        msg = "Dataset \"{}\" does not exist on disk, downloading ... "
        msg = msg.format(dataset_name)

    # Print status message.
    print(msg)

    if download:
        # Download the file from the SimFin server.
        download_path = _download(*args, **kwargs)

        # Print status message.
        print("\n- Extracting zip-file: ", end="")

        # Unpack the zip-file to the data_dir.
        zipfile.ZipFile(file=download_path, mode="r").extractall(get_data_dir())

        # Print status message.
        print("Done!")

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

    :param dataset:
        String with the name of the dataset. Examples:
            'income': Income statements.
            'balance': Balance sheets.
            'cashflow': Cash-flow statements.
            'shareprices': Share-prices.
            'companies': Company details.
            'industries': Sector and industry details.

        Complete list of datasets:
        link ???

    :param variant:
        String with the dataset variant. Valid options depends on the dataset.
        Valid options for fundamental data:
            'annual': Annual financial reports.
            'quarterly': Quarterly financial reports.
            'ttm': Trailing-Twelve-Months (TTM) reports.

        Valid options for shareprices:
            'daily': Daily share-prices.

    :param market:
        String for the market e.g. 'USA' or 'UK'.

        Currently not supported on the SimFin server and should be set to None.

    :param parse_dates:
        String or list of strings with column-names that contain dates
        to be parsed. This depends on the dataset.
        For fundamental data it is [REPORT_DATE, PUBLISH_DATE].
        For shareprices it is [DATE].
        Format is always assumed to be YYYY-MM-DD.

    :param index:
        String or list of strings with column-names that will be used as index.

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
# Wrapper-functions for loading different datasets.

def load_fundamental(index=REPORT_DATE, *args, **kwargs):
    """
    Load fundamental financial data such as Income Statements, Balance Sheets,
    or Cash-Flow Statements. This is a simple wrapper for the load() function,
    which has a complete description of the valid parameters.

    This wrapper just ensures that the DataFrame is indexed by TICKER and
    either REPORT_DATE or PUBLISH_DATE, and that those dates are also parsed.

    :param index:
        Column-name to use for the date-index: REPORT_DATE or PUBLISH_DATE.

    :return:
        Pandas DataFrame with the data.
    """
    return load(index=[TICKER, index],
                parse_dates=[REPORT_DATE, PUBLISH_DATE],
                *args, **kwargs)


def load_income(variant='ttm', index=REPORT_DATE, *args, **kwargs):
    """
    Load Income Statements. This is a simple wrapper for the load() function,
    which just ensures that the DataFrame is indexed by TICKER and either
    REPORT_DATE or PUBLISH_DATE, and that those dates are also parsed.

    :param variant:
        String with the dataset variant. Valid options:
            'annual': Annual financial reports.
            'quarterly': Quarterly financial reports.
            'ttm': Trailing-Twelve-Months (TTM) reports.

    :param index:
        Column-name to use for the date-index: REPORT_DATE or PUBLISH_DATE.

    :return:
        Pandas DataFrame with the data.
    """
    return load_fundamental(dataset='income', variant=variant,
                            index=index, *args, **kwargs)


def load_balance(variant='ttm', index=REPORT_DATE, *args, **kwargs):
    """
    Load Balance Sheets. This is a simple wrapper for the load() function,
    which just ensures that the DataFrame is indexed by TICKER and either
    REPORT_DATE or PUBLISH_DATE, and that those dates are also parsed.

    :param variant:
        String with the dataset variant. Valid options:
            'annual': Annual financial reports.
            'quarterly': Quarterly financial reports.
            'ttm': Trailing-Twelve-Months (TTM) reports.

    :param index:
        Column-name to use for the date-index: REPORT_DATE or PUBLISH_DATE.

    :return:
        Pandas DataFrame with the data.
    """
    return load_fundamental(dataset='balance', variant=variant,
                            index=index, *args, **kwargs)


def load_cashflow(variant='ttm', index=REPORT_DATE, *args, **kwargs):
    """
    Load Cash-Flow Statements. This is a simple wrapper for the load() function,
    which just ensures that the DataFrame is indexed by TICKER and either
    REPORT_DATE or PUBLISH_DATE, and that those dates are also parsed.

    :param variant:
        String with the dataset variant. Valid options:
            'annual': Annual financial reports.
            'quarterly': Quarterly financial reports.
            'ttm': Trailing-Twelve-Months (TTM) reports.

    :param index:
        Column-name to use for the date-index: REPORT_DATE or PUBLISH_DATE.

    :return:
        Pandas DataFrame with the data.
    """
    return load_fundamental(dataset='cashflow', variant=variant,
                            index=index, *args, **kwargs)


def load_companies(index=TICKER, *args, **kwargs):
    """
    Load details about companies.
    This is a simple wrapper for the load() function.

    :param index:
        Column-name to use for the index: TICKER or SIMFIN_ID.

    :return:
        Pandas DataFrame with the data.
    """
    return load(dataset='companies', index=index, *args, **kwargs)


def load_industries(*args, **kwargs):
    """
    Load details about industries and sectors.
    This is a simple wrapper for the load() function.

    :return:
        Pandas DataFrame with the data.
    """
    return load(dataset='industries', index=INDUSTRY_ID, *args, **kwargs)


def load_shareprices(variant='daily', *args, **kwargs):
    """
    Load all share-prices. This is a simple wrapper for the load() function.

    :param variant:
        String with the dataset variant. Valid options:
            'daily': Daily share-prices.

    :return:
        Pandas DataFrame with the data.
    """
    return load(dataset='shareprices', variant=variant,
                index=[TICKER, DATE], parse_dates=[DATE],
                *args, **kwargs)

##########################################################################
