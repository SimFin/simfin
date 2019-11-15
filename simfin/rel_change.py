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

import pandas as pd

from simfin.utils import apply
from simfin.names import TICKER

##########################################################################
# Constants.

# Average number of business- or trading-days in a year.
BDAYS_PER_YEAR = 251.67

# Average number of week-days in a year. Normal years have 365 days,
# but every 4th year is a leap-year with 366 days.
DAYS_PER_YEAR = 365.25

# Number of weeks per year.
WEEKS_PER_YEAR = 52

# Number of months per year.
MONTHS_PER_YEAR = 12

# Number of quarters per year.
QUARTERS_PER_YEAR = 4

##########################################################################
# Private helper-functions.

def _convert_to_periods(freq, bdays, days, weeks, months, quarters, years):
    """
    Convert the number of days, weeks, months, quarters and years
    into the equivalent number of periods that a DataFrame must be
    shifted, when the DataFrame has the given frequency.

    :param freq:
        String for the frequency of the DataFrame. Valid options:
        - 'bdays' or 'b' for business or trading-days data.
        - 'days' or 'd' for data that has all 7 week-days.
        - 'weeks' or 'w' for weekly data.
        - 'months' or 'm' for monthly data.
        - 'quarters' or 'q' for quarterly data.
        - 'years', 'y', 'annual', 'a' for yearly or annual data.

    :param bdays: Number of business or trading-days.
    :param days: Number of days in a 7-day week.
    :param weeks: Number of weeks.
    :param months: Number of months.
    :param quarters: Number of quarters.
    :param years: Number of years.

    :return:
        periods (int): Number of steps to shift the DataFrame.
        shifted_years (float): Number of years the DataFrame is shifted.
    """

    # First we calculate the total number of years from all the arguments.
    total_years = bdays / BDAYS_PER_YEAR \
                  + days / DAYS_PER_YEAR \
                  + weeks / WEEKS_PER_YEAR \
                  + months / MONTHS_PER_YEAR \
                  + quarters / QUARTERS_PER_YEAR \
                  + years

    # Then we will convert total_years into the equivalent number of
    # periods (or steps) for a DataFrame with the given frequency.
    # For each type of freq we will calculate the following:
    #   - periods: This is the number of steps to shift the DataFrame.
    #   - shifted_years: This is the actual number of years the
    #     DataFrame is shifted, which may be different from
    #     total_years due to rounding of the number of periods.
    #     This is used when calculating the annualized change.
    #     For example, if quarters=7 and freq='years' then
    #     total_years==1.75, but the data would actually get
    #     shifted 2 years due to rounding, so we need to use
    #     2 years instead of 1.75 years when calculating the
    #     annualized change in the rel_change() function.

    # Ensure the string with the freq argument is lower-case.
    freq = freq.lower()

    # DataFrame's frequency is Business or Trading Days.
    if freq in ['bdays', 'b']:
        periods = round(BDAYS_PER_YEAR * total_years)
        shifted_years = periods / BDAYS_PER_YEAR

    # DataFrame's frequency is Days (all 7 week-days).
    elif freq in ['days', 'd']:
        periods = round(DAYS_PER_YEAR * total_years)
        shifted_years = periods / DAYS_PER_YEAR

    # DataFrame's frequency is Weeks.
    elif freq in ['weeks', 'w']:
        periods = round(WEEKS_PER_YEAR * total_years)
        shifted_years = periods / WEEKS_PER_YEAR

    # DataFrame's frequency is Months.
    elif freq in ['months', 'm']:
        periods = round(MONTHS_PER_YEAR * total_years)
        shifted_years = periods / MONTHS_PER_YEAR

    # DataFrame's frequency is Quarters.
    elif freq in ['quarters', 'q']:
        periods = round(QUARTERS_PER_YEAR * total_years)
        shifted_years = periods / QUARTERS_PER_YEAR

    # DataFrame's frequency is Years.
    elif freq in ['years', 'y', 'annual', 'a']:
        periods = round(total_years)
        shifted_years = periods

    # Error.
    else:
        msg = 'Unsupported arg freq=\'{}\''.format(freq)
        raise ValueError(msg)

    # Convert periods to int, it should already be rounded to nearest number.
    periods = int(periods)

    return periods, shifted_years

##########################################################################

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

    WARNING: The DataFrame `df` is assumed to be sorted in ascending order
    on its date-index. Furthermore, the DataFrame is assumed to be complete
    in the sense that data is present for all time-steps at the given
    frequency. This function does not check that. The SimFin database ensures
    that quarterly and annual financial data such as Income Statements are
    all complete in this sense, but if you are using other data-sources,
    then you must ensure this yourself.

    It calculates the following when `future=True`:

    df_result[t] = df[t+periods] / df[t] - 1

    It calculates the following when `future=False`:

    df_result[t] = df[t] / df[t-periods] - 1

    Furthermore, we may calculate the annualized change instead, which is
    particularly useful when the time-interval is several years. For example,
    this can be used to calculate the Annualized Total Return on stocks.
    The variable `shifted_years` is the number of years corresponding to
    `periods` so the formula is as follows when `future=True`:

    df_result[t] = (df[t+periods] / df[t]) ** (1 / shifted_years) - 1

    And the formula is as follows when `future=False`:

    df_result[t] = (df[t] / df[t-periods]) ** (1 / shifted_years) - 1

    See Tutorial 03 for detailed examples on how to use this function.

    :param df:
        Pandas DataFrame or Series assumed to have either a DatetimeIndex
        or a MultiIndex with 2 indices, one of which is a DatetimeIndex
        and the other is given by the arg `group_index`.

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
        If True then df_result[t] = df[t+periods] / df[t] - 1
        If False then df_result[t] = df[t] / df[t-periods] - 1

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
    periods, shifted_years = _convert_to_periods(freq=freq, bdays=bdays,
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
        df_result.rename(columns=new_names, inplace=True)

    return df_result

##########################################################################
