# The Future of SimFin

## v. 0.4.0 (Public Beta)

### Goal

A beta version that is ready for the general public.

### Tasks

-   **Magnus:** Generate docs using sphinx or another system.  

-   **Thomas:** Fix erroneous share-counts in the data.

-   **Thomas:** Merge financial data for GOOG and GOOG_OLD, so it is just
    one company in the database. Is it the same problem for other companies? 

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
