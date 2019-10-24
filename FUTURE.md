# The Future of SimFin

## v. 0.2.0 (Private Beta)

### Goal

Make a "private" beta version with the basic features, that is good
enough for a small group of friends and experienced SimFin users to try out.

### Tasks

-   <del>Check all column-names and update `names.py` (Magnus)</del>
-   <del>Split bulk-data into markets (usa, uk, de, etc.) and make API support
    for it using e.g. markets=usa (Thomas and Magnus)</del>
-   <del>Make API support for different data-columns e.g. columns=all/subset
    where free datasets have a subset of all the data-columns. Also try
    and find a more elegant solution. (Thomas and Magnus)</del>
-   Fix the serious and obvious problems with the datasets e.g. negative
    Revenue. If it is too difficult to find the bug, then just black-list
    problematic companies for now, and re-include them in the future when
    the data has been fixed. (Thomas)
-   <del>Make API support for datasets: 'income-banks', 'income-insurance', etc. (Magnus)</del>
-   <del>Make a new variant 'latest' of dataset 'shareprices' which only contains
    the data for the most recent trading day. This can be used to make a
    simple stock-screener, without having to download the entire dataset
    for shareprices every single day. (Thomas and Magnus)</del>
-   Update Python API and tutorial with all the new features. (Magnus)


## v. 0.3.0 (Private Beta)

### Goal

Improve and polish the "private" beta. It may not be ready for the
general public to try out yet.

### Tasks

-   **Both:** Fix errors reported by users for the previous version.

-   **Both:** Find solution for handling duplicate tickers. Should the ticker be
    unique within a single market (e.g. all tickers for market=us are
    unique)? Delisted tickers can be renamed XYZ1, XYZ2, etc. What
    about GOOG, is it an error it has the same ticker with two SIMFIN_ID's?

-   **Magnus:** Implement some of the helper-functions on the wishlist.

-   **Thomas:** Create a dataset with a CSV-file that contains a list of all
    available datasets with lists of their possible variants and markets.
    This could also be a json-file, but ideally it would be a CSV-file using
    the regular API for datasets, because it would make it easier for the
    Python API to save it to disk and reload it later.
    **Magnus:** Use it in `datasets.py` to load and iterate over all
    available datasets, variants and markets. And use that in
    `test_bulk.py` and `test_bulk_data.ipynb` etc.

-   **Thomas:** Write descriptions for the most important data-column names in:
    https://simfin.com/api/bulk_info/bulk_names.php
    Simply copy and edit the text from Investopedia and other websites such as:
    https://www.accountingtools.com/articles/early-extinguishment-of-debt.html
    Also add a json-field with `description_src` which is a link to the source.
    Maybe if you copy/write 10 descriptions per day, it won't be too boring and
    it will be done in a week or so, for all the 'free' data-columns.
    Remember to update `names.py` afterwards.

-   **Thomas:** Improve the web-page with overview of datasets:
    https://simfin.com/data/access/bulk

    - I think you are pre-generating the web-page now? That's great,
      because it loads very fast now! But please schedule the generation
      in the cron, so it is automatically done every day. We've made
      some changes to names and shortcuts that aren't currently shown.

    - All the available datasets should be shown e.g. 'markets', 'companies',
      'shareprices' and 'industries'.

    - Maybe if the market / dataset / variant are pulldown menus instead?
      There are already many in these lists, and there's going to be even
      more in the future.
      
    - Maybe remove "Total companies: 2,553" because it is only valid for some
      datasets e.g. in the future you may have currency-data and various
      economic indicators for inflation etc. If people want to see the number
      of companies they can click on the 'companies' dataset.

    - "Total time periods (number of rows in CSV): 66,102" is confusing.
      How about just: "Total rows in CSV-file: 66,102"
      
    - Table-column "Entries" is confusing. I think it would be better to name
      it "Coverage" and just report the percentage. This should be rounded up
      because you sometimes show e.g. 186 rows have the data but it's rounded
      down to 0% coverage, where it would be better to show 1% coverage. Just
      round them up to nearest integer.

    - We need a way to show the description, e.g. if you make a small (?)
      icon next to the Column Name when the description is available, and
      when I hover the mouser over the (?) icon it shows the description.
      The (?) icon should probably be to the right of the "Column Name".
      The header of that table-column could be Help or About. I think
      "Description" is too long.

    - The table-column "Availability" could perhaps be renamed to "Free"
      or something like that. It should also be moved so it is all the
      way to the right of the table. That makes it easier for people to
      see how much more data they would get if they paid for SimFin+.
      Perhaps write Free or SF+ instead of SimFin+ on every line, because
      some people like me are only using small laptop monitors.

    - The explanation above the table is good. Perhaps a minor revision
      would improve it slightly for all the above changes:
      "The table shows all the available data-columns for this dataset
      with explanations and Python shortcuts. The percentage coverage
      shows how many rows in the CSV-file have that data. The table also shows
      whether each data-column is included in the free dataset or requires
      a paid SimFin+ subscription (these words should be a link to your
      subscription page)."
      
    - Perhaps change the header from: "Bulk Download v. 2.0 - Overview"
      to just "SimFin Bulk Datasets".

    - Perhaps remove: "Please select the market, the dataset and the variant
      (applicable time periods) for an overview of the available data."
      This is probably self-explanatory.

    - Perhaps change the text: "Endpoint for selected dataset:"
      Maybe something like this: "All the datasets can be downloaded
      easily using the Python API (link to github). The selected dataset
      can also be downloaded as a Zipped CSV-file (link to the API endpoint)."
      I don't think the full url should be shown. The only reason people
      need the url, is if they want to build an API for another language,
      but then they're probably clever enough to get the url.

-   **Thomas:** Extend the data-tests in `test_bulk_data.ipynb` and improve data
    quality.


## Feature Wishlist

-   Write descriptions for the remaining data-columns in:
    https://simfin.com/api/bulk_info/bulk_names.php

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
