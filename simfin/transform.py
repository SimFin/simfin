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

from simfin.names import *

##########################################################################

def free_cash_flow(df_cashflow):
    """
    Calculate Free Cash Flow from columns in the given DataFrame.

    :param df_cashflow:
        Pandas DataFrame assumed to have columns named NET_CASH_OPS and CAPEX.

    :return:
        Pandas Series with the FCF.
    """

    # Calculate FCF.
    # Because CAPEX is defined as the Disposition *minus* Acquisition of
    # Fixed Assets and Intangibles, we have to add CAPEX to NET_CASH_OPS in
    # order to subtract the Acquisition-part and calculate the Free Cash Flow.
    df_result = df_cashflow[NET_CASH_OPS] + df_cashflow[CAPEX]

    # Rename the result to FCF.
    df_result.rename(FCF, inplace=True)

    return df_result

##########################################################################

def ebitda(df_income, df_cashflow, formula=NET_INCOME):
    """
    Calculate 'Earnings Before Interest, Taxes, Depreciation & Amortization'
    aka. EBITDA from columns in the given DataFrames. Two different EBITDA
    formulas are supported:

    If `formula=NET_INCOME` then the formula is:
        EBITDA = Net Income + Interest + Taxes + Depreciation + Amortization

    If `formula=OP_INCOME` then the formula is:
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

def clip(df, lower, upper):
    """
    Limit the values of a DataFrame between the lower and upper bounds.
    This is very similar to Pandas' clip-function, except that if you
    only provide bounds for some of the columns, Pandas' clip-function will
    set all the other columns to NaN-values, while this function will just
    use the values from the original DataFrame.

    For example, if `df` contains the columns PE, PFCF, PSALES and PBOOK, but
    you only want to clip the values for PE and PFCF, you can pass dicts with
    bounds for only those columns:

        `lower = {PE: 5, PFCF: 6}`
        `upper = {PE: 30, PFCF: 40}`

    Using Pandas' clip-function (v. 0.25) this would result in the other
    columns for PSALES and PBOOK to have only NaN-values, while this function
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

def winsorize(df, quantile=0.05, columns=None):
    """
    Limit the values in the DataFrame between quantile and (1-quantile).
    This is useful for removing outliers without specifying the exact bounds.

    For example, when quantile=0.05 we limit all values between the
    0.05 and 0.95 quantiles.

    :param df:
        Pandas DataFrame with the data to be limited.

    :param quantile:
        Float between 0.0 and 1.0

    :param columns:
        List of strings with names of the columns in `df` to winsorize.
        If None then winsorize all columns in `df`.

    :return:
        Pandas DataFrame similar to `df` but with winsorized values.
    """

    if columns is not None:
        # Winsorize SOME of the columns in the DataFrame.

        # Create a copy of the original data.
        df_clipped = df.copy()

        # Recursively call this function to winsorize and update those columns.
        df_clipped[columns] = winsorize(df=df[columns], quantile=quantile)
    else:
        # Winsorize ALL of the columns in the DataFrame.

        # Lower and upper quantiles for all columns in the data.
        lower = df.quantile(q=quantile)
        upper = df.quantile(q=1.0 - quantile)

        # Limit / clip all column-values between these quantiles.
        df_clipped = df.clip(lower=lower, upper=upper, axis='columns')

    return df_clipped

##########################################################################

def avg_ttm_2y(df):
    """
    Calculate 2-year averages from TTM financial data, which has 4 data-points
    per year, and each data-point covers the Trailing Twelve Months.

    This is different from using a rolling average on TTM data, which
    over-weighs the most recent quarters in the average.

    This function should only be used on DataFrames for a single stock.
    Use `sf.apply` with this function on DataFrames for multiple stocks.

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
    Use `sf.apply` with this function on DataFrames for multiple stocks.

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
    Use `sf.apply` with this function on DataFrames for multiple stocks.

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
