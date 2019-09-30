# The Future of SimFin

## v. 0.2.0 (Private Beta)

### Goal

Make a "private" beta version with the basic features, that is good
enough for a small group of friends and experienced SimFin users to try out.

### Tasks

-   Check all column-names and update `names.py` (Magnus)
-   Split bulk-data into markets (usa, uk, de, etc.) and make API support
    for it using e.g. markets=usa (Thomas and Magnus)
-   Make API support for different data-columns e.g. columns=all/subset
    where free datasets have a subset of all the data-columns. Also try
    and find a more elegant solution. (Thomas and Magnus)
-   Fix the serious and obvious problems with the datasets e.g. negative
    Revenue. If it is too difficult to find the bug, then just black-list
    problematic companies for now, and re-include them in the future when
    the data has been fixed. (Thomas)
-   Make API support for datasets: 'income-banks', 'income-insurance', etc. (Magnus)
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
-   Extend the data-tests in `test_bulk_data.ipynb` and improve data
    quality. (Thomas)
-   Maybe include some of the features listed below.


## Future Versions

-   Helper-function for calculating per-share numbers e.g. Sales Per Share
    and Earnings Per Share.
-   Helper-function for calculating growth-rates e.g. Sales Growth.
-   Helper-function for calculating returns and annualized returns.
-   Tutorial for a simple stock-screener using 'shareprices-latest'
    and basic valuation ratios such as P/E, Sales Growth, and ROE.
