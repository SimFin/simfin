# The Future of SimFin

## v. 0.4.0 (Public Beta)

### Goal

A beta version that is ready for the general public.

### Tasks

-   <del>**Magnus:** Generate docs using sphinx or another system.</del>  

-   <del>**Magnus:** Setup automatic testing using GitHub Actions.</del>

-   **Thomas:** Fix erroneous share-counts in the data.
    Or "blacklist" the companies until they can be checked and fixed.

-   **Thomas:** Make datasets with signals (P/E ratios etc.)
    **Magnus:** create `load`-functions for them. **NOTE:** I have mixed
    feelings about this. It is a good idea, but the json/database-system
    for defining the data-columns and their shortcuts and descriptions is
    pretty F'd up, so I am worried if it is going to destroy something,
    as happened with `SHARE_PRICE` last week that was suddenly just gone.

-   **Thomas:** You ought to change www.simfin.com so the API-page does not
    require login. This may help getting more users. You should use the
    design suggestions I wrote in a previous e-mail.
    
-   **Thomas:** You ought to change the subscription to only have a single paid
    level and price it at EUR 20 per month. This may help getting more paying
    users.

-   **Thomas:** Consider delaying the free data for 12 months instead of only
    4, to make a greater incitement for users to pay the EUR 20 per month.

-   **Thomas**: Log all bulk downloads and create a simple statistics page.
    You can create the statistics page later, but you should start logging
    now.

-   **Thomas:** Merge financial data for GOOG and GOOG_OLD, so it is just
    one company in the database. Is it the same problem for other companies?
    GOOG is such an important company that a lot of people would expect
    is in the database. It is weird that it is split into two companies
    in the database, just because it changed its name. 

-   **Thomas:** Write descriptions for the most important data-column names in:
    https://simfin.com/api/bulk_info/columns.php
    Simply copy and edit the text from Investopedia and other websites such as:
    https://www.accountingtools.com/articles/early-extinguishment-of-debt.html
    Also add a json-field with `description_src` which is a link to the source.
    Maybe if you copy/write 10 descriptions per day, it won't be too boring and
    it will be done in a week or so, for all the 'free' data-columns.
    Remember to update `names.py` afterwards.


## Feature Wishlist

-   Write descriptions for the remaining data-columns in:
    https://simfin.com/api/bulk_info/columns.php

-   Make more unit-tests, especially for `resample.py` and `rel_change.py`
    using synthetic data, so it can be tested that it computes correctly.
    Setup GitHub Actions for automated unit-testing. This should be triggered
    on both Push and Pull Requests. Because it only uses synthetic data,
    it should be very fast.

-   Implement function sf.mean_change() which is similar to mean_log_change()
    except it can calculate actual annualized returns, instead of log-returns.
    This must probably be a for-loop implementation with numba.jit for speed.

-   Parallel implementation of `sf.apply()`


## Dataset Wishlist

-   Add datasets with e.g. Point-In-Time (PIT) data such as [Compustat](https://wrds-www.wharton.upenn.edu/pages/support/data-overview/overview-compustat-preliminary-unrestated-and-point-time-datasets/)
    Should this be another dataset-variant? Or should the main datasets just be PIT?

-   Share-prices for selected ETF's. These would be a good proxy for e.g.
    large-cap, mid-cap and small-cap stock indices. It is also easier to
    calculate the Total Return for ETF-data, because ETF dividends are paid
    as if it was a regular stock.

-   Other data from US SEC such as insider trading for companies, and
    the portfolios of hedge-funds.

-   Consumer Price Index (CPI) from https://www.bls.gov/cpi/data.htm
    It would be nice to have this in the SimFin database so it could
    be loaded with e.g. `sf.load_cpi(variant='all-urban-consumers')`
    
-   Other economic data such as unemployment rates, housing-prices, etc. 

-   US Gov. Bond yields from e.g. https://www.federalreserve.gov/datadownload/Choose.aspx?rel=H15
    It might be a good idea to combine all the different bond maturities
    into a single CSV-file and give the columns descriptive names,
    instead of only having a single bond-maturity in each CSV-file.
