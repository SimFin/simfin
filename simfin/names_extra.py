##########################################################################
#
# Names that makes it easier to address individual data-columns.
#
# This supplements names.py which has been auto-generated from the SimFin
# database. This allows us to define more convenience names than are
# available in the SimFin database. This module is imported in names.py
# so all the names defined here will also be available from names.py
#
##########################################################################
# SimFin - Simple financial data for Python.
# www.simfin.com - www.github.com/simfin/simfin
# See README.md for instructions and LICENSE.txt for license details.
##########################################################################
# Per-Share Numbers.

# Sales / Number of Shares.
SPS = SALES_PER_SHARE = 'Sales Per Share'

# Net Income / Number of Shares.
EPS = EARNINGS_PER_SHARE = 'Earnings Per Share'

# Total Equity / Number of Shares.
EQ_PS = EQUITY_PER_SHARE = BV_PS = BOOK_VALUE_PER_SHARE = 'Equity Per Share'

# Free Cash Flow / Number of Shares.
FCF_PS = 'Free Cash Flow Per Share'

##########################################################################
# Valuation Signals.

# Price / Earnings Ratio.
PE = 'P/E'

# Price / Sales Ratio.
PSALES = 'P/Sales'

# Price / Free Cash Flow.
PFCF = 'P/FCF'

# Price / Book-Value (aka. Equity).
PBOOK = 'P/Book'

# Dividend TTM / Share-Price.
DIV_YIELD = 'Dividend Yield'

##########################################################################
# Financial Signals.

# Free Cash Flow.
FCF = 'Free Cash Flow'

# Net Income / Revenue.
NET_PROFIT_MARGIN = 'Net Profit Margin'

# Gross Profit / Revenue.
GROSS_PROFIT_MARGIN = 'Gross Profit Margin'

# Current Assets / Current Liabilities.
CURRENT_RATIO = 'Current Ratio'

# (Short-Term Debt + Long-Term Debt) / Total Assets
DEBT_RATIO = 'Debt Ratio'

# Net Income / Total Assets.
ROA = 'Return on Assets'

# Net Income / Shareholder Equity.
ROE = 'Return on Equity'

##########################################################################
# Growth Signals.

# Sales or Revenue Growth.
SALES_GROWTH = 'Sales Growth'
SALES_GROWTH_QOQ = 'Sales Growth QOQ'
SALES_GROWTH_YOY = 'Sales Growth YOY'

# Earnings or Net Income Growth.
EARNINGS_GROWTH = 'Earnings Growth'
EARNINGS_GROWTH_QOQ = 'Earnings Growth QOQ'
EARNINGS_GROWTH_YOY = 'Earnings Growth YOY'

# Free Cash Flow (FCF) Growth.
FCF_GROWTH = 'FCF Growth'
FCF_GROWTH_QOQ = 'FCF Growth QOQ'
FCF_GROWTH_YOY = 'FCF Growth YOY'

##########################################################################
# Price Signals.

# Moving Average.
MAVG_20 = 'MAVG 20'
MAVG_200 = 'MAVG 200'

# Exponential Moving Average.
EMA = 'EMA'

# Moving Average Convergence Divergence.
MACD = 'MACD'

# MACD with extra smoothing by Exp. Moving Average.
MACD_EMA = 'MACD-EMA'

# Latest trading-volume relative to its moving average.
REL_VOL = 'Relative Volume'

# Buy signal (typically a boolean value).
BUY = 'Buy'

# Sell signal (typically a boolean value).
SELL = 'Sell'

# Hold signal (typically a boolean value).
HOLD = 'Hold'

##########################################################################
