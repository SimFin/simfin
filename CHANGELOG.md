# Changes to the SimFin Python package

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
