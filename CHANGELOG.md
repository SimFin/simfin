# Changes to the SimFin Python package

## Version 0.3.0 (2019-MM-DD)

"Private" beta version only intended for a small number of friends and
experienced users of SimFin.

### Changes

-   Added `sf.StockHub` for easy loading and processing of stock data,
    and wrote a new tutorial on this.

-   Added function `sf.rel_change()` for calculating stock returns and
    various growth-rates. Added `sf.mean_log_change()` for calculating
    mean-log stock returns e.g. for all 1-3 year periods. Also wrote a
    new tutorial for these functions.

-   Added function `sf.apply()` for applying a function to a DataFrame
    with either a single or multiple stocks. Changed `sf.asfreq()`,
    `sf.resample()`, `sf.reindex()`, and `sf.rel_change()` to use this.
    Added a section to Tutorial 01 on this.

-   Added several functions for calculating signals from financial data,
    and wrote a new tutorial for these functions.
    
-   Added wrapper-function ` @sf.cache` for caching the result of slow
    functions to disk. Added its use in all signal-functions. Wrote
    Tutorial 06 on this.

-   Added function `sf.ebitda` for calculating EBITDA.


## Version 0.2.0 (2019-11-09)

"Private" beta version only intended for a small number of friends and
experienced users of SimFin.

It took us a while to make these changes, because we consider our moves
very carefully: https://www.youtube.com/watch?v=HxWCAJS7Co8

### Changes

-   Added bulk-data load-functions for banks and insurance companies.
-   Changed all specialized bulk-data load-functions to use functools.partial.
-   Added 'full' variants for datasets: income, balance, cashflow.
    The 'full' variant has more columns than the 'free' variant.
-   Added 'shareprices-latest' dataset variant.
-   Added support for dataset markets e.g. `sf.load_income(variant='annual', market='us')`
-   Added a script that generates 'names.py' from the SimFin-server's database.
-   Improved implementation of `sf.resample()` and also added the functions
    `sf.reindex()` and `sf.asfreq()`. Also wrote a new tutorial for these.


## Version 0.1.0 (2019-09-26)

Alpha version only intended for developers.
