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

#: Sales / Number of Shares.
SPS = SALES_PER_SHARE = 'Sales Per Share'

#: Net Income / Number of Shares.
EPS_BASIC = EPS = EARNINGS_PER_SHARE = 'Earnings per Share, Basic'

#: Net Income / Number of Shares.
EPS_DILUTED = 'Earnings per Share, Diluted'

#: Total Equity / Number of Shares.
EQ_PS = EQUITY_PER_SHARE = BV_PS = BOOK_VALUE_PER_SHARE = 'Equity Per Share'

#: Free Cash Flow / Number of Shares.
FCF_PS = 'Free Cash Flow Per Share'

#: Dividends / Number of Shares.
DPS = DIVIDENDS_PS = 'Dividends Per Share'

##########################################################################
# Valuation Signals.

#: Price / Earnings Ratio.
P_E = PE = 'P/E'

#: Price / Earnings Ratio., quarterly and ttm variants
PE_QUARTERLY = 'Price to Earnings Ratio (quarterly)'
PE_TTM = 'Price to Earnings Ratio (ttm)'

#: Price / Book-Value (aka. Equity).
P_BOOK = PBOOK = PB = PRICE_BOOK = 'Price to Book Value'

#: Enterprise Value
EV = ENTERPRISE_VALUE = 'Enterprise Value'

#: Enterprise Value / EBITDA
EV_EBITDA = 'EV/EBITDA'

#: Enterprise Value / Sales
EV_SALES = 'EV/Sales'

#: Enterprise Value / FCF
EV_FCF = 'EV/FCF'

#: Book to market value
BOOK_MARKET = 'Book to Market Value'

#: Operating Income to EV
OP_INCOME_EV = 'Operating Income/EV'

#: Price / Sales Ratio.
P_SALES = PSALES = 'P/Sales'

#: Price / Sales Ratio., quarterly and ttm variants
PS_QUARTERLY = 'Price to Sales Ratio (quarterly)'
PS_TTM = 'Price to Sales Ratio (ttm)'

#: Price / Free Cash Flow.
P_FCF = PFCF = 'P/FCF'

#: Price / Free Cash Flow., quarterly and ttm variants
PRICE_FCF_QUARTERLY = P_FCF_QUARTERLY = 'Price to Free Cash Flow (quarterly)'
PRICE_FCF_TTM = P_FCF_TTM = 'Price to Free Cash Flow (ttm)'

#: Price / Net Current Asset Value (NCAV).
#: Where NCAV = Current Assets - Total Liabilities.
#: This formula is attributed to Ben Graham (Warren Buffett's teacher).
#: It compares the share-price relative to an estimated liquidation value,
#: which may be overestimated because the Current Assets may not be sold at
#: their actual book-value. The P_NETNET ratio is a more conservative estimate.
P_NCAV = PNCAV = 'P/NCAV'

#: Net Current Asset Value (see P_NCAV for more explanation).
NCAV = 'Net Current Asset Value (NCAV)'

#: Price / NetNet Working Capital (NetNet aka. NNWC).
#: Where NetNet = Cash & Equiv. + 0.75 * Receivables
#:              + 0.5 * Inventory - Total Liabilities.
#: This formula is attributed to Ben Graham (Warren Buffett's teacher).
#: It compares the share-price relative to an estimated liquidation value.
#: This is more conservative than P_NCAV because Receivables and Inventories
#: are not fully counted in the estimate of the liquidation value.
P_NETNET = PNETNET = P_NNWC = PNNWC = 'P/NetNet'

#: NetNet Working Capital (see P_NETNET for more explanation).
NETNET = 'NetNet Working Capital'

#: Price / (Cash + Equivalents + Short-Term Investments)
#: This can be used to screen for companies that might be takeover targets.
P_CASH = PCASH = 'P/Cash'

#: Earnings / Price.
EARNINGS_YIELD = 'Earnings Yield'

#: FCF / Price.
FCF_YIELD = 'FCF Yield'

#: Dividend TTM / Share-Price.
DIV_YIELD = DIVIDEND_YIELD = 'Dividend Yield'

#: Market Capitalization = Shares Outstanding * Share-Price.
MCAP = MARKET_CAP = 'Market-Cap'

##########################################################################
# Financial Signals.

#: Total debt: short term debt + long term debt
TOTAL_DEBT = DEBT = 'Total Debt'

#: Free Cash Flow.
FCF = 'Free Cash Flow'

#: Earnings Before Interest, Taxes, Depreciation & Amortization.
EBITDA = 'EBITDA'

#: Net Income / Revenue.
NET_PROFIT_MARGIN = NP_MARGIN = 'Net Profit Margin'

#: Gross Profit / Revenue.
GROSS_PROFIT_MARGIN = GROSS_MARGIN = 'Gross Profit Margin'

#: Operating Margin
OP_MARGIN = OPERATING_MARGIN = 'Operating Margin'

#: Research & Development / Revenue.
RD_REVENUE = 'R&D / Revenue'

#: Research & Development / Gross Profit.
RD_GROSS_PROFIT = 'R&D / Gross Profit'

#: Gross Profit / Research & Development.
RORC = 'Return on Research Capital'

#: Operating Income / Interest Expense, Net.
INTEREST_COV = INTEREST_COVERAGE = 'Interest Coverage'

#: Current Assets / Current Liabilities.
CURRENT_RATIO = 'Current Ratio'

#: (Cash + Equiv. + Short-Term Inv. + Receivables) / Current Liabilities.
QUICK_RATIO = 'Quick Ratio'

#: (Short-Term Debt + Long-Term Debt) / Total Assets
DEBT_RATIO = DEBT_ASSETS = 'Debt Ratio'

#: Liabilities to Equity Ratio
LIABILITIES_EQUITY = 'Liabilities to Equity Ratio'

#: Dividends / Free Cash Flow
PAYOUT_RATIO = 'Dividends / FCF'

#: (Dividends + Share Buybacks) / Free Cash Flow
PAYOUT_BUYBACK_RATIO = '(Dividends + Share Buyback) / FCF'

#: Share Buybacks / Free Cash Flow
BUYBACK_RATIO = 'Share Buyback / FCF'

#: Net Income / Total Assets.
ROA = 'Return on Assets'

#: Net Income / Shareholder Equity.
ROE = 'Return on Equity'

#: Revenue / Total Assets.
ASSET_TURNOVER = 'Asset Turnover'

#: Revenue / Inventory.
INVENTORY_TURNOVER = 'Inventory Turnover'

#: Net Acquisitions & Divestitures / Total Assets.
ACQ_ASSETS_RATIO = 'Net Acquisitions / Total Assets'

#: Capital Expenditures / (Depreciation + Amortization).
CAPEX_DEPR_RATIO = 'CapEx / (Depr + Amor)'

#: Log10(Revenue).
LOG_REVENUE = 'Log Revenue'

#: Free Cash Flow to Net Income
FCF_NET_INCOME = "Free Cash Flow to Net Income"

#: Pietroski F-Score
PIETROSKI = 'Pietroski F-Score'

##########################################################################
# Growth Signals.

#: Sales or Revenue Growth.
SALES_GROWTH = 'Sales Growth'
SALES_GROWTH_QOQ = 'Sales Growth QOQ'
SALES_GROWTH_YOY = 'Sales Growth YOY'

#: Earnings or Net Income Growth.
EARNINGS_GROWTH = 'Earnings Growth'
EARNINGS_GROWTH_QOQ = 'Earnings Growth QOQ'
EARNINGS_GROWTH_YOY = 'Earnings Growth YOY'

#: Free Cash Flow (FCF) Growth.
FCF_GROWTH = 'FCF Growth'
FCF_GROWTH_QOQ = 'FCF Growth QOQ'
FCF_GROWTH_YOY = 'FCF Growth YOY'

#: Total Assets Growth.
ASSETS_GROWTH = 'Assets Growth'
ASSETS_GROWTH_QOQ = 'Assets Growth QOQ'
ASSETS_GROWTH_YOY = 'Assets Growth YOY'

##########################################################################
# Price Signals.

#: Moving Average.
MAVG_20 = 'MAVG 20'
MAVG_200 = 'MAVG 200'

#: Exponential Moving Average.
EMA = 'EMA'

#: Moving Average Convergence Divergence.
MACD = 'MACD'

#: MACD with extra smoothing by Exp. Moving Average.
MACD_EMA = 'MACD-EMA'

#: Buy signal (typically a boolean value).
BUY = 'Buy'

#: Sell signal (typically a boolean value).
SELL = 'Sell'

#: Hold signal (typically a boolean value).
HOLD = 'Hold'

##########################################################################
# Volume Signals.

#: Daily trading-volume relative to its moving average.
REL_VOL = 'Relative Volume'

#: Market-Capitalization of the daily trading-volume.
#: Defined as: Volume x Share-Price.
VOL_MCAP = VOLUME_MCAP = 'Volume Market-Cap'

#: Daily trading-volume relative to the number of shares outstanding.
#: Defined as: Volume / Shares Outstanding
VOL_TURN = VOLUME_TURNOVER = 'Volume Turnover'

##########################################################################
# Other
#: Shares outstanding as per last available date for the 'shareprices' dataset.
SHARES_OUTSTANDING = 'Shares Outstanding'
