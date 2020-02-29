# Changes to the SimFin Python package

## Version 0.5.0 (2020-MM-DD)

???

### Changes

-   Added function `sf.moving_zscore()`

-   Made function `sf.convert_to_periods()` public.

-   Changed calculation of signals: ROA, ROE, ASSET_TURNOVER.

-   Added support for Pandas Series in function `sf.winsorize()`

-   Added data quality tests to `test_bulk_data.ipynb`


## Version 0.4.0 (2020-01-25)

Public beta version.

Please be patient if you experience any problems. Although the system may look
fully automated, there is actually a little man sitting inside the server to
handle all of your requests: https://youtu.be/8cXF88XzALk

### Changes

-   Added function `sf.max_drawdown()`

-   Added documentation using the sphinx system and setup automatic generation
    of the docs at: https://simfin.readthedocs.io/
    
-   Setup automatic daily testing using GitHub Actions for both the simfin
    package and the tutorials.


## Version 0.3.0 (2020-01-03)

Early public beta version.

In this version, we were mainly trying to decide which colour the icons
should be: https://youtu.be/UMXs9i201AQ

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
    
-   Extended bulk-data system to support json-files with meta-info.
    Added functions `sf.load_info_datasets` and `sf.load_info_columns`
    and used them in `datasets.py` and `test_bulk_data.py`. Also added
    functions `sf.info_datasets` and `sf.info_columns` and used them
    in Tutorial 01.


## Version 0.2.0 (2019-11-09)

"Private" beta version only intended for a small number of friends and
experienced users of SimFin.

It took us a while to make these changes, because we consider our moves
very carefully: https://youtu.be/HxWCAJS7Co8

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
