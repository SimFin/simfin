##########################################################################
#
# Various utility functions.
#
##########################################################################
# SimFin - Simple financial data for Python.
# www.simfin.com - www.github.com/simfin/simfin
# See README.md for instructions and LICENSE.txt for license details.
##########################################################################

import pandas as pd
from simfin.names import REPORT_DATE, TICKER

##########################################################################

def add_date_offset(df, date_index=REPORT_DATE, offset=pd.DateOffset(days=90)):
    """
    Add an offset to the date-index of a Pandas DataFrame.

    This is useful if you want to add a lag of e.g. 3 months
    (90 days) to the dates of financial reports such as Income
    Statements or Balance Sheets, because the REPORT_DATE is
    not when it was actually made available to the public.

    Typically there is a lag of 1, 2 or even 3 months between
    the REPORT_DATE and the actual date of publication. This
    function makes it easy to add such a lag to all reports.

    Although PUBLISH_DATE is supposed to be the actual date of
    publication, it can be misleading if there has been
    restatements to a financial report. Sometimes these can
    occur several years later, and because SimFin uses the
    newest data available, the PUBLISH_DATE is the date of the
    latest restatement rather than the first report, so the
    PUBLISH_DATE is not always useful.

    :param df:
        Pandas DataFrame assumed to have a MultiIndex
        containing dates in a column named `index_date`.

    :param date_index:
        Name of the date-column e.g. REPORT_DATE.

    :param offset:
        Offset to add to the dates. Use Pandas DateOffset.

    :return:
        Pandas DataFrame. Same as the input `df` except the
        dates in the index have been offset by the given amount.
    """

    # Perhaps there is a better way of doing this in Pandas?

    # Remove the column with dates from the index.
    df2 = df.reset_index(date_index)

    # Add the offset to the dates.
    df2[date_index] += offset

    # Reinsert the dates into the index.
    df2 = df2.set_index(date_index, append=True)

    return df2

##########################################################################

def apply(df, func, group_index=TICKER, **kwargs):
    """
    Apply a function to a Pandas DataFrame or Series with either a
    DatetimeIndex or MultiIndex. This is useful when you don't know
    whether a DataFrame contains data for a single or multiple stocks.

    You write your function to work for a DataFrame with a single stock,
    and this function lets you apply it to both DataFrames with a single
    or multiple stocks. The function automatically uses Pandas groupby to
    split-apply-merge on DataFrames with multiple stocks.

    :param df:
        Pandas DataFrame or Series assumed to have either a DatetimeIndex
        or a MultiIndex with 2 indices, one of which is a DatetimeIndex
        and the other is given by the arg `group_index`.

    :param func:
        Function to apply on a per-stock or per-group basis.
        The function is assumed to be of the form:

            def func(df_grp):
                # df_grp is a Pandas DataFrame with data for a single stock.
                # Perform some calculation on df_grp and create another
                # Pandas DataFrame or Series with the result and return it.
                # For example, we can calculate the cumulative sum:
                return df_grp.cumsum()

    :param group_index:
        If `df` has a MultiIndex then group data using this index-column.
        By default this is TICKER but it could also be e.g. SIMFIN_ID if
        you are using that as an index in your DataFrame.

    :param **kwargs:
        Optional keyword-arguments passed to `func`.

    :return:
        Pandas DataFrame or Series with the result of applying `func`.
    """

    assert isinstance(df, (pd.DataFrame, pd.Series))
    assert isinstance(df.index, (pd.DatetimeIndex, pd.MultiIndex))

    # If the DataFrame has a DatetimeIndex.
    if isinstance(df.index, pd.DatetimeIndex):
        df_result = func(df, **kwargs)

    # If the DataFrame has a MultiIndex.
    elif isinstance(df.index, pd.MultiIndex):
        # Helper-function for a DataFrame with a single group.
        def _apply_group(df_grp):
            # Remove group-index (e.g. TICKER) from the MultiIndex.
            df_grp = df_grp.reset_index(group_index, drop=True)

            # Perform the operation on this group.
            df_grp_result = func(df_grp, **kwargs)

            return df_grp_result

        # Split the DataFrame into sub-groups and perform
        # the operation on each sub-group and glue the
        # results back together into a single DataFrame.
        df_result = df.groupby(group_index).apply(_apply_group)

    return df_result

##########################################################################
