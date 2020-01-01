##########################################################################
#
# Functions for composing file-paths for storing datasets and info-files.
#
##########################################################################
# SimFin - Simple financial data for Python.
# www.simfin.com - www.github.com/simfin/simfin
# See README.md for instructions and LICENSE.txt for license details.
##########################################################################

import os

from simfin.config import get_data_dir, get_info_dir, get_download_dir

##########################################################################
# Compose filenames.

def _filename_dataset(dataset, market=None, variant=None, extension=None):
    """
    Compose the filename for a dataset given its name, variant, market,
    and filename extension.

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
        filename = '{}-{}'.format(market, dataset)

    # Add variant to filename.
    if variant is not None:
        filename = '{}-{}'.format(filename, variant)

    # Add extension to filename.
    if extension is not None:
        filename = '{}.{}'.format(filename, extension)

    return filename


def _filename_info(name):
    """
    Compose the filename for an info-file given its name.

    :param name: String with name of the info-file.
    :return: String with filename for the info-file.
    """
    return name + '.json'

##########################################################################
# Compose the full paths for where files are stored on disk.

def _path_dataset(**kwargs):
    """
    Compose the full path for a dataset-file on disk.

    :param kwargs: Keyword args for the dataset details.
    :return: String with full path for the dataset-file on disk.
    """
    filename = _filename_dataset(extension='csv', **kwargs)
    path = os.path.join(get_data_dir(), filename)
    return path


def _path_info(name):
    """
    Compose the full path for an info-file on disk.

    :param name: String with name of the info-file e.g. 'datasets'.
    :return: String with full path for the info-file on disk.
    """
    filename = _filename_info(name=name)
    path = os.path.join(get_info_dir(), filename)
    return path

##########################################################################
# Compose the temporary download paths for the files.

def _path_download(filename):
    """
    Compose the full path for the downloaded file.

    :param filename: String with filename e.g. 'us-income-ttm.zip'
    :return: String with full path for the download-file.
    """
    return os.path.join(get_download_dir(), filename)


def _path_download_dataset(**kwargs):
    """
    Compose the full path for the downloaded dataset zip-file.

    :param kwargs: Keyword args for the dataset details.
    :return: String with full path for the downloaded file on disk.
    """
    filename = _filename_dataset(extension='zip', **kwargs)
    return _path_download(filename=filename)


def _path_download_info(name):
    """
    Compose the full path for the downloaded info-file.

    :param name: String with name of the info-file e.g. 'datasets'.
    :return: String with full path for the downloaded file on disk.
    """
    filename = _filename_info(name=name)
    return _path_download(filename=filename)

##########################################################################
