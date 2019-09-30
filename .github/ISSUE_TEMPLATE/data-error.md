---
name: Data Error
about: Simfin data has errors
title: Data Error
labels: data-error
assignees: ''

---

# Data Error

If you find errors in the SimFin data, please make sure that you
have the newest version of simfin installed using:

    pip install --upgrade simfin

Then make sure you have fresh data. If you set `refresh_days=0` when
loading the data (see example below), then the data should get downloaded
automatically. Otherwise you can manually delete the file from your
local simfin data-directory, before downloading the data again.

If you are still having problems, then please provide the following
details.


## Code Example

Please write a minimal code example that reproduces the problem.
You can indent the code-block to get proper formatting, like so:

    import simfin as sf

    # Configure simfin.
    sf.set_data_dir('~/simfin_data/')
    sf.load_api_key(path='~/simfin_api_key.txt', default_key='free')

    # Download and load the dataset from the SimFin server.
    df = sf.load_income(variant='annual', refresh_days=0)

    # Show the data that has errors.
    print(df[[SHARES_BASIC, SHARES_DILUTED]].head(5))


## Data Output

Please write the data output that has errors and point out the problem.
For example, the above code generates the following output,
where SHARES_BASIC and SHARES_DILUTED are both NaN for Report Date 2007-10-31.
(Note that you can also indent the data by pressing the tab-key to get
proper formatting)

                        Shares (Basic)  Shares (Diluted)
    Ticker Report Date                                  
    A      2007-10-31              NaN               NaN
           2008-10-31      508200000.0       519400000.0
           2009-10-31      484400000.0       484400000.0
           2010-10-31      485800000.0       494200000.0
           2011-10-31      485800000.0       497000000.0


## Generic Test

We use an automatic test-suite to ensure the data is correct and reliable.
You are very welcome to try and develop a generic test using the tools in
[tests/test_bulk_data.ipynb](https://github.com/SimFin/simfin/blob/master/tests/test_bulk_data.ipynb)
that can find all data errors of the type you are reporting. If you do so,
then please write the code here. Instructions for running this automated
data-test can be found in the project's [README](https://github.com/SimFin/simfin/blob/master/README.md).
