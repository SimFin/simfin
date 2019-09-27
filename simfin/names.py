##########################################################################
#
# Names that makes it easier to address individual data-columns.
# For example, you can write df[SGA] instead of
# df['Selling, General & Administrative'] to get the same data.
#
##########################################################################
# SimFin - Simple financial data for Python.
# www.simfin.com - www.github.com/simfin/simfin
# See README.md for instructions and LICENSE.txt for license details.
##########################################################################
# Names used in different datasets.

# Ticker for identifying a stock e.g. MSFT for Microsoft.
TICKER = 'Ticker'

# Unique ID for a company in the SimFin database. Useful if multiple
# companies have the same ticker at different points in time, or
# if a company does not have a ticker.
SIMFIN_ID = 'SimFinId'

# Currency for the data e.g. 'USD' for U.S. Dollar.
CURRENCY = 'Currency'

# Fiscal year for a financial report. This may not equal the calendar year.
FISCAL_YEAR = 'Fiscal Year'

# Fiscal period for a financial report e.g. 'Q1' for the 1st Quarter.
FISCAL_PERIOD = 'Fiscal Period'

# Date printed in a financial report e.g. 2018-12-31. This is not the date
# the information was available to the market, see PUBLISH_DATE for that.
REPORT_DATE = 'Report Date'

# Date that a financial report was available to the market. Some financial
# reports are restated and the standard datasets only use the newest data.
# For example, if a financial report for the fiscal period 2012-12-31 is
# originally published on e.g. 2013-01-21 but then restated on 2015-07-17
# then this latter date will be the one associated with the standard date.
# If you want the original report and all restatements, you need to access
# the special dataset designed for that.
PUBLISH_DATE = 'Publish Date'

# Date associated with the given data e.g. share-prices.
DATE = 'Date'

# Shares outstanding NOT adjusted for dilution from stock-options etc.
# Weighted average for the period. Adjusted for stock-splits.
SHARES_BASIC = 'Shares (Basic)'

# Shares outstanding adjusted for dilution from stock-options etc.
# Weighted average for the period. Adjusted for stock-splits.
SHARES_DILUTED = 'Shares (Diluted)'

##########################################################################
# Income Statement.
# https://simfin.com/data/help/main?topic=definitions

REVENUE = 'Revenue'
COST_GOODS_SOLD = 'Cost of Goods Sold'
GROSS_PROFIT = 'Gross Profit'
OPERATING_EXPENSES = 'Operating Expenses'
SGA = 'Selling, General & Administrative'
RESEARCH_DEV = 'Research & Development Expenses'
OPERATING_INCOME_EBIT = 'Operating Income (EBIT)'
INTEREST_EXPENSE_NET = 'Interest Expense (Net)'
PRETAX_INCOME_ADJ = 'Pretax Income (Adjusted)'
PRETAX_INCOME = 'Pretax Income'
INCOME_TAXES = 'Income Taxes'
INCOME_CONT_OP = 'Income from Continuing Operations'
NET_INCOME = 'Net Income'

##########################################################################
# Balance Sheet.

# Assets that are either cash or can be converted to cash.
CASH_EQUIV = 'Cash and Cash-equivalents'

# Assets for the money owed that customers owe the company for goods or
# services that have been sold but not yet paid for. Net of what???
RECEIVABLES = 'Receivables (Net)'

# Assets that are either cash, or expected to generate cash within a year.
CURRENT_ASSETS = 'Total Current Assets'

# Assets that are fixed property and production plants. These are historical
# values minus depreciation and may not reflect current or replacement values. ??? check this
PROPERTY_PLANT = 'Property, Plant and Equipment (Net)'

TOTAL_ASSETS = 'Total Assets'

ACCOUNTS_PAYABLE = 'Accounts Payable'
CURRENT_DEBT = 'Current Debt'
CURRENT_LIABILITIES = 'Total Current Liabilities'
NON_CURRENT_DEBT = 'Non-current Debt'
TOTAL_LIABILITIES = 'Total Liabilities'

PREFERRED_EQUITY = 'Preferred Equity'
COMMON_STOCK = 'Common Stock'
EQUITY_BEFORE_MINORITY = 'Equity Before Minorities'
MINORITY_INTEREST = 'Minority Interest'
TOTAL_EQUITY = 'Total Equity'

##########################################################################
# Cash-Flow Statement.

DEPRECIATION = 'Depreciation & Amortisation'
CHANGE_WORKING_CAPITAL = 'Change in Working Capital'
OPERATING_CASH_FLOW = 'Operating Cash Flow'

CHANGE_PPE_INTANGIBLES = 'Net Change in PP&E & Intangibles'
INVESTING_CASH_FLOW = 'Investing Cash Flow'

DIVIDENDS_PAID = 'Dividends Paid'
FINANCING_CASH_FLOW = 'Financing Cash Flow'

NET_CHANGE_CASH = 'Net Change in Cash'

##########################################################################
# Share-price.

# Daily share-price open. Adjusted for stock-splits but NOT dividends.
SHARE_PRICE_OPEN = OPEN = 'Open'

# Daily share-price high. Adjusted for stock-splits but NOT dividends.
SHARE_PRICE_HIGH = HIGH = 'High'

# Daily share-price low. Adjusted for stock-splits but NOT dividends.
SHARE_PRICE_LOW = LOW = 'Low'

# Daily share-price close. Adjusted for stock-splits but NOT dividends.
# This is used as the default share-price.
SHARE_PRICE = SHARE_PRICE_CLOSE = CLOSE = 'Close'

# Daily share-price close. Adjusted for BOTH stock-splits AND dividends, so
# dividends are reinvested back into the stock immediately, taxes are ignored.
# This is also known as the Total Return and is used to calculate stock-returns
# especially over longer time-periods where reinvestment of dividends can be
# a significant contribution to the overall return on a stock.
# This should NOT be used to calculate ratios such as P/E and P/Sales or
# technical indicators such as moving averages. Use SHARE_PRICE_CLOSE for that.
TOTAL_RETURN = SHARE_PRICE_ADJ_CLOSE = ADJ_CLOSE = 'Adj. Close'

# Number of shares traded during the day. Adjusted for stock-splits.
SHARE_VOLUME = 'Volume'

# Dividends paid per share, before taxes. Adjusted for stock-splits.
SHARE_DIVIDENDS = 'Dividends'

##########################################################################
# Company details.

# Name of a company e.g. 'Microsoft'.
COMPANY_NAME = 'Company Name'

##########################################################################
# Sector and Industry.

# Unique ID for an industry in the SimFin database.
INDUSTRY_ID = 'IndustryId'

# Name of the industry e.g. 'Consumer Cyclical'.
# ??? Rename to 'Industry Name'
INDUSTRY_NAME = 'Industry'

# Name of the sector e.g. 'Travel & Leisure'.
SECTOR = 'Sector'

##########################################################################
# Common names for derived data.

# Sales / Number of Shares.
SALES_PER_SHARE = 'Sales Per Share'

# Price / Earnings Ratio.
PE = 'P/E'

# Price / Sales Ratio.
PSALES = 'P/Sales'

# Net Income / Revenue.
NET_PROFIT_MARGIN = 'Net Profit Margin'

# Net Income / Total Assets.
ROA = 'Return on Assets'

# Net Income / Shareholder Equity.
ROE = 'Return on Equity'

##########################################################################
