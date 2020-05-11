##########################################################################
#
# Various functions for transforming Pandas DataFrames and Series.
#
##########################################################################
# SimFin - Simple financial data for Python.
# www.simfin.com - www.github.com/simfin/simfin
# See README.md for instructions and LICENSE.txt for license details.
##########################################################################

import pandas as pd
import numpy as np

from simfin.utils import apply, rename_columns
from simfin.names import TICKER

##########################################################################

def clip(df, lower, upper, clip=True):
    """
    Limit the values of a DataFrame between the lower and upper bounds.
    This is very similar to Pandas' `clip`-function, except that if you
    only provide bounds for some of the columns, Pandas' `clip`-function will
    set all the other columns to `NaN`-values, while this function will just
    use the values from the original DataFrame.

    For example, if `df` contains the columns PE, PFCF, PSALES and PBOOK, but
    you only want to clip the values for PE and PFCF, you can pass dicts with
    bounds for only those columns:

    - `lower = {PE: 5, PFCF: 6}`
    - `upper = {PE: 30, PFCF: 40}`

    Using Pandas' `clip`-function (v. 0.25) this would result in the other
    columns for PSALES and PBOOK to have only `NaN`-values, while this function
    copies the original values from `df` for those columns.

    Furthermore, this function can also set the values outside the bounds to
    `NaN` instead of using the boundary values, which can distort statistical
    analysis.

    :param df:
        Pandas DataFrame with the data to be clipped.

    :param lower:
        Dict or Pandas Series with the lower bounds for some or all of the
        columns in `df`.

    :param upper:
        Dict or Pandas Series with the upper bounds for some or all of the
        columns in `df`.

    :param clip:
        Boolean whether to clip/limit all values outside the bounds (True),
        or if the values should be set to NaN (False). Note: When the values
        are clipped it can distort statistical analysis of the data. But when
        the values are set to NaN, it reduces the amount of data-points
        available for the statistical analysis. You should try both options.

    :return:
        Pandas DataFrame similar to `df` but with clipped values.
    """

    # Pandas' clip-function doesn't allow dicts with bounds for only some
    # columns, so we convert them to Pandas Series which is allowed.
    if isinstance(lower, dict):
        lower = pd.Series(lower)
    if isinstance(upper, dict):
        upper = pd.Series(upper)

    # Clip/limit the values outside these bounds, or set them to NaN?
    if clip:
        # Clip/limit the data between the lower and upper bounds.
        df_clipped = df.clip(lower=lower, upper=upper, axis='columns')

        # If the bounds were only for some columns, Pandas' clip has set all
        # other columns to NaN, so we copy those values from the original data.
        df_clipped = df_clipped.fillna(df)
    else:
        # Boolean mask for the values that are outside the bounds.
        mask_outside = (df < lower) | (df > upper)

        # Copy the original data and set the values outside the bounds to NaN.
        df_clipped = df.where(~mask_outside)

    return df_clipped

##########################################################################

def winsorize(df, quantile=0.05, clip=True,
              columns=None, exclude_columns=None):
    """
    Limit the values in the DataFrame between `quantile` and `(1-quantile)`.
    This is useful for removing outliers without specifying the exact bounds.

    For example, when `quantile=0.05` we limit all values between the
    0.05 and 0.95 quantiles.

    Note that `inf` and `NaN` values are ignored when finding the quantiles.

    :param df:
        Pandas DataFrame or Series with the data to be limited.

    :param quantile:
        Float between 0.0 and 1.0

    :param clip:
        Boolean whether to clip/limit all values outside the quantiles (True),
        or if the values should be set to NaN (False). Note: When the values
        are clipped it can distort statistical analysis of the data. But when
        the values are set to NaN, it reduces the amount of data-points
        available for the statistical analysis. You should try both options.

    :param columns:
        List of strings with names of the columns in `df` to Winsorize,
        and the rest of the columns are merely copied from `df`.
        If `None` then Winsorize all columns in `df`.

    :param exclude_columns:
        List of strings with names of columns in `df` to exclude from the
        Winsorization. If `None` then Winsorize all columns in `df`.

    :return:
        Pandas DataFrame or Series similar to `df` but with Winsorized values.

    :raises:
        ValueError: If both `columns` and `exclude_commons` are given.
    """

    # Invalid arguments?
    if columns is not None and exclude_columns is not None:
        msg = 'Arguments columns and exclude_columns cannot both be set'
        raise ValueError(msg)

    if exclude_columns is not None:
        # Winsorize all columns EXCEPT the ones given.
        columns = df.columns.difference(exclude_columns)

    if columns is not None:
        # Winsorize SOME of the columns in the DataFrame.

        # Create a copy of the original data.
        df_result = df.copy()

        # Recursively call this function to Winsorize and update those columns.
        df_result[columns] = winsorize(df=df[columns], quantile=quantile,
                                       clip=clip)
    else:
        # Winsorize ALL of the columns in the DataFrame.

        # Boolean mask used to ignore inf values.
        mask = np.isfinite(df)

        # Lower and upper quantiles for all columns in the data.
        # We use the boolean mask to select only the finite values,
        # and the infinite values are set to NaN, which are ignored
        # by the quantile-function.
        lower = df[mask].quantile(q=quantile)
        upper = df[mask].quantile(q=1.0 - quantile)

        # Clip the values outside these quantiles, or set them to NaN?
        if clip:
            # Only use the axis-arg for a DataFrame, not for a Series.
            axis = 'columns' if isinstance(df, pd.DataFrame) else None

            # Clip / limit the values outside these quantiles.
            df_result = df.clip(lower=lower, upper=upper, axis=axis)
        else:
            # Boolean mask for the values that are outside these quantiles.
            mask_outside = (df < lower) | (df > upper)

            # Set the values outside the quantiles to NaN.
            df_result = df.copy()
            df_result[mask_outside] = np.nan

    return df_result

##########################################################################

def avg_ttm_2y(df):
    """
    Calculate 2-year averages from TTM financial data, which has 4 data-points
    per year, and each data-point covers the Trailing Twelve Months.

    This is different from using a rolling average on TTM data, which
    over-weighs the most recent quarters in the average.

    This function should only be used on DataFrames for a single stock.
    Use :obj:`~simfin.utils.apply` with this function on DataFrames for
    multiple stocks.

    :param df:
        Pandas DataFrame with TTM financial data sorted ascendingly by date.

    :return:
        Pandas DataFrame with 2-year averages.
    """
    return 0.5 * (df + df.shift(4))


def avg_ttm_3y(df):
    """
    Calculate 3-year averages from TTM financial data, which has 4 data-points
    per year, and each data-points covers the Trailing Twelve Months.

    This is different from using a rolling average on TTM data, which
    over-weighs the most recent quarters in the average.

    This function should only be used on DataFrames for a single stock.
    Use :obj:`~simfin.utils.apply` with this function on DataFrames for
    multiple stocks.

    :param df:
        Pandas DataFrame with TTM financial data sorted ascendingly by date.

    :return:
        Pandas DataFrame with 3-year averages.
    """
    return (1.0/3.0) * (df + df.shift(4) + df.shift(8))


def avg_ttm(df, years):
    """
    Calculate multi-year averages from TTM financial data, which has 4
    data-points per year, that each covers the Trailing Twelve Months.

    This is different from using a rolling average on TTM data, which
    over-weighs the most recent quarters in the average.

    This function should only be used on DataFrames for a single stock.
    Use :obj:`~simfin.utils.apply` with this function on DataFrames for
    multiple stocks.

    :param df:
        Pandas DataFrame with TTM financial data sorted ascendingly by date.

    :param years:
        Integer for the number of years.

    :return:
        Pandas DataFrame with the averages.
    """

    # Start with the non-shifted data.
    df_result = df.copy()

    # Add shifted data for each year.
    for i in range(1, years):
        df_result += df.shift(4 * i)

    # Take the average.
    df_result /= years

    return df_result

##########################################################################

def rel_change_ttm_1y(df):
    """
    Calculate 1-year relative change from TTM financial data, which has
    4 data-points per year, and each data-point covers the Trailing Twelve
    Months.

    This is a light-weight version of :obj:`~simfin.rel_change.rel_change`
    intended to be used as the `func` argument in the signal-functions.

    This function can also be used directly on DataFrames for a single stock,
    or on DataFrames for multiple stocks using :obj:`~simfin.utils.apply`

    :param df:
        Pandas DataFrame with TTM financial data sorted ascendingly by date.

    :return:
        Pandas DataFrame with 1-year relative changes.
    """
    return df / df.shift(4) - 1


def rel_change_ttm_2y(df):
    """
    Calculate 2-year relative change from TTM financial data, which has
    4 data-points per year, and each data-point covers the Trailing Twelve
    Months.

    This is a light-weight version of :obj:`~simfin.rel_change.rel_change`
    intended to be used as the `func` argument in the signal-functions.

    This function can also be used directly on DataFrames for a single stock,
    or on DataFrames for multiple stocks using :obj:`~simfin.utils.apply`

    :param df:
        Pandas DataFrame with TTM financial data sorted ascendingly by date.

    :return:
        Pandas DataFrame with 2-year relative changes.
    """
    return df / df.shift(8) - 1

##########################################################################

def max_drawdown(df, window=None, group_index=TICKER):
    """
    Calculate the Maximum Drawdown for all stocks in the given DataFrame.

    :param df:
        Pandas DataFrame typically with share-prices but could have any data.
        The DataFrame may contain data for one or more stocks.

    :param window:
        If `None` then calculate the Max Drawdown from the beginning.
        If an integer then calculate the Max Drawdown for a rolling window
        of that length.

    :param group_index:
        If the DataFrame has a MultiIndex then group data using this
        index-column. By default this is TICKER but it could also be e.g.
        SIMFIN_ID if you are using that as an index in your DataFrame.

    :return:
        Pandas DataFrame with the Max Drawdown.
    """

    # Helper-function for calculating the Max Drawdown for a single stock.
    if window is None:
        # Calculate Max Drawdown from the beginning.
        def _max_drawdown(df):
            return df / df.cummax() - 1.0
    else:
        # Calculate Max Drawdown for a rolling window.
        def _max_drawdown(df):
            return df / df.rolling(window=window).max() - 1.0

    # Calculate Max Drawdown. Use Pandas groupby if `df` has multiple stocks.
    df_result = apply(df=df, func=_max_drawdown, group_index=group_index)

    return df_result

##########################################################################

def moving_zscore(df, periods, rolling=True, new_names=None,
                  group_index=TICKER):
    """
    Calculate the Moving Z-Score for all stocks in the given DataFrame.

    :param df:
        Pandas DataFrame e.g. with P/Sales ratios but could have any data.
        The DataFrame may contain data for one or more stocks.

    :param periods:
        Integer with the number of time-steps to calculate Z-Score for.
        If `rolling==True` then it is the length of the moving window.
        If `rolling==False` then it is the minimum window-length before
        the Z-Score is calculated.

    :param rolling:
        Boolean whether to use a rolling window (True), or to use all preceding
        data-points (False).

    :param new_names:
        Dict or function for mapping / converting the column-names.
        If `df` is a Pandas Series, then this is assumed to be a string.

    :param group_index:
        If the DataFrame has a MultiIndex then group data using this
        index-column. By default this is TICKER but it could also be e.g.
        SIMFIN_ID if you are using that as an index in your DataFrame.

    :return:
        Pandas DataFrame with the Moving Z-Score.
    """

    # Helper-function for calculating the Moving Z-Score for a single stock.
    if rolling:
        # Calculate Z-Score for a rolling window.
        def _moving_zscore(df):
            x = df.rolling(window=periods)
            return (df - x.mean()) / x.std()
    else:
        # Calculate Z-Score from the beginning.
        def _moving_zscore(df):
            x = df.expanding(min_periods=periods)
            return (df - x.mean()) / x.std()

    # Calculate Moving Z-Score. Use Pandas groupby if `df` has multiple stocks.
    df_result = apply(df=df, func=_moving_zscore, group_index=group_index)

    # Rename the columns.
    if new_names is not None:
        rename_columns(df=df_result, new_names=new_names, inplace=True)

    return df_result

##########################################################################
