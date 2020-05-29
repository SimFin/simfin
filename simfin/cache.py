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
from simfin.utils import _file_age, _is_file_older, _is_str_or_list_str

##########################################################################
# Private helper-functions.

def _compose_cache_path(func, cache_name, cache_format):
    """
    Compose the filename and full path for the cache-file.

    :param func: The function wrapped by @cache.
    :param cache_name: String with the cache-name.
    :param cache_format: String with the cache-format.
    :return: Tuple: (String with the filename, String with the full path).
    """
    # We have already asserted that the cache_format is valid.

    # Compose filename of the cache-file.
    filename = func.__name__
    if cache_name is not None:
        filename += '-' + cache_name
    filename += '.' + cache_format

    # Compose full path of the cache-file.
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
    Wrapper / decorator for a function that returns a Pandas DataFrame. The
    wrapper saves the DataFrame to a file on disk, so the next time you call
    the wrapped function, it first checks if the cache-file exists and is
    recent, in which case it loads the cache-file, otherwise the wrapped
    function is called and the result is saved to the cache-file on disk for
    the next time the function is called.

    This is used e.g. in the signal-functions because they can take several
    minutes to compute, while it only takes a second to load a cache-file.

    .. warning:: You **MUST** use keyword arguments when calling the wrapped
        function, otherwise the first unnamed arguments would get passed to
        this `cache` wrapper instead.

    The following arguments are added to the wrapped function:

    - `cache_name`:
        String with the name of the cache-file. The full filename is the
        function's name + '-' + `cache_name` + '.' + `cache_format`

    - `cache_refresh`:
        Determines if `func` should be called and the results saved to the
        cache-file. Different conditions are supported, depending on the
        type and value of this argument:

        - If `None` then the cache-file is never used and `func` is always
          called as normal.
        - If `True` then `func` is called and the cache-file refreshed.
        - If `False` the cache-file is always used, unless it does not
          exist, in which case `func` is called and the cache-file saved.
        - If an integer which is lower than the cache-file's age in days,
          then `func` is called and the cache-file is refreshed. The cache
          is also refreshed if the integer is 0 (zero).
        - If a string or list of strings, these are considered file-paths
          e.g. for dataset-files. If the cache-file is older than any one
          of those files, then `func` is called and the cache-file is
          refreshed.

    - `cache_format`:
        String with the format of the cache-file. Default is 'pickle' which
        is very fast but creates large, uncompressed files. Compression can
        be enabled with the option 'pickle.gz' which is slightly slower.

        Other valid options are: 'parquet' and 'feather' which put several
        restrictions on the DataFrames, and are mainly useful for sharing
        the DataFrames with others.

    The following are the normal arguments for this function:

    :param func:
        Function which does the actual computation and returns a DataFrame.

    :return:
        The function `func` wrapped with the cache functionality.
    """

    @wraps(func)
    def wrapper(cache_name=None, cache_refresh=None,
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
        function you have wrapped with `@cache`.

        :param cache_name:
            String with the name of the cache-file. The full filename is the
            function's name + '-' + `cache_name` + '.' + `cache_format`

        :param cache_refresh:
            Determines if `func` should be called and the results saved to the
            cache-file. Different conditions are supported, depending on the
            type and value of this argument:

            - If `None` then the cache-file is never used and `func` is always
              called as normal.
            - If `True` then `func` is called and the cache-file refreshed.
            - If `False` the cache-file is always used, unless it does not
              exist, in which case `func` is called and the cache-file saved.
            - If an integer which is lower than the cache-file's age in days,
              then `func` is called and the cache-file is refreshed. The cache
              is also refreshed if the integer is 0 (zero).
            - If a string or list of strings, these are considered file-paths
              e.g. for dataset-files. If the cache-file is older than any one
              of those files, then `func` is called and the cache-file is
              refreshed.

        :param cache_format:
            String with the format of the cache-file. Default is 'pickle' which
            is very fast but creates large, uncompressed files. Compression can
            be enabled with the option 'pickle.gz' which is slightly slower.

            Other valid options are: 'parquet' and 'feather' which put several
            restrictions on the DataFrames, and are mainly useful for sharing
            the DataFrames with others. Note that you need to manually install
            the `pyarrow` package if you want to use these options.

        :param kwargs:
            Additional keyword arguments to pass to the wrapped function.

        :return:
            Pandas DataFrame with either the contents of the cache-file,
            or the results from computing the wrapped function.
        """

        if cache_refresh is None:
            # Never use the cache, always just compute the function.
            df_result = func(**kwargs)
        else:
            # We want to use a cache-file. Determine if it should be refreshed.

            # Ensure the cache-format is a valid string.
            assert cache_format.startswith('pickle') or \
                   cache_format in ['parquet', 'feather']

            # Compose the filename and full path for the cache-file.
            cache_filename, cache_path = \
                _compose_cache_path(func=func, cache_name=cache_name,
                                    cache_format=cache_format)

            # Check if cache-file exists on disk.
            if os.path.exists(cache_path):
                # Cache-file exists on disk, so get its age in days.
                cache_file_age_days = _file_age(cache_path).days

                # Print status.
                msg = 'Cache-file \'{0}\' on disk ({1} days old).'
                msg = msg.format(cache_filename, cache_file_age_days)
                print(msg)

                # Should the function be computed and the cache-file refreshed?
                if isinstance(cache_refresh, bool):
                    # Use cache_refresh directly as a bool whether to refresh.
                    compute = cache_refresh
                elif isinstance(cache_refresh, int):
                    # Use cache_refresh as the number of days before refresh.
                    compute = (cache_refresh == 0) or \
                              (cache_file_age_days > cache_refresh)
                elif _is_str_or_list_str(cache_refresh):
                    # Use cache_refresh as a file-path or list of file-paths.
                    # Refresh if the cache-file is older than the other files.
                    compute = _is_file_older(path=cache_path,
                                             other_paths=cache_refresh)
                else:
                    # Raise exception for invalid argument.
                    msg = 'invalid arg cache_refresh={0}'
                    msg = msg.format(cache_refresh)
                    raise ValueError(msg)

                # Load cache-file instead of computing function?
                if not compute:
                    print('- Loading from disk ... ', end='')
                    df_result = _read_cache(path=cache_path,
                                            cache_format=cache_format)
                    print('Done!')
            else:
                # Cache-file does not exist, so we must compute the function.
                compute = True

                # Print status.
                msg = 'Cache-file \'{0}\' not on disk.'
                msg = msg.format(cache_filename)
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
                _write_cache(df=df_result, path=cache_path,
                             cache_format=cache_format)
                print('Done!')

        return df_result

    return wrapper

##########################################################################
