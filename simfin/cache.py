##########################################################################
#
# Wrapper / decorator for caching the results of slow functions that
# return Pandas DataFrames.
#
##########################################################################
# SimFin - Simple financial data for Python.
# www.simfin.com - www.github.com/simfin/simfin
# See README.md for instructions and LICENSE.txt for license details.
##########################################################################

import pandas as pd
import os
from functools import wraps

from simfin.config import get_cache_dir
from simfin.utils import file_age

##########################################################################
# Private helper-functions.

def _compose_path(func, cache_name, cache_format):
    """
    Compose the filename and full path for the cache-file.

    :param func: The function wrapped by @cache.
    :param cache_name: String with the cache-name.
    :param cache_format: String with the cache-format.
    :return: Tuple: (String with the filename, String with the full path).
    """
    # We have already asserted that the cache_format is valid.

    # File-extension.
    extension = '.' + cache_format

    # Compose name and full path of the cache-file.
    filename = func.__name__ + '-' + cache_name + extension
    path = os.path.join(get_cache_dir(), filename)

    return filename, path


def _write_cache(df, path, cache_format):
    """
    Save the DataFrame to the cache-file on disk using the given format.

    :param df: Pandas DataFrame to be cached to disk.
    :param path: Full path for the cache-file.
    :param cache_format: String with the cache-format.
    :return: None
    """
    # We have already asserted that the cache_format is valid.

    if cache_format.startswith('pickle'):
        df.to_pickle(path)
    elif cache_format == 'parquet':
        df.to_parquet(path)
    elif cache_format == 'feather':
        df.to_feather(path)


def _read_cache(path, cache_format):
    """
    Read a DataFrame from the cache-file on disk using the given format.

    :param path: Full path for the cache-file.
    :param cache_format: String with the cache-format.
    :return: Pandas DataFrame.
    """
    # We have already asserted that the cache_format is valid.

    if cache_format.startswith('pickle'):
        df_result = pd.read_pickle(path)
    elif cache_format == 'parquet':
        df_result = pd.read_parquet(path)
    elif cache_format == 'feather':
        df_result = pd.read_feather(path)

    return df_result

##########################################################################

def cache(func):
    """
    Wrapper / decorator for a function that returns a Pandas DataFrame.
    The result of the function is a Pandas DataFrame which is cached to a
    file on disk, so the next time you call the function, it first checks if
    the cache-file exists and is recent, in which case it loads the cache-file,
    otherwise the wrapped function is called and the result is saved to the
    cache-file on disk for the next time the function is called.

    This is used e.g. in the signal-functions because they can take several
    minutes to compute, while it only takes a second to load a cache-file.

    By default the cache-files are saved in the binary and uncompressed
    pickle-format, which is very fast but can create quite large files.
    It is also possible to save the cache-files as compressed pickle-files,
    which trades computation time for disk-space. Other file-formats such
    as Parquet and Feather are also supported, but they put several
    restrictions on the Pandas DataFrames, so those formats are mainly
    useful for sharing DataFrames with others.

    :param func:
        Function which does the actual computation and returns a DataFrame.

    :return:
        The function `func` wrapped with the cache functionality.
    """

    @wraps(func)
    def wrapper(cache_name=None, cache_refresh_days=1,
                cache_format='pickle', **kwargs):
        """
        This uses more advanced Python features to wrap `func` using a
        function-decorator, which are not explained so well in the
        official Python documentation.

        A good video tutorial explaining how this works is found here:
        https://www.youtube.com/watch?v=KlBPCzcQNU8

        Because we are using @wraps the original function name and doc-string
        is kept in the wrapped / decorated function. So you may want to copy
        the following doc-strings for the parameters into the doc-string of the
        function you have wrapped with @cache.

        :param cache_name:
            String with the name of the cache-file. The full filename is the
            function's name + `cache_name` + '.' + `cache_format`
            If `cache_name=None` then the cache-file is never used and the
            function is always called as normal.

        :param cache_refresh_days:
            Integer with the number of days for the cache-file before the
            function is called again and the cache-file is refreshed. Setting
            `cache_refresh_days=0` ignores the age of the cache-file and calls
            the function again to refresh the cache-file.

        :param cache_format:
            String with the format of the cache-file. Default is 'pickle' which
            is very fast but creates large, uncompressed files. Compression can
            be enabled with the option 'pickle.gz' which is slightly slower.

            Other valid options are: 'parquet' and 'feather' which put several
            restrictions on the DataFrames, and are mainly useful for sharing
            the DataFrames with others.

        :param kwargs:
            Additional keyword arguments to pass to the wrapped function.

        :return:
            Pandas DataFrame with either the contents of the cache-file,
            or the results from computing the wrapped function.
        """

        if cache_name is None:
            # Never use the cache, always just compute the function.
            df_result = func(**kwargs)
        else:
            # Ensure the cache-format is a valid string.
            assert cache_format.startswith('pickle') or \
                   cache_format in ['parquet', 'feather']

            # Compose the filename and full path for the cache-file.
            filename, path = _compose_path(func=func,
                                           cache_name=cache_name,
                                           cache_format=cache_format)

            # Does cache-file exist on disk?
            if os.path.exists(path):
                # Cache-file exists on disk, so get its age in days.
                file_age_days = file_age(path).days

                # Print status.
                msg = 'Cache-file \'{0}\' on disk ({1} days old).'
                msg = msg.format(filename, file_age_days)
                print(msg)

                # Is cache-file too old so we need to recompute the function?
                compute = (cache_refresh_days == 0) or \
                          (file_age_days > cache_refresh_days)

                if not compute:
                    # Cache-file is not too old, so load it.
                    print('- Loading cache-file from disk ... ', end='')
                    df_result = _read_cache(path=path, cache_format=cache_format)
                    print('Done!')
            else:
                # Cache-file does not exist, so we must compute the function.
                compute = True

                # Print status.
                msg = 'Cache-file \'{0}\' not on disk.'
                msg = msg.format(filename)
                print(msg)

            # Should we compute the function?
            if compute:
                # Print status.
                msg = '- Running function {0}() ... '
                msg = msg.format(func.__name__)
                print(msg, end='')

                # Compute the actual function.
                df_result = func(**kwargs)

                # Print status.
                print('Done!')

                # Save the resulting Pandas DataFrame to the cache-file.
                print('- Saving cache-file to disk ... ', end='')
                _write_cache(df=df_result, path=path, cache_format=cache_format)
                print('Done!')

        return df_result

    return wrapper

##########################################################################
