# The Future of SimFin

## v. 0.2.0 (Private Beta)

### Goal

Make a "private" beta version with the basic features, that is good
enough for a small group of friends and experienced SimFin users to try out.

### Tasks

-   Check all column-names and update `names.py` (Magnus)
-   Split bulk-data into markets (usa, uk, de, etc.) and make API support
    for it using e.g. markets=usa (Thomas and Magnus)
-   <del>Make API support for different data-columns e.g. columns=all/subset
    where free datasets have a subset of all the data-columns. Also try
    and find a more elegant solution. (Thomas and Magnus)</del>
-   Fix the serious and obvious problems with the datasets e.g. negative
    Revenue. If it is too difficult to find the bug, then just black-list
    problematic companies for now, and re-include them in the future when
    the data has been fixed. (Thomas)
-   <del>Make API support for datasets: 'income-banks', 'income-insurance', etc. (Magnus)</del>
-   Make a new variant 'latest' of dataset 'shareprices' which only contains
    the data for the most recent trading day. This can be used to make a
    simple stock-screener, without having to download the entire dataset
    for shareprices every single day. (Thomas and Magnus)
-   Update Python API and tutorial with all the new features. (Magnus)


## v. 0.3.0 (Public Beta)

### Goal

Make a "public" beta version with the basic features, that is stable enough
for the general public to try out.

### Tasks

-   Fix errors reported in the "private" beta.

-   Create web-page on www.simfin.com with a list of available datasets
    and the difference between free / paid datasets (Thomas).
    Add link in tutorial and README.md (Magnus).

-   Find solution for handling duplicate tickers. Should the ticker be
    unique within a single market (e.g. all tickers for market=usa are
    unique)? Delisted tickers can be renamed XYZ1, XYZ2, etc. What
    about GOOG, is it an error it has two SIMFIN_ID's? (Thomas and Magnus)

-   <del>Allow sf.load_fundamentals() to index by SIMFIN_ID instead of TICKER?
    This is only really necessary if tickers are not always unique.
    How can it be done most elegantly? (Magnus)</del>

-   Document the most important names for data-columns in Income Statements,
    Balance Sheets, Cash-Flow Statements, etc. as found in `names.py`
    Either expand the existing web-page: https://simfin.com/data/help/main?topic=definitions
    or create a wiki on github. (Thomas) Add link to `names.py` (Magnus)
    
-   Extend the data-tests in `test_bulk_data.ipynb` and improve data
    quality. (Thomas)


## Feature Wishlist

-   Document the remaining names for data-columns in Income Statements,
    Balance Sheets, Cash-Flow Statements, etc. as found in `names.py`
    Either expand the existing web-page: https://simfin.com/data/help/main?topic=definitions
    or create a wiki on github. (Thomas)

-   Helper-function for calculating per-share numbers e.g. Sales Per Share
    and Earnings Per Share.

-   Helper-function for calculating growth-rates e.g. Sales Growth.

-   Helper-function for calculating returns and annualized returns.

-   Helper-functions for calculating ROA / ROE / Profit Margin / etc.

-   Tutorial for a simple stock-screener using 'shareprices-latest'
    and basic valuation ratios such as P/E, Sales Growth, and ROE.


## Dataset Wishlist

-   Other data from US SEC such as insider trading for companies, and
    the portfolios of hedge-funds.

-   Consumer Price Index (CPI) from https://www.bls.gov/cpi/data.htm
    It would be nice to have this in the SimFin database so it could
    be loaded with e.g. `sf.load_cpi(variant='all-urban-consumers')`

-   US Gov. Bond yields from e.g. https://www.federalreserve.gov/datadownload/Choose.aspx?rel=H15
    It might be a good idea to combine all the different bond maturities
    into a single CSV-file and give the columns descriptive names,
    instead of only having a single bond-maturity in each CSV-file.
