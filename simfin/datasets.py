##########################################################################
#
# Functions and classes for iterating over and loading all datasets,
# variants and markets that are available for bulk download from SimFin.
#
##########################################################################
# SimFin - Simple financial data for Python.
# www.simfin.com - www.github.com/simfin/simfin
# See README.md for instructions and LICENSE.txt for license details.
##########################################################################

import simfin as sf
from simfin.load_info import load_info_datasets

from collections import defaultdict
from functools import partial, lru_cache
import sys

##########################################################################
# Lists of dataset names.

@lru_cache()
def datasets_all():
    """
    Return a list of strings with the names of all available datasets.
    """

    # Load dict with info about all the datasets.
    info_datasets = load_info_datasets()

    # Create a list of just the dataset names.
    datasets = list(info_datasets)

    return datasets


@lru_cache()
def datasets_startswith(names):
    """
    Return a list of strings with dataset names that begin with the given
    names.

    :param names:
        String or tuple of strings.

    :return:
        List of strings.
    """

    # Load dict with info about all the datasets.
    info_datasets = load_info_datasets()

    # Create a list of just the dataset names.
    datasets = list(info_datasets)

    # Filter the datasets so we only get the ones that start with these names.
    datasets = list(filter(lambda s: s.startswith(names), datasets))

    return datasets

# List of dataset names that begin with 'income'.
datasets_income = partial(datasets_startswith, names='income')
datasets_income.__doc__ = 'List of dataset names that begin with \'income\'.'

# List of dataset names that begin with 'balance'.
datasets_balance = partial(datasets_startswith, names='balance')
datasets_balance.__doc__ = 'List of dataset names that begin with \'balance\'.'

# List of dataset names that begin with 'cashflow'.
datasets_cashflow = partial(datasets_startswith, names='cashflow')
datasets_cashflow.__doc__ = 'List of dataset names that begin with \'cashflow\'.'

# List of dataset names that begin with either 'income', 'balance' or 'cashflow'.
datasets_fundamental = partial(datasets_startswith,
                               names=('income', 'balance', 'cashflow'))
datasets_fundamental.__doc__ = 'List of dataset names with fundamental data.'

# List of dataset names that begin with 'shareprices'.
datasets_shareprices = partial(datasets_startswith, names='shareprices')
datasets_shareprices.__doc__ = 'List of dataset names that begin with \'shareprices\'.'

##########################################################################
# Functions for iterating over and loading all datasets.

def iter_all_datasets(datasets=None):
    """
    Create a generator for iterating over all valid datasets, variants and
    markets. For example:

    .. code-block:: python

        for dataset, variant, market in iter_all_datasets():
            print(dataset, variant, market)

    This only yields the names of the datasets, variants and markets, not the
    actual Pandas DataFrames, use :obj:`~simfin.datasets.load_all_datasets`
    or the :obj:`~simfin.datasets.AllDatasets` class for that.

    :param datasets:
        If `None` then iterate over all datasets. Otherwise if this is a string
        or list of strings, then only iterate over these datasets.
    """

    # Load dict with info about all the datasets.
    info_datasets = load_info_datasets()

    # Only use the given datasets?
    if datasets is not None:
        # Create a new dict which only contains the given datasets.
        info_datasets = {k: v for k, v in info_datasets.items()
                         if k in datasets}

    # Yield all valid combinations of datasets, variants and markets.
    for dataset, x in info_datasets.items():
        # If the list of variants is empty, use a list with None,
        # otherwise the for-loop below would not yield anything.
        if len(x['variants']) > 0:
            variants = x['variants']
        else:
            variants = [None]

        # If the list of markets is empty, use a list with None,
        # otherwise the for-loop below would not yield anything.
        if len(x['markets']) > 0:
            markets = x['markets']
        else:
            markets = [None]

        for variant in variants:
            for market in markets:
                yield dataset, variant, market


def load_all_datasets(**kwargs):
    """
    Load all datasets and variants. Create and return a nested
    dict for fast lookup given dataset, variant and market names.

    Accepts the same args as the :obj:`~simfin.load.load` function, except for
    dataset, variant and market. For example, `refresh_days` can be set
    to 0 to ensure all datasets are downloaded again, which is
    useful for testing purposes.

    :return:
        Nested dict `dfs` with all datasets, variants and markets.
        Example: `dfs['income']['annual']['us']` is the dataset for
        annual Income Statements for the US market.
    """

    # Initialize a dict that can be nested to any depth.
    dfs = defaultdict(lambda: defaultdict(dict))

    # For all possible datasets, variants and markets.
    for dataset, variant, market in iter_all_datasets():
        try:
            # Load the dataset and variant as a Pandas DataFrame.
            df = sf.load(dataset=dataset, variant=variant, market=market,
                         **kwargs)

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

    def __init__(self, **kwargs):
        """
        Accepts the same args as the :obj:`~simfin.load.load` function, except
        for dataset, variant and market. For example, `refresh_days` can be
        set to 0 to ensure all datasets are downloaded again, which is
        useful for testing purposes.
        """
        # Load all datasets into a nested dict-dict.
        self._dfs = load_all_datasets(**kwargs)

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
        or only use the ones specified. For example:

        .. code-block:: python

            for dataset, variant, market, df in all_datasets.iter():
                # dataset, variant and market are strings with the names.
                # df is a Pandas DataFrame with the actual data.

        :param datasets:
            Default is `None` which uses all valid datasets.
            Otherwise a list of strings with the dataset-names to use.

        :param variants:
            Default is `None` which uses all valid variants for a dataset.
            Otherwise a list of strings with the variant-names to use.

        :param markets:
            Default is `None` which uses all valid markets for a dataset.
            Otherwise a list of strings with the market-names to use.

        :return:
            Generator which iterates over:
            dataset (string), variant (string), market (string), df (Pandas DataFrame)
        """

        # Load dict with info about all the datasets.
        info_datasets = load_info_datasets()

        # Use provided or all datasets?
        if datasets is None:
            datasets = datasets_all

        # For all datasets.
        for dataset in datasets:
            # Use provided or all valid variants for this dataset?
            if variants is not None:
                _variants = variants
            else:
                _variants = info_datasets[dataset]['variants']

            # Use provided or all valid markets for this dataset?
            if markets is not None:
                _markets = markets
            else:
                _markets = info_datasets[dataset]['markets']

            # For all the selected variants and markets.
            for variant in _variants:
                for market in _markets:
                    # Get the Pandas DataFrame with the actual data.
                    df = self.get(dataset=dataset, variant=variant, market=market)

                    # Yield all the strings and the Pandas DataFrame.
                    yield dataset, variant, market, df

##########################################################################
