##########################################################################
#
# Various functions for transforming financial data.
#
##########################################################################
# SimFin - Simple financial data for Python.
# www.simfin.com - www.github.com/simfin/simfin
# See README.md for instructions and LICENSE.txt for license details.
##########################################################################

import pandas as pd
import numpy as np

from simfin.utils import apply
from simfin.names import *

##########################################################################

def free_cash_flow(df_cashflow):
    """
    Calculate Free Cash Flow from columns in the given DataFrame using the
    formula:

        FCF = Net Cash from Operations - Capital Expenditures

    :param df_cashflow:
        Pandas DataFrame assumed to have columns named NET_CASH_OPS and CAPEX.

    :return:
        Pandas Series with the FCF.
    """

    # Calculate FCF.
    # Because CAPEX is defined as the Disposition *minus* Acquisition of
    # Fixed Assets and Intangibles, we have to add CAPEX to NET_CASH_OPS in
    # order to subtract the Acquisition-part and calculate the Free Cash Flow.
    # This is discussed in more detail in Tutorial 04.
    df_result = df_cashflow[NET_CASH_OPS].fillna(0) \
              + df_cashflow[CAPEX].fillna(0)

    # Rename the result to FCF.
    df_result.rename(FCF, inplace=True)

    return df_result

##########################################################################

def ebitda(df_income, df_cashflow, formula=NET_INCOME):
    """
    Calculate 'Earnings Before Interest, Taxes, Depreciation & Amortization'
    aka. EBITDA from columns in the given DataFrames. Two different EBITDA
    formulas are supported:

    - If `formula=NET_INCOME` then:
        EBITDA = Net Income + Interest + Taxes + Depreciation + Amortization

    - If `formula=OP_INCOME` then:
        EBITDA = Operating Income + Depreciation + Amortization

    :param df_income:
        Pandas DataFrame with Income Statements.

    :param df_cashflow:
        Pandas DataFrame with Cash-Flow Statements.

    :param formula:
        String for the formula to use in the EBITDA calculation.
        Use either NET_INCOME or OP_INCOME defined in `names.py`

    :return:
        Pandas Series with the EBITDA.
    """

    if formula == OP_INCOME:
        # Calculate EBITDA using Operating Income formula.
        df_result = df_income[OP_INCOME].fillna(0) \
                  + df_cashflow[DEPR_AMOR].fillna(0)
    elif formula == NET_INCOME:
        # Calculate EBITDA using Net Income formula.
        # Note that INTEREST_EXP_NET and INCOME_TAX have negative values
        # so in order to add them back to Net Income, we have to negate them.
        df_result = df_income[NET_INCOME].fillna(0) \
                  - df_income[INTEREST_EXP_NET].fillna(0) \
                  - df_income[INCOME_TAX].fillna(0) \
                  + df_cashflow[DEPR_AMOR].fillna(0)
    else:
        # Raise exception because of invalid arg.
        msg = 'arg `formula` was invalid.'
        raise ValueError(msg)

    # Rename the result.
    df_result.rename(EBITDA, inplace=True)

    return df_result

##########################################################################

def ncav(df_balance):
    """
    Calculate the so-called Net Current Asset Value (NCAV) which is a very
    conservative estimate of the liquidation value of a company, where only
    the Current Assets are counted at 100% and no other assets are counted,
    and then the Total Liabilities are subtracted from this.

    :param df_balance:
        Pandas DataFrame which is assumed to have the columns:
        TOTAL_CUR_ASSETS, TOTAL_LIABILITIES

    :return:
        Pandas Series
    """

    # Calculate NCAV.
    df_result = df_balance[TOTAL_CUR_ASSETS] - df_balance[TOTAL_LIABILITIES]

    # Rename the result.
    df_result.rename(NCAV, inplace=True)

    return df_result


def netnet(df_balance):
    """
    Calculate the so-called NetNet Working Capital which is an even more
    conservative estimate of the liquidation value of a company compared to
    the NCAV, because Cash & Equivalents are counted at 100%, but Receivables
    are only counted at 75%, Inventories are counted at 50%, and no other
    assets are counted, and the Total Liabilities are subtracted from this.

    :param df_balance:
        Pandas DataFrame which is assumed to have the columns:
        CASH_EQUIV_ST_INVEST, ACC_NOTES_RECV, INVENTORIES, TOTAL_LIABILITIES

    :return:
        Pandas Series
    """

    # Calculate NetNet.
    df_result = df_balance[CASH_EQUIV_ST_INVEST].fillna(0) \
              + df_balance[ACC_NOTES_RECV].fillna(0) * 0.75 \
              + df_balance[INVENTORIES].fillna(0) * 0.5 \
              - df_balance[TOTAL_LIABILITIES]

    # Rename the result.
    df_result.rename(NETNET, inplace=True)

    return df_result

##########################################################################

def clip(df, lower, upper):
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

    :param df:
        Pandas DataFrame with the data to be clipped.

    :param lower:
        Dict or Pandas Series with the lower bounds for some or all of the
        columns in `df`.

    :param upper:
        Dict or Pandas Series with the upper bounds for some or all of the
        columns in `df`.

    :return:
        Pandas DataFrame similar to `df` but with clipped values.
    """

    # Pandas' clip-function doesn't allow dicts with bounds for only some
    # columns, so we convert them to Pandas Series which is allowed.
    if isinstance(lower, dict):
        lower = pd.Series(lower)
    if isinstance(upper, dict):
        upper = pd.Series(upper)

    # Clip the data between the lower and upper bounds.
    df_clipped = df.clip(lower=lower, upper=upper, axis='columns')

    # If the bounds were only for some columns, Pandas' clip has set all
    # other columns to NaN, so we copy those values from the original data.
    df_clipped = df_clipped.fillna(df)

    return df_clipped

##########################################################################

def winsorize(df, quantile=0.05, clip=True, columns=None):
    """
    Limit the values in the DataFrame between `quantile` and `(1-quantile)`.
    This is useful for removing outliers without specifying the exact bounds.

    For example, when `quantile=0.05` we limit all values between the
    0.05 and 0.95 quantiles.

    Note that `inf` and `NaN` values are ignored when finding the quantiles.

    :param df:
        Pandas DataFrame with the data to be limited.

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

    :return:
        Pandas DataFrame similar to `df` but with Winsorized values.
    """

    if columns is not None:
        # Winsorize SOME of the columns in the DataFrame.

        # Create a copy of the original data.
        df_clipped = df.copy()

        # Recursively call this function to Winsorize and update those columns.
        df_clipped[columns] = winsorize(df=df[columns], quantile=quantile,
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
            # Clip / limit the values outside these quantiles.
            df_clipped = df.clip(lower=lower, upper=upper, axis='columns')
        else:
            # Boolean mask for the values that are outside these quantiles.
            mask_outside = (df < lower) | (df > upper)

            # Set the values outside the quantiles to NaN.
            df_clipped = df.copy()
            df_clipped[mask_outside] = np.nan

    return df_clipped

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
