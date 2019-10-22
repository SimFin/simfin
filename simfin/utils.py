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
from simfin.names import REPORT_DATE

##########################################################################

def add_date_offset(df, index_date=REPORT_DATE, offset=pd.DateOffset(days=90)):
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

    :param index_date:
        Name of the date-column e.g. REPORT_DATE.

    :param offset:
        Offset to add to the dates. Use Pandas DateOffset.

    :return:
        Pandas DataFrame. Same as the input `df` except the
        dates in the index have been offset by the given amount.
    """

    # Perhaps there is a better way of doing this in Pandas?

    # Remove the column with dates from the index.
    df2 = df.reset_index(index_date)

    # Add the offset to the dates.
    df2[index_date] += offset

    # Reinsert the dates into the index.
    df2 = df2.set_index(index_date, append=True)

    return df2

##########################################################################
