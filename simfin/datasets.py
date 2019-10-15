##########################################################################
#
# Lists with the names of all valid datasets, variants and markets
# available for bulk download from SimFin. Also a few helper-functions
# for iterating and loading all the datasets.
#
##########################################################################
# SimFin - Simple financial data for Python.
# www.simfin.com - www.github.com/simfin/simfin
# See README.md for instructions and LICENSE.txt for license details.
##########################################################################

import simfin as sf

from collections import defaultdict
import sys

##########################################################################
# Datasets.

# All dataset names for Income Statements.
datasets_income = ['income', 'income-banks', 'income-insurance']

# All dataset names for Balance Sheets.
datasets_balance = ['balance', 'balance-banks', 'balance-insurance']

# All dataset names for Cash-Flow Statements.
datasets_cashflow = ['cashflow', 'cashflow-banks', 'cashflow-insurance']

# All dataset names for fundamental data.
datasets_fundamental = datasets_income + datasets_balance + datasets_cashflow

# All dataset names for shareprice data.
datasets_shareprices = ['shareprices']

# All other dataset names.
datasets_other = ['companies', 'industries', 'markets']

# All dataset names.
datasets_all = datasets_income + datasets_balance + datasets_cashflow + \
               datasets_shareprices + datasets_other

##########################################################################
# Markets.

# Lists of the market-choices. This is the default list that can be
# updated from the SimFin server using the helper-functions below.
markets_all = ['us', 'de', 'sg']
markets_none = [None]


def _gen_valid_markets():
    """
    Create a dict for easy lookup of valid markets for different datasets.

    The reason we have a helper-function for this, is that it needs to
    be updated when `markets_all` has been updated from the SimFin server.
    """

    valid_markets = \
        {
            'income': markets_all,
            'income-banks': markets_all,
            'income-insurance': markets_all,

            'balance': markets_all,
            'balance-banks': markets_all,
            'balance-insurance': markets_all,

            'cashflow': markets_all,
            'cashflow-banks': markets_all,
            'cashflow-insurance': markets_all,

            'shareprices': markets_all,
            'companies': markets_all,

            'industries': markets_none,
            'markets': markets_none
        }

    return valid_markets


# Dict for easy lookup of the valid markets for a given dataset.
# This will be updated when _load_market_list() is called.
valid_markets = _gen_valid_markets()


def _load_market_list():
    """
    Load all available markets from the SimFin server and update
    the global variables `markets_all` and `valid_markets`.

    Note that we cannot call this function until the data-dir has been set,
    so it cannot simply set `markets_all` and `valid_markets` upon import.
    """
    global markets_all
    global valid_markets

    try:
        # Load list with all the markets from the SimFin server.
        df = sf.load_markets(refresh_days=0)

        # Update the list of all available markets.
        markets_all = list(df.index.values)

        # Update the dict of valid markets for different datasets.
        valid_markets = _gen_valid_markets()
    except Exception as e:
        # Print the exception and continue.
        print(e, file=sys.stderr)
        print("Using default market-list.", file=sys.stderr)


##########################################################################
# Variants.

# Lists of the variant-choices for different types of datasets.
variants_fundamental = ['annual', 'annual-full',
                        'quarterly', 'quarterly-full',
                        'ttm', 'ttm-full']
variants_shareprices = ['latest', 'daily']
variants_none = [None]

# Dict for easy lookup of the valid variants for a given dataset.
valid_variants = \
    {
        'income': variants_fundamental,
        'income-banks': variants_fundamental,
        'income-insurance': variants_fundamental,

        'balance': variants_fundamental,
        'balance-banks': variants_fundamental,
        'balance-insurance': variants_fundamental,

        'cashflow': variants_fundamental,
        'cashflow-banks': variants_fundamental,
        'cashflow-insurance': variants_fundamental,

        'shareprices': variants_shareprices,
        'companies': variants_none,
        'industries': variants_none,
        'markets': variants_none,
    }

##########################################################################
# Helper functions.

def iter_all_datasets():
    """
    Create a generator for iterating over all valid datasets, variants and
    markets. This only yields the names of the datasets, variants and
    markets, not the actual Pandas DataFrames, use load_all_datasets() or
    the AllDatasets-class for that.

    Example:

    for dataset, variant, market in iter_all_datasets():
        print(dataset, variant, market)
    """

    # Yield all valid combinations of datasets, variants and markets.
    for dataset in datasets_all:
        for variant in valid_variants[dataset]:
            for market in valid_markets[dataset]:
                yield dataset, variant, market


def load_all_datasets(*args, **kwargs):
    """
    Load all datasets and variants. Create and return a nested
    dict for fast lookup given dataset, variant and market names.

    Accepts the same args as the `sf.load()` function, except for
    dataset, variant and market. For example, `refresh_days` can be set
    to 0 to ensure all datasets are downloaded again, which is
    useful for testing purposes.

    :return:
        Nested dict `dfs` with all datasets, variants and markets.

        Example: dfs['income']['annual']['us'] is the dataset for
                 annual Income Statements for the US market.
    """

    # Update the list of available markets from the SimFin server.
    _load_market_list()

    # Initialize a dict that can be nested to any depth.
    dfs = defaultdict(lambda: defaultdict(dict))

    # For all possible datasets, variants and markets.
    for dataset, variant, market in iter_all_datasets():
        try:
            # Load the dataset and variant as a Pandas DataFrame.
            df = sf.load(dataset=dataset, variant=variant, market=market,
                         *args, **kwargs)

            # Add the Pandas DataFrame to the nested dict.
            dfs[dataset][variant][market] = df
        except Exception as e:
            # Exceptions can occur e.g. if the API key is invalid, or if there
            # is another server error, or if there is no internet connection.

            # Print the exception and continue.
            print(e, file=sys.stderr)

            # Set the Pandas DataFrame to None in the nested dict,
            # to indicate that it could not be loaded.
            dfs[dataset][variant][market] = None

    # Return the nested dict. It is a bit tricky to convert the
    # defaultdict to a normal dict, and it is not really needed,
    # so just return the defaultdict as it is.
    return dfs

##########################################################################

class AllDatasets:
    """
    Load all valid datasets, variants and markets as Pandas DataFrames.
    Also provide functions for easy lookup and iteration over datasets.
    """

    def __init__(self, *args, **kwargs):
        """
        Accepts the same args as the `sf.load()` function, except for
        dataset, variant and market. For example, `refresh_days` can be
        set to 0 to ensure all datasets are downloaded again, which is
        useful for testing purposes.
        """
        # Load all datasets into a nested dict-dict.
        self._dfs = load_all_datasets(*args, **kwargs)

    def get(self, dataset, variant=None, market=None):
        """
        Return the Pandas DataFrame for a single dataset, variant and market.

        :param dataset: String with the dataset name.
        :param variant: String with the dataset's variant.
        :param market: String with the dataset's market.
        :return: Pandas DataFrame with the dataset.
        """
        return self._dfs[dataset][variant][market]

    def iter(self, datasets=None, variants=None, markets=None):
        """
        Iterate over all valid datasets, variants and markets,
        or only use the ones specified.

        Example:

        for dataset, variant, market, df in iter():
            # dataset, variant and market are strings with the names.
            # df is a Pandas DataFrame with the actual data.

        :param datasets:
            Default is None which uses all valid datasets.
            Otherwise a list of strings with the dataset-names to use.

        :param variants:
            Default is None which uses all valid variants for a dataset.
            Otherwise a list of strings with the variant-names to use.

        :param markets:
            Default is None which uses all valid markets for a dataset.
            Otherwise a list of strings with the market-names to use.

        :return:
            Generator which iterates over:
            dataset (string), variant (string), market (string), df (Pandas DataFrame)
        """

        # Use provided or all datasets?
        if datasets is None:
            datasets = datasets_all

        # For all datasets.
        for dataset in datasets:
            # Use provided or all valid variants for this dataset?
            if variants is not None:
                _variants = variants
            else:
                _variants = valid_variants[dataset]

            # Use provided or all valid markets for this dataset?
            if markets is not None:
                _markets = markets
            else:
                _markets = valid_markets[dataset]

            # For all the selected variants and markets
            for variant in _variants:
                for market in _markets:
                    # Get the DataFrame with the actual data.
                    df = self.get(dataset=dataset, variant=variant, market=market)

                    # Yield all the strings and the DataFrame.
                    yield dataset, variant, market, df

##########################################################################
