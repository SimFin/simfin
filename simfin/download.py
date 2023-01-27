##########################################################################
#
# Functions for downloading files from the SimFin server.
#
##########################################################################
# SimFin - Simple financial data for Python.
# www.simfin.com - www.github.com/simfin/simfin
# See README.md for instructions and LICENSE.txt for license details.
##########################################################################

import requests
import zipfile
import sys
import os

from simfin.config import get_data_dir, get_api_key
from simfin.exceptions import ServerException
from simfin.paths import _filename_dataset, _path_dataset, _path_download_dataset
from simfin.paths import _path_info, _path_download_info
from simfin.utils import _file_age

##########################################################################

def _url_dataset(dataset, market=None, variant=None):
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
    args = 'dataset=' + dataset

    # Variant.
    if variant is not None:
        args += '&variant=' + variant

    # Market.
    if market is not None:
        args += '&market=' + market

    # API key.
    api_key = get_api_key()
    if api_key is not None:
        args += '&api-key=' + api_key

    # Base URL for the bulk-download API on the SimFin server.
    base_url = 'https://simfin.com/api/bulk?'

    # Combine base URL and arguments.
    url = base_url + args

    return url


def _url_info(name):
    """
    Compose the URL for a json-file with information about the datasets.

    :param name: Name of the information e.g. 'datasets' or 'columns'.
    :return: String with the full URL.
    """

    url = 'https://simfin.com/api/bulk_info/{0}.php'
    url = url.format(name)
    return url

##########################################################################

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
        msg = '\r- Downloading ... {0:.1%}'.format(pct_complete)
    else:
        # Show the progress as number of bytes downloaded,
        # because the total size is unknown.

        # Status-message. Note the \r which means the line should overwrite itself.
        msg = '\r- Downloaded bytes: {0:,}'.format(downloaded_size)

    # Print the status-message.
    sys.stdout.write(msg)
    sys.stdout.flush()

##########################################################################

def _download(url, download_path):
    """
    Download a file from an internet URL and save it to disk.

    The download was a success if the function returns, otherwise an
    exception is raised.

    :param url:
        Internet URL.

    :param download_path:
        Full path to the destination file where the downloaded contents are
        saved. The file will be overwritten if it already exists. Data is
        saved in binary format.

    :raises ServerException:
        If the server returned an error.

    :raises HTTPError:
        If some other HTTP error occurred.
    """

    # Open a streaming connection to the server.
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

        # Or if the server returned an error.
        elif status_code == 400:
            # Get the error message reported by the server.
            error = response.json()['error']

            # Raise exception with the error message from the server.
            raise ServerException(error)

        # Or if another error occurred.
        else:
            # Raise the error as an exception.
            response.raise_for_status()

##########################################################################

def _maybe_download(name, url, path, download_path, refresh_days):
    """
    Check if the file in `path` exists on disk or if it is too old, and then
    download the file from `url` and save it to disk.

    If the downloaded file is a zip-file then its contents will be extracted
    to the data-dir, otherwise it is just moved there directly. This should
    ensure the download is complete before it overwrites the old files.

    :param name:
        Name of the dataset to print in status-message.

    :param url:
        Internet URL where the file will be downloaded from.

    :param path:
        Full path for a file on disk whose existence and age is used to decide
        whether the file must be downloaded again.

    :param download_path:
        Full path where the downloaded file will be temporarily saved on disk.

    :param refresh_days:
        Integer with the number of days before data is downloaded again.
        Compare this to the age of the file given in `path`.

        A value of refresh_days == 0 means the data is downloaded regardless
        of the age of the data-file saved on disk.

    :return:
        True if data was downloaded, False otherwise.
    """

    # Determine if the file must be downloaded.
    if os.path.exists(path):
        # File's age in days.
        file_age_days = _file_age(path).days

        # Boolean whether to download the file again, if it is too old.
        must_download = (file_age_days >= refresh_days)

        # Status message.
        msg = 'Dataset \"{}\" on disk ({} days old).'
        msg = msg.format(name, file_age_days)

    else:
        # File does not exist on local disk, so we must download it.
        must_download = True

        # Status message.
        msg = 'Dataset \"{}\" not on disk.'
        msg = msg.format(name)

    # File must always be downloaded regardless of its age.
    if refresh_days == 0:
        must_download = True

    # Print status message.
    print(msg)

    if must_download:
        # Download the file from the SimFin server.
        # This is assumed to succeed unless an exception is raised.
        _download(url=url, download_path=download_path)

        if download_path.endswith('zip'):
            # Downloaded file must be unzipped into the data-dir.

            # Print status message.
            print('\n- Extracting zip-file ... ', end='')

            # Unpack the zip-file to the data_dir.
            zipfile.ZipFile(file=download_path, mode='r').extractall(get_data_dir())

            # Print status message.
            print('Done!')
        else:
            # Downloaded file will just be moved to the destination path.

            # Print status message.
            print('\n- Moving file to data-dir ... ', end='')

            # Move and replace the file if it already exists.
            os.replace(download_path, path)

            # Print status message.
            print('Done!')

    # Return boolean whether the file was downloaded or not.
    return must_download

##########################################################################

def _maybe_download_dataset(refresh_days, **kwargs):
    """
    Check if the given dataset is already on disk and how old it is,
    and download again from the SimFin server if it needs to be refreshed.

    :param kwargs: Keyword args for the dataset details.
    :param refresh_days: Integer with number of days before refreshing data.
    :return: Boolean whether data was downloaded (True) or not (False).
    """

    # Name of the dataset, this is just the filename without an extension.
    dataset_name = _filename_dataset(**kwargs, extension=None)

    # Full path for the local data-file.
    path = _path_dataset(**kwargs)

    # Full path for the downloaded file.
    download_path = _path_download_dataset(**kwargs)

    # URL to SimFin's server where the file is located.
    url = _url_dataset(**kwargs)

    return _maybe_download(name=dataset_name, path=path,
                           download_path=download_path,
                           url=url, refresh_days=refresh_days)

##########################################################################

def _maybe_download_info(name, refresh_days):
    """
    Check if the given info-file is already on disk and how old it is,
    and download again from the SimFin server if it needs to be refreshed.

    :param name: Name of the info-file.
    :param refresh_days: Integer with number of days before refreshing data.
    :return: Boolean whether data was downloaded (True) or not (False).
    """

    # Full path for the local data-file.
    path = _path_info(name=name)

    # Full path for the downloaded file.
    download_path = _path_download_info(name=name)

    # URL to SimFin's server where the file is located.
    url = _url_info(name=name)

    return _maybe_download(name=name, path=path,
                           download_path=download_path,
                           url=url, refresh_days=refresh_days)

##########################################################################
