##########################################################################
#
# Functions for calculating signals from share-prices and financial data.
#
##########################################################################
# SimFin - Simple financial data for Python.
# www.simfin.com - www.github.com/simfin/simfin
# See README.md for instructions and LICENSE.txt for license details.
##########################################################################

import pandas as pd
import numpy as np

from simfin.resample import reindex
from simfin.rel_change import rel_change
from simfin.utils import apply, add_date_offset
from simfin.transform import free_cash_flow
from simfin.names import *

##########################################################################

def price_signals(df_prices, group_index=TICKER):
    """
    Calculate price-signals such as Moving Average and MACD for all stocks
    in the given DataFrame.

    :param df_prices:
        Pandas DataFrame with share-prices for multiple stocks.

    :param group_index:
        If the DataFrame has a MultiIndex then group data using this
        index-column. By default this is TICKER but it could also be e.g.
        SIMFIN_ID if you are using that as an index in your DataFrame.

    :return:
        Pandas DataFrame with price-signals.
    """

    # Helper-function for calculating signals for a single stock.
    def _signals(df_prices):
        # Create new DataFrame for the signals.
        df_signals = pd.DataFrame()

        # Get the closing share-price and trading volume.
        df_price = df_prices[CLOSE]
        df_volume = df_prices[VOLUME]

        # Moving Average for past 20 days.
        df_signals[MAVG_20] = df_price.rolling(window=20).mean()

        # Moving Average for past 200 days.
        df_signals[MAVG_200] = df_price.rolling(window=200).mean()

        # Exponential Moving Average for past 20 days.
        df_signals[EMA] = df_price.ewm(span=20).mean()

        # Moving Average Convergence Divergence for 12 and 26 days.
        # https://en.wikipedia.org/wiki/MACD
        df_signals[MACD] = df_price.ewm(span=12).mean() \
                         - df_price.ewm(span=26).mean()

        # MACD with extra smoothing by Exp. Moving Average for 9 days.
        df_signals[MACD_EMA] = df_signals[MACD].ewm(span=9).mean()

        # Last trading volume relative to 20-day moving average.
        df_rel_vol = df_volume / df_volume.rolling(window=20).mean()
        df_signals[REL_VOL] = np.log(df_rel_vol)

        return df_signals

    # Calculate signals and use Pandas groupby if `df` has multiple stocks.
    df_signals = apply(df=df_prices, func=_signals, group_index=group_index)

    # Sort the columns by their names.
    df_signals.sort_index(axis='columns', inplace=True)

    return df_signals

##########################################################################

def trig_signals(df, signal1, signal2, group_index=TICKER):
    """
    Create Buy / Sell / Hold signals from two signals in the given DataFrame.

    If df[signal1] >= df[signal2] create a Hold signal.
    If df[signal1] crosses above df[signal2] create a Buy signal.
    if df[signal1] crosses below df[signal2] create a Sell signal.

    :param df:
        Pandas DataFrame with columns `signal1` and `signal2`.
        May contain data for one or more stocks.

    :param signal1:
        String with the name of a column in `df`.

    :param signal2:
        String with the name of a column in `df`.

    :param group_index:
        If the DataFrame has a MultiIndex then group data using this
        index-column. By default this is TICKER but it could also be e.g.
        SIMFIN_ID if you are using that as an index in your DataFrame.

    :return:
        Pandas Dataframe with BUY, SELL, HOLD signals.
    """

    # Helper-function for calculating signals for a single stock.
    def _signals(df):
        # Create new DataFrame for the signals.
        df_signals = pd.DataFrame()

        # Boolean whether signal1 >= signal2.
        df_above = (df[signal1] >= df[signal2])

        # Boolean whether to buy the stock.
        df_signals[BUY] = df_above & ~df_above.shift(1, fill_value=True)

        # Boolean whether to sell the stock.
        df_signals[SELL] = ~df_above & df_above.shift(1, fill_value=False)

        # Boolean whether to keep holding the stock.
        df_signals[HOLD] = df_above

        return df_signals

    # Calculate signals and use Pandas groupby if `df` has multiple stocks.
    df_signals = apply(df=df, func=_signals, group_index=group_index)

    # Sort the columns by their names.
    df_signals.sort_index(axis='columns', inplace=True)

    return df_signals

##########################################################################

def fin_signals(df_income_ttm, df_balance_ttm, df_prices=None,
                offset=None, func=None, fill_method='ffill',
                date_index=REPORT_DATE, group_index=TICKER):
    """
    Calculate financial signals such as Net Profit Margin, Debt Ratio, ROA,
    etc. for all stocks in the given DataFrames.

    :param df_prices:
        Optional Pandas DataFrame with share-prices for one or more stocks.
        If not None, then the signals will be reindexed to the same daily
        data-points as `df_prices`, otherwise the signals will be quarterly.

    :param df_income_ttm:
        Pandas DataFrame with Income Statement TTM data for one or more stocks.

    :param df_balance_ttm:
        Pandas DataFrame with Balance Sheet TTM data for one or more stocks.

    :param df_cashflow_ttm:
        Pandas DataFrame with Cash-Flow Statement TTM data for one or more stocks.

    :param func:
        Function to apply on a per-stock basis after the signals have been
        calculated, but before they have been reindexed to daily data-points.
        This is useful e.g. to calculate multi-year averages.
        For example, to calculate the 2-year averages of TTM data:

            `func = lambda df: 0.5 * (df + df.shift(4))`

    :param fill_method:
        String or callable for the method of filling in empty values when
        reindexing financial data to daily data-points. See `sf.reindex`
        for valid options.

    :param offset:
        Pandas DateOffset added to the date-index of the Pandas DataFrames with
        the financial data. Example: `pd.DateOffset(days=60)` This is useful if
        you want to add a lag of e.g. 60 days to the dates of financial reports
        with Income Statements, Balance Sheets, and Cash-Flow Statements, because
        the REPORT_DATE is not when it was actually made available to the public,
        which can be 1, 2 or even 3 months after the REPORT_DATE.
        See `sf.add_date_offset` for more details.

    :param date_index:
        Name of the date-column for the financial data e.g. REPORT_DATE.

    :param shares_index:
        String with the column-name for the share-counts. SHARES_DILUTED
        takes the potential diluting impact of stock-options into account, so
        it results in more conservative valuation ratios than SHARES_BASIC.

    :param group_index:
        If the DataFrames have a MultiIndex then group data using this
        index-column. By default this is TICKER but it could also be e.g.
        SIMFIN_ID if you are using that as an index in your DataFrame.

    :return:
        Pandas DataFrame with financial signals.
    """

    # Helper-function for calculating signals for a single stock.
    def _signals(df):
        # Create new DataFrame for the signals.
        df_signals = pd.DataFrame()

        # Net Profit Margin.
        df_signals[NET_PROFIT_MARGIN] = df[NET_INCOME] / df[REVENUE]

        # Gross Profit Margin.
        df_signals[GROSS_PROFIT_MARGIN] = df[GROSS_PROFIT] / df[REVENUE]

        # Current Ratio = Current Assets / Current Liabilities.
        df_signals[CURRENT_RATIO] = df[TOTAL_CUR_ASSETS] / df[TOTAL_CUR_LIAB]

        # Debt Ratio = (Short-term Debt + Long-term Debt) / Total Assets.
        df_signals[DEBT_RATIO] = (df[ST_DEBT] + df[LT_DEBT]) / df[TOTAL_ASSETS]

        # Return on Assets = Net Income / Total Assets from 1 year ago.
        df_signals[ROA] = df[NET_INCOME] / df[TOTAL_ASSETS].shift(4)

        # Return on Equity = Net Income / Total Equity from 1 year ago.
        df_signals[ROE] = df[NET_INCOME] / df[TOTAL_EQUITY].shift(4)

        return df_signals

    # Get relevant data from Income Statements.
    columns = [REVENUE, GROSS_PROFIT, NET_INCOME]
    df1 = df_income_ttm[columns]

    # Get relevant data from Balance Sheets.
    columns = [TOTAL_ASSETS, TOTAL_CUR_ASSETS, TOTAL_CUR_LIAB, TOTAL_EQUITY,
               ST_DEBT, LT_DEBT]
    df2 = df_balance_ttm[columns]

    # Combine the data into a single DataFrame.
    df = pd.concat([df1, df2], axis=1)

    # Add offset / lag to the index-dates of the financial data.
    if offset is not None:
        df = add_date_offset(df=df, offset=offset, date_index=date_index)

    # Calculate signals and use Pandas groupby if `df` has multiple stocks.
    df_signals = apply(df=df, func=_signals, group_index=group_index)

    # Process the signals using the supplied function e.g. to calculate averages.
    if func is not None:
        df_signals = apply(df=df_signals, func=func, group_index=group_index)

    # Reindex to the same daily data-points as the share-prices.
    if df_prices is not None:
        df_signals = reindex(df_src=df_signals, df_target=df_prices,
                             method=fill_method)

    # Sort the columns by their names.
    df_signals.sort_index(axis='columns', inplace=True)

    return df_signals

##########################################################################

def growth_signals(df_income_ttm, df_income_qrt,
                   df_cashflow_ttm, df_cashflow_qrt,
                   df_prices=None, fill_method='ffill',
                   offset=None, func=None,
                   date_index=REPORT_DATE, group_index=TICKER):
    """
    Calculate growth-signals such as Sales Growth, Earnings Growth, etc.
    for all stocks in the given DataFrames.

    Three growth-signals are given for each type of financial data, e.g.:

    - SALES_GROWTH is calculated from the TTM Revenue divided by the
      TTM Revenue from one year ago.

    - SALES_GROWTH_YOY is calculated from the Quarterly Revenue divided by
      the Quarterly Revenue from one year ago.

    - SALES_GROWTH_QOQ is calculated from the Quarterly Revenue divided by
      the Quarterly Revenue from the previous quarter.

    :param df_prices:
        Optional Pandas DataFrame with share-prices for one or more stocks.
        If not None, then the signals will be reindexed to the same daily
        data-points as `df_prices`, otherwise the signals will be quarterly.

    :param df_income_ttm:
        Pandas DataFrame with Income Statement TTM data for one or more stocks.

    :param df_income_qrt:
        Pandas DataFrame with Income Statement Quarterly data for one or more
        stocks.

    :param df_cashflow_ttm:
        Pandas DataFrame with Cash-Flow Statement TTM data for one or more
        stocks.

    :param df_cashflow_qrt:
        Pandas DataFrame with Cash-Flow Statement Quarterly data for one or
        more stocks.

    :param func:
        Function to apply on a per-stock basis after the signals have been
        calculated, but before they have been reindexed to daily data-points.
        This is useful e.g. to calculate multi-year averages.
        For example, to calculate the 2-year averages of TTM data:

            `func = lambda df: 0.5 * (df + df.shift(4))`

    :param fill_method:
        String or callable for the method of filling in empty values when
        reindexing financial data to daily data-points. See `sf.reindex`
        for valid options.

    :param offset:
        Pandas DateOffset added to the date-index of the Pandas DataFrames with
        the financial data. Example: `pd.DateOffset(days=60)` This is useful if
        you want to add a lag of e.g. 60 days to the dates of financial reports
        with Income Statements, Balance Sheets, and Cash-Flow Statements, because
        the REPORT_DATE is not when it was actually made available to the public,
        which can be 1, 2 or even 3 months after the REPORT_DATE.
        See `sf.add_date_offset` for more details.

    :param date_index:
        Name of the date-column for the financial data e.g. REPORT_DATE.

    :param shares_index:
        String with the column-name for the share-counts. SHARES_DILUTED
        takes the potential diluting impact of stock-options into account, so
        it results in more conservative valuation ratios than SHARES_BASIC.

    :param group_index:
        If the DataFrames have a MultiIndex then group data using this
        index-column. By default this is TICKER but it could also be e.g.
        SIMFIN_ID if you are using that as an index in your DataFrame.

    :return:
        Pandas DataFrame with growth signals.
    """

    # This implementation uses sf.rel_change() to calculate the growth-rates,
    # which means that several groupby operations are performed. But this is
    # easier to implement and for large DataFrames it is only about 10% slower
    # than using sf.apply() with a function like _signals() in fin_signals().

    ###############################
    # Annual growth using TTM data.

    # Select and combine the data we need.
    df_ttm1 = df_income_ttm[[REVENUE, NET_INCOME]]
    df_ttm2 = free_cash_flow(df_cashflow_ttm)
    df_ttm = pd.concat([df_ttm1, df_ttm2], axis=1)

    # Dict mapping to the new column-names.
    new_names = {REVENUE: SALES_GROWTH,
                 NET_INCOME: EARNINGS_GROWTH,
                 FCF: FCF_GROWTH}

    # Calculate the growth-rates.
    df_growth = rel_change(df=df_ttm, freq='q', quarters=4,
                           future=False, annualized=False,
                           new_names=new_names)

    #############################################
    # Year-Over-Year growth using Quarterly data.

    # Select and combine the data we need.
    df_qrt1 = df_income_qrt[[REVENUE, NET_INCOME]]
    df_qrt2 = free_cash_flow(df_cashflow_qrt)
    df_qrt = pd.concat([df_qrt1, df_qrt2], axis=1)

    # Dict mapping to the new column-names.
    new_names = {REVENUE: SALES_GROWTH_YOY,
                 NET_INCOME: EARNINGS_GROWTH_YOY,
                 FCF: FCF_GROWTH_YOY}

    # Calculate the growth-rates.
    df_growth_yoy = rel_change(df=df_qrt, freq='q', quarters=4,
                               future=False, annualized=False,
                               new_names=new_names)

    ########################################################
    # Quarter-Over-Quarter growth using Quarterly data.
    # Note: This uses the same Quarterly DataFrame as above.

    # Dict mapping to the new column-names.
    new_names = {REVENUE: SALES_GROWTH_QOQ,
                 NET_INCOME: EARNINGS_GROWTH_QOQ,
                 FCF: FCF_GROWTH_QOQ}

    # Calculate the growth-rates.
    df_growth_qoq = rel_change(df=df_qrt, freq='q', quarters=1,
                               future=False, annualized=False,
                               new_names=new_names)

    ##################
    # Post-processing.

    # Combine into a single DataFrame.
    df_signals = pd.concat([df_growth, df_growth_yoy, df_growth_qoq], axis=1)

    # Add offset / lag to the index-dates of the signals.
    if offset is not None:
        df_signals = add_date_offset(df=df_signals, offset=offset,
                                     date_index=date_index)

    # Process the signals using the supplied function e.g. to calculate averages.
    if func is not None:
        df_signals = apply(df=df_signals, func=func, group_index=group_index)

    # Reindex to the same daily data-points as the share-prices.
    if df_prices is not None:
        df_signals = reindex(df_src=df_signals, df_target=df_prices,
                             method=fill_method)

    # Sort the columns by their names.
    df_signals.sort_index(axis='columns', inplace=True)

    return df_signals

##########################################################################

def val_signals(df_prices, df_income_ttm, df_balance_ttm, df_cashflow_ttm,
                fill_method='ffill', offset=None, func=None,
                date_index=REPORT_DATE, shares_index=SHARES_DILUTED,
                group_index=TICKER):
    """
    Calculate valuation signals such as P/E and P/Sales ratios for all stocks
    in the given DataFrames.

    :param df_prices:
        Pandas DataFrame with share-prices for one or more stocks.

    :param df_income_ttm:
        Pandas DataFrame with Income Statement TTM data for one or more stocks.

    :param df_balance_ttm:
        Pandas DataFrame with Balance Sheet TTM data for one or more stocks.

    :param df_cashflow_ttm:
        Pandas DataFrame with Cash-Flow Statement TTM data for one or more stocks.

    :param fill_method:
        String or callable for the method of filling in empty values when
        reindexing financial data to daily data-points. See `sf.reindex`
        for valid options.

    :param offset:
        Pandas DateOffset added to the date-index of the Pandas DataFrames with
        the financial data. Example: `pd.DateOffset(days=60)` This is useful if
        you want to add a lag of e.g. 60 days to the dates of financial reports
        with Income Statements, Balance Sheets, and Cash-Flow Statements, because
        the REPORT_DATE is not when it was actually made available to the public,
        which can be 1, 2 or even 3 months after the REPORT_DATE.
        See `sf.add_date_offset` for more details.

    :param func:
        Function to apply on a per-stock basis on the financial data, before
        calculating the valuation signals. This is useful e.g. to calculate
        multi-year averages of the Net Income and Revenue and use those when
        calculating P/E and P/Sales ratios.
        For example, to calculate the 2-year averages of TTM data:

            `func = lambda df: 0.5 * (df + df.shift(4))`

    :param date_index:
        Name of the date-column for the financial data e.g. REPORT_DATE.

    :param shares_index:
        String with the column-name for the share-counts. SHARES_DILUTED
        takes the potential diluting impact of stock-options into account, so
        it results in more conservative valuation ratios than SHARES_BASIC.

    :param group_index:
        If the DataFrames have a MultiIndex then group data using this
        index-column. By default this is TICKER but it could also be e.g.
        SIMFIN_ID if you are using that as an index in your DataFrame.

    :return:
        Pandas DataFrame with valuation signals.
    """

    # Create a DataFrame with the financial data we need.
    # Start by copying data from the Income Statements.
    df = df_income_ttm[[REVENUE, NET_INCOME_COMMON, shares_index]].copy()

    # Add Shareholder's Equity as a new column to the DataFrame.
    df[TOTAL_EQUITY] = df_balance_ttm[TOTAL_EQUITY]

    # Add Dividends Paid as a new column to the DataFrame.
    df[DIVIDENDS_PAID] = df_cashflow_ttm[DIVIDENDS_PAID]

    # Calculate FCF and add it as a new column to the DataFrame.
    df[FCF] = free_cash_flow(df_cashflow_ttm)

    # Add offset / lag to the index-dates of the financial data.
    if offset is not None:
        df = add_date_offset(df=df, offset=offset, date_index=date_index)

    # Copy the number of shares before applying the user-supplied function,
    # which might change this number in the DataFrame.
    shares = df[shares_index].copy()

    # Process the financial data using the user-supplied function
    # e.g. to calculate multi-year averages of Earnings, Sales, etc.
    if func is not None:
        df = apply(df=df, func=func, group_index=group_index)

    # Calculate Per-Share numbers. It is important to use the share-count
    # from before the user-supplied function was applied.
    df_per_share = df.div(shares, axis=0)

    # Reindex the per-share financial data to daily data-points.
    df_daily = reindex(df_src=df_per_share, df_target=df_prices,
                       method=fill_method, group_index=group_index)

    # Create new DataFrame for the signals.
    df_signals = pd.DataFrame()

    # Use the closing share-price for all the valuation signals.
    df_price = df_prices[CLOSE]

    # Calculate signals.
    df_signals[PSALES] = df_price / df_daily[REVENUE]
    df_signals[PE] = df_price / df_daily[NET_INCOME_COMMON]
    df_signals[PFCF] = df_price / df_daily[FCF]
    df_signals[PBOOK] = df_price / df_daily[TOTAL_EQUITY]

    # Calculate Dividend Yield using Cash-Flow data.
    # Note the negation because DIVIDENDS_PAID is negative.
    df_signals[DIV_YIELD] = -df_daily[DIVIDENDS_PAID] / df_price

    # Sort the columns by their names.
    df_signals.sort_index(axis='columns', inplace=True)

    return df_signals

##########################################################################
