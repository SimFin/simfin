##########################################################################
#
# Function for calculating the changes over time in time-series data of a
# Pandas DataFrame. This is used to calculate growth-rates for financial
# data e.g. Sales and Earnings Growth, as well as stock-returns.
#
##########################################################################
# SimFin - Simple financial data for Python.
# www.simfin.com - www.github.com/simfin/simfin
# See README.md for instructions and LICENSE.txt for license details.
##########################################################################

import numpy as np

from simfin.cache import cache
from simfin.utils import apply, convert_to_periods, rename_columns
from simfin.names import TICKER

##########################################################################

@cache
def rel_change(df, freq, future, bdays=0, days=0, weeks=0, months=0,
               quarters=0, years=0, annualized=False, new_names=None,
               group_index=TICKER):
    """
    Calculate the relative change for the values in a Pandas DataFrame or
    Series with either a DatetimeIndex or MultiIndex.

    This can be used to calculate growth-rates e.g. Sales and Earnings Growth,
    as well as stock-returns. It can be calculated for any time-interval that
    is a multiple of the DataFrame's frequency.

    The number of days, weeks, months, quarters and years is combined into
    an integer `periods` for the number of time-steps to shift the DataFrame,
    depending on the DataFrame's frequency. The relative change is calculated
    from the original and shifted DataFrame.

    If `annualized==False` then the function calculates the following:

    - If `future==True` then `df_result[t] = df[t+periods] / df[t] - 1`
    - If `future==False` then `df_result[t] = df[t] / df[t-periods] - 1`

    If `annualized==True` then the function calculates the annualized change
    instead, which is particularly useful when the time-interval is several
    years. For example, this can be used to calculate the Annualized Total
    Return on stocks. The variable `shifted_years` is the number of years
    corresponding to `periods`. So the function calculates:

    - If `future==True` then
      `df_result[t] = (df[t+periods] / df[t]) ** (1 / shifted_years) - 1`
    - If `future==False` then
      `df_result[t] = (df[t] / df[t-periods]) ** (1 / shifted_years) - 1`

    See `Tutorial 03`_ for detailed examples on how to use this function.

    This function can take a while to compute, so it will create a cache-file
    if you pass the arg `cache_refresh`. The next time you call this function,
    the cache-file will get loaded if it is more recent than specified by
    `cache_refresh`, otherwise the function will get computed again and the
    result saved in the cache-file for future use. See the documentation for
    the :obj:`~simfin.cache.cache` function for details on its arguments.

    .. warning:: You **MUST** use keyword arguments to this function, otherwise
        the first unnamed arguments would get passed to the `cache` wrapper
        instead.

    :param df:
        Pandas DataFrame or Series assumed to have either a DatetimeIndex
        or a MultiIndex with 2 indices, one of which is a DatetimeIndex
        and the other is given by the arg `group_index`.

        .. warning:: `df` is assumed to be sorted in ascending order on its
            date-index. Furthermore, the DataFrame is assumed to be complete
            in the sense that data is present for all time-steps at the given
            frequency. This function does not check that. The SimFin database
            ensures that quarterly and annual financial data such as Income
            Statements are all complete in this sense, but if you are using
            other data-sources, then you must ensure this yourself.

    :param freq:
        String for the frequency of the DataFrame `df`. Valid options:

        - 'bdays' or 'b' for business or trading-days data.
        - 'days' or 'd' for data that has all 7 week-days.
        - 'weeks' or 'w' for weekly data.
        - 'months' or 'm' for monthly data.
        - 'quarters' or 'q' for quarterly data.
        - 'years', 'y', 'annual', 'a' for yearly or annual data.

    :param future:
        Boolean whether to calculate the future change (True)
        or past change (False).

    :param bdays: Number of business or trading-days.
    :param days: Number of days in a 7-day week.
    :param weeks: Number of weeks.
    :param months: Number of months.
    :param quarters: Number of quarters.
    :param years: Number of years.

    :param annualized:
        Boolean whether to calculate the annualized change (True)
        or the relative change (False). When calculating the change over
        several years, it is often useful to calculate the annualized change
        by setting this to True.

    :param new_names:
        Dict or function for mapping / converting the column-names.
        If `df` is a Pandas Series, then this is assumed to be a string.

    :param group_index:
        If `df` has a MultiIndex then group companies using this index-column.
        By default this is TICKER but it could also be e.g. SIMFIN_ID if
        you are using that as an index in your DataFrame.

    :return:
        Pandas DataFrame with the result.
    """

    # Convert the arguments to the equivalent number of periods (int) that
    # the DataFrame must be shifted, and the total number of years (float)
    # that it corresponds to, which is used in the annualized formula below.
    periods, shifted_years = convert_to_periods(freq=freq, bdays=bdays,
                                                days=days, weeks=weeks,
                                                months=months,
                                                quarters=quarters,
                                                years=years)

    # Function to apply on a DataFrame with a single stock.
    def _rel_change(df_grp):
        # Relative change between past time-step [t-periods] and step [t].
        # This calculates: df_grp_result[t] = df_grp[t] / df_grp[t-periods]
        # Note that 1 will be subtracted further below.
        df_grp_result = df_grp / df_grp.shift(periods=periods)

        if future:
            # Shift the data to get the relative change between current
            # time-step [t] and future time-step [t+periods].
            # This calculates: df_grp_result[t] = df_grp[t+periods] / df_grp[t]
            df_grp_result = df_grp_result.shift(periods=-periods)

        return df_grp_result

    # Apply the function and use groupby if DataFrame has multiple stocks.
    df_result = apply(df=df, func=_rel_change, group_index=group_index)

    if annualized:
        # Calculate the annualized change.
        df_result = df_result ** (1.0 / shifted_years) - 1.0
    else:
        # Finalize the relative change by subtracting 1.
        df_result = df_result - 1.0

    # Rename the columns.
    if new_names is not None:
        rename_columns(df=df_result, new_names=new_names, inplace=True)

    return df_result

##########################################################################

@cache
def mean_log_change(df, freq, future,
                    min_bdays=0, min_days=0, min_weeks=0,
                    min_months=0, min_quarters=0, min_years=0,
                    max_bdays=0, max_days=0, max_weeks=0,
                    max_months=0, max_quarters=0, max_years=0,
                    annualized=False, new_names=None, group_index=TICKER):
    """
    Calculate the mean log-change for the values in a Pandas DataFrame or
    Series with either a DatetimeIndex or MultiIndex.

    This is useful e.g. for calculating the mean future stock-returns for
    all periods between e.g. 1 and 3 years so as to smoothen the short-term
    volatility. This can make it easier to see how predictor variables such
    as P/E ratios may relate to future returns.

    This implementation is slightly complicated, but the idea is fairly simple:
    Instead of calculating the relative change between two points `df[t]` and
    `df[t + periods]`, we want to calculate the mean change between a point
    `df[t]` and a whole slice of points `df[t + min_periods:t + max_periods]`.

    We use the logarithm because it makes it easier to implement efficiently
    by using vectorized math operations directly supported in Pandas and Numpy.
    But using the logarithm also means that negative values are not supported.

    We use the natural logarithm, which is almost linear for changes between
    ±20%, but beyond that range it underestimates both the gains and losses
    compared to the non-log changes. For practical purposes, you may often
    consider the mean-log changes to be roughly equivalent to the normal
    percentage changes.

    See `Tutorial 03`_ for a detailed explanation and derivation of the math
    used in this function, and examples on how to use this function.

    This function can take a while to compute, so it will create a cache-file
    if you pass the arg `cache_refresh`. The next time you call this function,
    the cache-file will get loaded if it is more recent than specified by
    `cache_refresh`, otherwise the function will get computed again and the
    result saved in the cache-file for future use. See the documentation for
    the :obj:`~simfin.cache.cache` function for details on its arguments.

    .. warning:: You **MUST** use keyword arguments to this function, otherwise
        the first unnamed arguments would get passed to the `cache` wrapper
        instead.

    :param df:
        Pandas DataFrame or Series assumed to have either a DatetimeIndex
        or a MultiIndex with 2 indices, one of which is a DatetimeIndex
        and the other is given by the arg `group_index`.

        .. warning:: `df` is assumed to be sorted in ascending order on its
            date-index. Furthermore, the DataFrame is assumed to be complete
            in the sense that data is present for all time-steps at the given
            frequency. This function does not check that. The SimFin database
            ensures that quarterly and annual financial data such as Income
            Statements are all complete in this sense, but if you are using
            other data-sources, then you must ensure this yourself.

    :param freq:
        String for the frequency of the DataFrame `df`. Valid options:

        - 'bdays' or 'b' for business or trading-days data.
        - 'days' or 'd' for data that has all 7 week-days.
        - 'weeks' or 'w' for weekly data.
        - 'months' or 'm' for monthly data.
        - 'quarters' or 'q' for quarterly data.
        - 'years', 'y', 'annual', 'a' for yearly or annual data.

    :param future:
        Boolean whether to calculate the future (True) or past (False) change.

    :param min_bdays: Min number of business or trading-days.
    :param min_days: Min number of days in a 7-day week.
    :param min_weeks: Min number of weeks.
    :param min_months: Min number of months.
    :param min_quarters: Min number of quarters.
    :param min_years: Min number of years.

    :param max_bdays: Max number of business or trading-days.
    :param max_days: Max number of days in a 7-day week.
    :param max_weeks: Max number of weeks.
    :param max_months: Max number of months.
    :param max_quarters: Max number of quarters.
    :param max_years: Max number of years.

    :param annualized:
        Boolean whether to calculate the annualized change (True),
        or the geometric mean for the original frequency of the data (False).
        For example, if you want to calculate the change over several years,
        it is often useful to calculate the annualized change by setting this
        to True. But if you want to calculate the change over shorter periods
        e.g. days or weeks, then the annualized change may result in extreme
        values. If you set this to False then the geometric mean is calculated
        in the original frequency of the data, e.g. daily for share-price data
        or quarterly for TTM data.

    :param new_names:
        Dict or function for mapping / converting the column-names.
        If `df` is a Pandas Series, then this is assumed to be a string.

    :param group_index:
        If `df` has a MultiIndex then group companies using this index-column.
        By default this is TICKER but it could also be e.g. SIMFIN_ID if
        you are using that as an index in your DataFrame.

    :return:
        Pandas DataFrame with the result.
    """

    ###################################################################
    # We must first convert the arguments to the equivalent number of
    # periods (int) that the DataFrame must be shifted, and the total
    # number of years (float) that it corresponds to, which is used in
    # the annualized formulas below.

    # Convert arguments for min_periods.
    min_periods, min_shifted_years = \
        convert_to_periods(freq=freq, bdays=min_bdays, days=min_days,
                           weeks=min_weeks, months=min_months,
                           quarters=min_quarters, years=min_years)

    # Convert arguments for max_periods.
    max_periods, max_shifted_years = \
        convert_to_periods(freq=freq, bdays=max_bdays, days=max_days,
                           weeks=max_weeks, months=max_months,
                           quarters=max_quarters, years=max_years)

    assert min_periods < max_periods

    # Number of periods in a windowing-slice.
    num_periods = max_periods - min_periods

    ###################################################################
    # Create the array of exponents for the windowing-slice, which is
    # used to either calculate the annualized change, or the geometric
    # mean change.

    if annualized:
        # Values between 0.0 and 1.0 for each time-step in the slice.
        x = np.arange(num_periods) / (num_periods-1)

        # Number of years the data is shifted, for each time-step in the slice.
        shifted_years = (max_shifted_years - min_shifted_years) * x + min_shifted_years

        # Array of exponents used to calculate annualized change.
        exponent = 1.0 / shifted_years
    else:
        # Array of exponents used to calculate geometric mean change in the
        # same frequency as the original data, e.g. mean daily change for
        # share-price data, or mean quarterly change for quarterly or TTM data.
        exponent = 1.0 / np.arange(min_periods, max_periods)

    # Because we are doing the window-slicing using Pandas' rolling operator,
    # we need to reverse the array of exponents if we want to calculate the
    # changes from *past* time-steps to the current time-step.
    if not future:
        exponent = np.flip(exponent)

    # Sum of all the exponents, which is used in the final formula.
    exponent_sum = np.sum(exponent)

    ################################
    # Calculate the mean log-change.

    # Logarithm of the original data, so we can use the log-transforms:
    # log(df[t+period] / df[t]) = log(df[t+period]) - log(df[t]) and
    # log(df[t] ^ exponent) = exponent * log(df[t]) in these formulas.
    df_log = np.log(df)

    # Function for the dot-product between a slice of data and the exponents.
    def _dot_product(x):
        return np.sum(x * exponent)

    # Function to calculate mean-log change on a DataFrame with a single stock.
    def _mean_log_change(df_log_grp):
        # Take successive slices of the data and apply the window-function.
        # This effectively calculates:
        # df_windowed[t] = sum( df_log_grp[t-num_periods:t] * exponents )
        df_windowed = df_log_grp.rolling(num_periods).apply(_dot_product, raw=True)

        if future:
            # Shift the data so we have:
            # df_windowed[t] = sum( df_log_grp[t+min_period:t+max_period] * exponents )
            df_windowed = df_windowed.shift(periods=-max_periods)

            # Calculate the mean log-change from df_log_grp[t] to df_windowed[t].
            # See Tutorial 03 for the mathematical derivation of this formula.
            df_mean_log_chg = (df_windowed - df_log_grp * exponent_sum) / num_periods
        else:
            # Shift the data so we have:
            # df_windowed[t] = sum( df_log_grp[t-max_period:t-min_period] * exponents )
            df_windowed = df_windowed.shift(periods=min_periods)

            # Calculate the mean log-change from df_windowed[t] to df_log_grp[t].
            # See Tutorial 03 for the mathematical derivation of this formula.
            df_mean_log_chg = (df_log_grp * exponent_sum - df_windowed) / num_periods

        return df_mean_log_chg

    # Apply the function and use groupby if DataFrame has multiple stocks.
    df_result = apply(df=df_log, func=_mean_log_change, group_index=group_index)

    # Rename the columns.
    if new_names is not None:
        rename_columns(df=df_result, new_names=new_names, inplace=True)

    return df_result

##########################################################################
