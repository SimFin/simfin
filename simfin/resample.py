##########################################################################
#
# Functions for resampling and reindexing Pandas DataFrames and Series.
#
##########################################################################
# SimFin - Simple financial data for Python.
# www.simfin.com - www.github.com/simfin/simfin
# See README.md for instructions and LICENSE.txt for license details.
##########################################################################

from simfin.utils import apply
from simfin.names import TICKER

import pandas as pd
import functools

##########################################################################
# Private helper-functions.

def _convert_method_arg(method):
    """
    Convert argument `method` to a function that can be called after
    resampling or reindexing a DataFrame. If `method` is a string such
    as 'ffill' or 'bfill' then it will be converted to a function. Otherwise
    if `method` is itself a callable function, then it will be used directly.

    For example, the string 'ffill' is converted to a lambda-function `func`
    so that `func(df.resample(rule))` actually performs the chained
    function-call `df.resample(rule).ffill()`

    :param method: String or callable function.

    :return: Callable function.
    """

    if method == 'ffill':
        # Forward fill.
        func = lambda x: x.ffill()
    elif method == 'bfill':
        # Backward fill
        func = lambda x: x.bfill()
    elif method == 'linear':
        # Linear interpolation.
        func = lambda x: x.interpolate(method='linear')
    elif method == 'quadratic':
        # Quadratic interpolation.
        func = lambda x: x.interpolate(method='quadratic')
    elif method == 'mean':
        # Averaging which is useful in downsampling.
        func = lambda x: x.mean()
    elif callable(method):
        # Use the provided callable method directly.
        func = method
    else:
        # Raise exception because of invalid arg.
        msg = 'arg `method` must either be a valid string or a callable function.'
        raise ValueError(msg)

    return func

##########################################################################

def asfreq(df, freq, method=None, group_index=TICKER, **kwargs):
    """
    Simple resampling of a Pandas DataFrame or Series with either a
    DatetimeIndex or MultiIndex. This can be used to resample financial
    data for a single company, or resample data for multiple companies
    in a single DataFrame.

    This only provides options for forward- and backward-fill of new
    data-points. If you need other filling methods, then you should use
    the :obj:`~simfin.resample.resample` function.

    :param df:
        Pandas DataFrame or Series assumed to have either a DatetimeIndex
        or a MultiIndex with 2 indices, one of which is a DatetimeIndex
        and the other is given by the arg `group_index`.

    :param freq:
        Resampling frequency e.g. 'D' for daily.
        This is passed directly to the Pandas function which has more options:
        https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects

    :param method:
        String for the method of filling in empty values. Valid options:

        - `None`, do not fill in the empty values.
        - 'ffill' is forward-fill with last known values.
        - 'bfill' is backward-fill using future values.

        This is passed directly to the Pandas function which has more options:
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.asfreq.html

    :param group_index:
        If `df` has a MultiIndex then group data using this index-column.
        By default this is TICKER but it could also be e.g. SIMFIN_ID if
        you are using that as an index in your DataFrame.

    :param **kwargs:
        Optional keyword-arguments passed directly to Pandas `asfreq` function.
        Valid arguments:
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.asfreq.html

    :return:
        Resampled DataFrame or Series.
    """

    # Function to apply on a DataFrame with a single stock.
    def _asfreq(df_grp):
        return df_grp.asfreq(freq=freq, method=method, **kwargs)

    # Apply the function and use groupby if DataFrame has multiple stocks.
    df_result = apply(df=df, func=_asfreq, group_index=group_index)

    return df_result


# Convenience function for asfreq with daily frequency.
asfreq_daily = functools.partial(asfreq, freq='D')
asfreq_daily.__doc__ = 'Resample (asfreq) a Pandas DataFrame or Series to ' \
                       'daily data. This is typically used for upsampling ' \
                       'quarterly or annual financial data. ' \
                       'See :obj:`~simfin.resample.asfreq` for valid args.'

##########################################################################

def resample(df, rule, method='ffill', group_index=TICKER, **kwargs):
    """
    Resample a Pandas DataFrame or Series with either a DatetimeIndex
    or MultiIndex. This can be used to resample financial data for a
    single company, or resample data for multiple companies in a
    single DataFrame.

    Unlike the :obj:`~simfin.resample.asfreq` function which only allows
    forward- and backward-fill, this function allows for the use of
    arbitrary functions, either using string keywords for the most common
    filling functions, or user-supplied functions for arbitrary filling
    and summarization.

    :param df:
        Pandas DataFrame or Series assumed to have either a DatetimeIndex
        or a MultiIndex with 2 indices, one of which is a DatetimeIndex
        and the other is given by the arg `group_index`.

    :param rule:
        Resampling frequency e.g. 'D' for daily.
        This is passed directly to the Pandas function which has more options:
        https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects

    :param method:
        String or callable for the method of filling in empty values.
        Valid options:

        - 'ffill' is forward-fill with last known values.
        - 'bfill' is backward-fill using future values.
        - 'linear' is linear interpolation between known values.
        - 'quadratic' is quadratic interpolation between known values.
        - 'mean' is averaging for use when downsampling.

        Can also be a callable function or lambda-function which is called
        after the resampling, e.g.: `method=lambda x: x.nearest(limit=100)`

    :param group_index:
        If `df` has a MultiIndex then group data using this index-column.
        By default this is TICKER but it could also be e.g. SIMFIN_ID if
        you are using that as an index in your DataFrame.

    :param **kwargs:
        Optional keyword-arguments passed directly to Pandas resample function.
        Valid arguments:
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.resample.html

    :return:
        Resampled DataFrame or Series.
    """

    # Convert arg `method` to a function that can be called after resampling.
    # For example, if fill_func = lambda x: x.ffill() then we have that
    # fill_func(df.resample()) is equivalent to df.resample().ffill()
    fill_func = _convert_method_arg(method=method)

    # Function to apply on a DataFrame with a single stock.
    def _resample(df_grp):
        return fill_func(df_grp.resample(rule=rule, **kwargs))

    # Apply the function and use groupby if DataFrame has multiple stocks.
    df_result = apply(df=df, func=_resample, group_index=group_index)

    return df_result


# Convenience function for resampling to daily data.
resample_daily = functools.partial(resample, rule='D')
resample_daily.__doc__ = 'Resample a Pandas DataFrame or Series to daily ' \
                         'data. This is typically used for upsampling ' \
                         'quarterly or annual financial data. ' \
                         'See :obj:`~simfin.resample.resample` for valid args.'

##########################################################################
# Functions for creating and combining DataFrame indices.

def index_union(df_src, df_target, use_target_names=True):
    """
    Create the union of the indices for the two Pandas DataFrames.
    This combines the "rows" of the two indices, so the index-types
    must be identical.

    :param df_src: Pandas Series or DataFrame.

    :param df_target: Pandas Series or DataFrame.

    :param use_target_names:
        Boolean whether to use the index-names
        from `df_target` (True) or `df_src` (False).

    :return: Pandas Index.
    """

    # This is not a "deep" type comparison. Two MultiIndex could be different.
    assert (type(df_src.index) == type(df_target.index))

    # Create the union of the indices.
    # This does not copy the index-names.
    idx = df_src.index.union(df_target.index)

    if use_target_names:
        # Use the index-names from the target.
        # This is similar to Pandas' reindex.
        idx.names = df_target.index.names
    else:
        # Use the index-names from the source.
        idx.names = df_src.index.names

    return idx

##########################################################################

def reindex(df_src, df_target, group_index=TICKER, union=True,
            only_target_index=True, method=None, **kwargs):
    """
    Reindex a source Pandas DataFrame or Series with either a DatetimeIndex
    or MultiIndex, so that it conforms to the index of a target DataFrame.

    This can be used to resample financial data for a single company, or
    resample data for multiple companies in a single DataFrame.

    It differs from the :obj:`~simfin.resample.resample` function because
    the resampled data has the same index as the target DataFrame. This is
    useful e.g. when upsampling annual or quarterly financial data to daily
    data that matches the share-price data, even beyond the last date of the
    financial data.

    By default this function uses a union of the indices of the source and
    target DataFrames, because otherwise data-points from the source might
    be lost if those particular dates do not exist in the target DataFrame.
    We can still ensure the resulting DataFrame only has the index of the
    target DataFrame, by setting `only_target_index=True`.
    This is explained in more detail in `Tutorial 02`_ on resampling.

    :param df_src:
        Pandas DataFrame or Series assumed to have either a DatetimeIndex
        or a MultiIndex with 2 indices, one of which is a DatetimeIndex
        and the other is given by the arg `group_index`.

    :param df_target:
        Pandas DataFrame or Series assumed to have an index of the same
        type as `df_src`. For example, they can both be a DatetimeIndex,
        or they can both be a MultiIndex with 2 indices, of which one
        must be a DatetimeIndex. The names of the indices can be different.

    :param group_index:
        If `df_src` and `df_target` have a MultiIndex then group data
        using this index-column. By default this is TICKER but it could also
        be e.g. SIMFIN_ID if you are using that as an index in your DataFrame.

    :param method:
        String or callable for the method of filling in empty values.
        You should not pass a summarizing method e.g. the string 'mean' or
        a similar lambda-function. You should only use filling methods such
        as forward-fill or interpolation. Valid options:

        - 'ffill' is forward-fill with last known values.
        - 'bfill' is backward-fill using future values.
        - 'linear' is linear interpolation between known values.
        - 'quadratic' is quadratic interpolation between known values.

        Can also be a callable function or lambda-function which is called
        after the reindexing, e.g.:
        `method=lambda x: x.interpolate(method='nearest')`

    :param union:
        Boolean. If True then use the union of the indices from `df_src` and
        `df_target`. If False then only use the index from `df_target`.

    :param only_target_index:
        This is only used if `union==True`. Boolean whether to perform an
        additional reindex operation to ensure the final index matches the
        index of `df_target`, otherwise it might have rows from `df_src`
        that do not exist in the index of `df_target`.

    :param **kwargs:
        Optional keyword-arguments passed directly to Pandas `reindex`
        function. Valid arguments:
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.reindex.html

    :return:
        Resampled DataFrame or Series.
    """

    assert isinstance(df_src, (pd.DataFrame, pd.Series))
    assert isinstance(df_target, (pd.DataFrame, pd.Series))
    # This is not a "deep" type comparison. Two MultiIndex could be different.
    assert (type(df_src.index) == type(df_target.index))

    # Convert arg `method` to a function that can be called after reindexing.
    # For example, if fill_func = lambda x: x.ffill() then we have that
    # fill_func(df.reindex()) is equivalent to df.reindex().ffill()
    fill_func = _convert_method_arg(method=method)

    # Which target index to use?
    if union:
        # Use the union of the indices of the source and target DataFrames.
        new_index = index_union(df_src=df_src, df_target=df_target)
    else:
        # Only use the index of the target DataFrame.
        new_index = df_target.index

    # Reindex the DataFrame. This works with both DatetimeIndex and MultiIndex.
    df_result = df_src.reindex(index=new_index, **kwargs)

    # Apply the fill-function and use groupby if DataFrame has multiple stocks.
    df_result = apply(df=df_result, func=fill_func, group_index=group_index)

    # Perform an additional reindex operation to ensure the final
    # result only contains the rows from df_target. This is only
    # necessary if we have used the union of the two indices in
    # the main reindexing.
    if union and only_target_index:
        df_result = df_result.reindex(index=df_target.index)

    return df_result

##########################################################################
