##########################################################################
#
# Functions for resampling Pandas DataFrames and Series.
#
##########################################################################
# SimFin - Simple financial data for Python.
# www.simfin.com - www.github.com/simfin/simfin
# See README.md for instructions and LICENSE.txt for license details.
##########################################################################

from simfin.names import TICKER, REPORT_DATE

import pandas as pd

##########################################################################

def resample(df, rule='D', method='ffill',
             group_index=TICKER, date_index=REPORT_DATE):
    """
    Resample a Pandas DataFrame or Series with either a DatetimeIndex or
    MultiIndex. This can be used to resample financial data for a single
    company, or resample data for multiple companies in a single DataFrame.

    :param df:
        Pandas DataFrame or Series.

    :param rule:
        Resampling frequency e.g. 'D' for daily.

        This is passed directly to the Pandas resampler which has more options:
        https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects

    :param method:
        String for the method of filling in empty values. Valid options:
        'ffill' is forward-fill with last known values.
        'linear' is linear interpolation between known values.

    :param group_index:
        If `df` has a MultiIndex then group companies using this data-column.
        By default this is TICKER but it could also be e.g. SIMFIN_ID if
        you are using that as an index in your DataFrame.

    :param date_index:
        If `df` has a MultiIndex then use this data-column as the dates.
        By default this is REPORT_DATE but it could also be e.g. PUBLISH_DATE
        if you are using that as an index in your DataFrame.

    :return:
        Resampled DataFrame or Series.
    """

    assert isinstance(df, (pd.DataFrame, pd.Series))
    assert isinstance(df.index, (pd.DatetimeIndex, pd.MultiIndex))
    assert method == 'ffill' or method == 'linear'

    # Pandas 0.25.1 does not support upsampling a DataFrame with a MultiIndex
    # using the normal resample() function, so we must handle the two cases
    # differently.

    # An issue has been opened on GitHub and hopefully this gets fixed in
    # the future so this implementation can be made more elegant.
    # https://github.com/pandas-dev/pandas/issues/28313

    # If the DataFrame has a DatetimeIndex.
    if isinstance(df.index, pd.DatetimeIndex):
        # Normal resampling using Pandas.

        if method == 'ffill':
            # Fill with last-known value.
            df_resampled = df.resample(rule).ffill()
        elif method == 'linear':
            # Fill with linearly interpolated values.
            df_resampled = df.resample(rule).interpolate(method='linear')

    # If the DataFrame has a MultiIndex.
    elif isinstance(df.index, pd.MultiIndex):
        # Pandas has very complicated semantics for resampling a DataFrame
        # with a MultiIndex. The best way is apparently to group the DataFrame
        # by companies (e.g. using TICKER) which creates an individual
        # DataFrame for each company, and then apply the resampling to each
        # of those DataFrames. It is further complicated by the need to reset
        # and set the index. Pandas is quite poorly designed in this regard
        # and its resampling API has already been changed several times.

        # Helper-function for resampling a DataFrame for a single company.
        def _resample(df):
            if method == 'ffill':
                # Fill with last-known value.
                return df.set_index(date_index).resample(rule).ffill()
            elif method == 'linear':
                # Fill with linearly interpolated values.
                return df.set_index(date_index).resample(rule).interpolate(method='linear')

        # Group the original DataFrame by companies and apply the resampling to each.
        df_resampled = df.reset_index(level=date_index).groupby(level=group_index).apply(_resample)

    return df_resampled


def resample_daily(*args, **kwargs):
    """
    Resample a Pandas DataFrame or Series to daily data. This is typically
    used for upsampling quarterly or annual financial data.

    This is a simple wrapper for the `resample` function and has the same
    arguments, except for `rule` which has been set to 'D' for daily.
    """

    return resample(rule='D', *args, **kwargs)

##########################################################################
