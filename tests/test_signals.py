##########################################################################
#
# Unit tests (pytest) for signals.py
#
##########################################################################
# SimFin - Simple financial data for Python.
# www.simfin.com - www.github.com/simfin/simfin
# See README.md for instructions and LICENSE.txt for license details.
##########################################################################

import simfin as sf

from pandas.testing import assert_frame_equal

##########################################################################
# Test configuration.

# Set data directory.
sf.set_data_dir(data_dir='~/simfin_data/')

# Load API key or use default 'free' if key-file doesn't exist.
sf.load_api_key(path='~/simfin_api_key.txt', default_key='free')

# Set number of days before refreshing data from SimFin server.
refresh_days = 30

##########################################################################
# Test functions.

def test_equal_subsets():
    """
    Test the signals are identical when calculated for subsets of the tickers.
    """

    # Calculate and compare signals for these tickers.
    ticker = 'SAVE'
    tickers = ['FL', 'SAVE', 'TLYS']

    # Used for calculating signals for ALL tickers.
    hub1 = sf.StockHub()

    # Used for calculating signals for SOME tickers.
    hub2 = sf.StockHub(tickers=tickers)

    # Used for calculating signals for ONE ticker.
    hub3 = sf.StockHub(tickers=[ticker])

    # Helper-function to perform the actual signal calculation and comparison.
    def _test(func_name, variant, func=None):
        # Get the object-methods for the function with the given name.
        signal_func1 = getattr(hub1, func_name)
        signal_func2 = getattr(hub2, func_name)
        signal_func3 = getattr(hub3, func_name)

        # Calculate the signals.
        df_signals1 = signal_func1(variant=variant, func=func)
        df_signals2 = signal_func2(variant=variant, func=func)
        df_signals3 = signal_func3(variant=variant, func=func)

        # Compare the signals and ensure they are identical.
        assert_frame_equal(df_signals1.loc[tickers], df_signals2)
        assert_frame_equal(df_signals1.loc[ticker], df_signals3.loc[ticker])
        assert_frame_equal(df_signals2.loc[ticker], df_signals3.loc[ticker])

    # Test for the different signal-functions, variants and functions.
    for func_name in ['val_signals', 'fin_signals', 'growth_signals']:
        for variant in ['daily', 'latest']:
            for func in [None, sf.avg_ttm_2y]:
                _test(func_name=func_name, variant=variant, func=func)

##########################################################################
