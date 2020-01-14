##########################################################################
#
# Functions for loading info-files as Python dicts, which contain meta-data
# about the contents of the financial datasets and their columns.
# The files will be automatically downloaded if they do not exist on disk.
#
##########################################################################
# SimFin - Simple financial data for Python.
# www.simfin.com - www.github.com/simfin/simfin
# See README.md for instructions and LICENSE.txt for license details.
##########################################################################

import json
from functools import partial, lru_cache

from simfin.download import _maybe_download_info
from simfin.paths import _path_info

##########################################################################

@lru_cache()
def load_info(name, refresh_days=30):
    """
    Load information / meta-data about the financial datasets. This data is
    very rarely updated on the server.

    This function uses the `@lru_cache` wrapper to keep the data in a
    RAM-cache, so it can be returned nearly instantly the second time this
    function is called. You should **NOT** modify the data returned by this
    function, because then it would modify the contents of the RAM-cache.
    You first need to make a copy of the data if you want to modify it.

    :param name:
        String with the name of the info-data to load. Valid options:

        - 'datasets': Load info about all available datasets.
        - 'columns': Load info about all available data-columns.

    :param refresh_days:
        Integer with the number of days before the data is downloaded again.
        Note that the info-data is updated very rarely on the SimFin server.

    :return:
        Python dict.
    """

    assert name is not None

    # Convert name to lower-case.
    name = name.lower()

    # Download file if it does not exist on local disk, or if it is too old.
    _maybe_download_info(name=name, refresh_days=refresh_days)

    # Full path for the local data-file.
    path = _path_info(name=name)

    # Print status message.
    print('- Loading from disk ... ', end='')

    # Load the json-file from disk.
    with open(path) as file:
        data = json.load(file)

    # Print status message.
    print('Done!')

    return data

##########################################################################
# Specialized functions for loading the different info-files.

# Load info about all available datasets.
load_info_datasets = partial(load_info, name='datasets')
load_info_datasets.__doc__ = 'Load info about all available datasets.'

# Load info about all available columns for the datasets.
load_info_columns = partial(load_info, name='columns')
load_info_columns.__doc__ = 'Load info about all the available data-columns.'

##########################################################################
