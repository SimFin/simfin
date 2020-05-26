##########################################################################
#
# Global configuration variables such as API key and data directories.
# Use the set/get functions for correct access to these variables.
#
##########################################################################
# SimFin - Simple financial data for Python.
# www.simfin.com - www.github.com/simfin/simfin
# See README.md for instructions and LICENSE.txt for license details.
##########################################################################

import os

##########################################################################
# API Key.

# The user's API key obtained when registering on www.simfin.com
# The default API key gives access to the free datasets.
_api_key = 'free'


def set_api_key(api_key='free'):
    """
    Set the API key.

    :param api_key: String with the API key.
    :return: `None`
    """
    global _api_key
    _api_key = api_key


def load_api_key(path='~/simfin_api_key.txt', default_key='free'):
    """
    Load the API key from the text-file with the given path.

    :param path:
        String with the path for the text-file.

    :param default_key:
        String with the default key if it could not be loaded from file.

    :return:
        `None`
    """
    try:
        # Expand the path if it begins with ~
        path = os.path.expanduser(path)

        # Read the first line from the file.
        with open(path) as f:
            key = f.readline().strip()
    except:
        # Something went wrong, so use the default API key.
        key = default_key

    # Set the API key.
    set_api_key(api_key=key)


def get_api_key():
    """
    Get the API key.

    :return: String with the API key.
    """
    return _api_key

##########################################################################
# Data directories.

# Directory where the datasets are saved on disk.
_data_dir = None

# Directory where the datasets are downloaded.
_download_dir = None

# Directory where the cached files are saved on disk.
_cache_dir = None

# Directory where info-files are saved on disk.
_info_dir = None


def _check_data_dir():
    """
    Raise an exception if the user has not set the data-directory.
    This is used instead of a really strange Python error-message.
    """
    if _data_dir is None:
        msg = 'The simfin data directory has not been set by the user. ' \
              'Please call the function sf.set_data_dir() first.'
        raise Exception(msg)


def set_data_dir(data_dir='~/simfin_data/'):
    """
    Set the directory where datasets are stored on disk
    and create the directory if it does not exist.

    :param data_dir: String with the directory-name.
    :return: `None`
    """
    global _data_dir, _download_dir, _cache_dir, _info_dir

    # Expand directory if it begins with ~
    _data_dir = os.path.expanduser(data_dir)

    # Directory for download. This is a sub-dir of data_dir.
    _download_dir = os.path.join(_data_dir, 'download/')

    # Directory for cache-files. This is a sub-dir of data_dir.
    _cache_dir = os.path.join(_data_dir, 'cache/')

    # Directory for info-files. This is a sub-dir of data_dir.
    _info_dir = os.path.join(_data_dir, 'info/')

    # Check if download directory exists, otherwise create it.
    # This also creates all parent directories if they don't exist,
    # including the main data_dir.
    if not os.path.exists(_download_dir):
        os.makedirs(_download_dir)

    # Check if cache directory exists, otherwise create it.
    if not os.path.exists(_cache_dir):
        os.makedirs(_cache_dir)

    # Check if info-directory exists, otherwise create it.
    if not os.path.exists(_info_dir):
        os.makedirs(_info_dir)


def get_data_dir():
    """
    Get the full path for the main data-directory where
    datasets are saved on disk.

    :return: String with the path for the data-directory.
    """
    # Ensure the data-directory has been set by the user.
    _check_data_dir()
    return _data_dir


def get_download_dir():
    """
    Get the full path for the download directory where
    the zip-files with datasets are temporarily stored.

    :return: String with the path for the download directory.
    """
    # Ensure the data-directory has been set by the user.
    _check_data_dir()
    return _download_dir


def get_cache_dir():
    """
    Get the full path for the directory where cache-files are saved.

    :return: String with the path for the cache directory.
    """
    # Ensure the data-directory has been set by the user.
    _check_data_dir()
    return _cache_dir


def get_info_dir():
    """
    Get the full path for the directory where info-files are saved.

    :return: String with the path for the info directory.
    """
    # Ensure the data-directory has been set by the user.
    _check_data_dir()
    return _info_dir

##########################################################################
