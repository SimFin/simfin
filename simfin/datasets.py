##########################################################################
#
# Lists with the names of all valid datasets and variants available for
# bulk download from SimFin. Also a few helper-functions for iterating
# and loading all the datasets and variants.
#
##########################################################################
# SimFin - Simple financial data for Python.
# www.simfin.com - www.github.com/simfin/simfin
# See README.md for instructions and LICENSE.txt for license details.
##########################################################################

import simfin as sf
from collections import defaultdict

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
datasets_other = ['companies', 'industries']

# All dataset names.
datasets_all = datasets_income + datasets_balance + datasets_cashflow + \
               datasets_shareprices + datasets_other

##########################################################################
# Variants.

# Lists of the variant-choices for different types of datasets.
variants_fundamental = ['annual', 'quarterly', 'ttm']
variants_shareprices = ['daily']
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
    }

##########################################################################
# Columns.

# Lists of the possible column-choices for different types of datasets.
columns_fundamental = ['subset', 'all']
columns_none = [None]

# Dict for easy lookup of the valid columns for a given dataset name.
valid_columns = \
    {
        'income': columns_fundamental,
        'income-banks': columns_fundamental,
        'income-insurance': columns_fundamental,

        'balance': columns_fundamental,
        'balance-banks': columns_fundamental,
        'balance-insurance': columns_fundamental,

        'cashflow': columns_fundamental,
        'cashflow-banks': columns_fundamental,
        'cashflow-insurance': columns_fundamental,

        'shareprices': columns_none,
        'companies': columns_none,
        'industries': columns_none,
    }

##########################################################################
# Helper functions.

def iter_all_datasets():
    """
    Create a generator for iterating over all valid datasets and variants.
    This only yields the names of the datasets and variants, not the actual
    Pandas DataFrames, use load_all_datasets() or the AllDatasets-class
    for that.

    Example:

    for dataset, variant in iter_all_datasets():
        print(dataset, variant)
    """

    # Yield all valid combinations of datasets and variants.
    for dataset in datasets_all:
        for variant in valid_variants[dataset]:
            yield dataset, variant


def load_all_datasets(*args, **kwargs):
    """
    Load all datasets and variants. Create and return a nested
    dict for fast lookup given dataset and variant names.

    Accepts the same args as the `sf.load()` function, except for
    dataset and variant. For example, `refresh_days` can be set
    to 0 to ensure all datasets are downloaded again, which is
    useful for testing purposes.

    :return:
        Nested dict `dfs` with all datasets and variants.

        Example: dfs['income']['annual'] is the dataset for
                 annual Income Statements.
    """

    # Initialize a nested dict-of-dict.
    dfs = defaultdict(dict)

    # For all possible datasets and variants.
    for dataset, variant in iter_all_datasets():
        # Load the dataset and variant as a Pandas DataFrame.
        df = sf.load(dataset=dataset, variant=variant, *args, **kwargs)

        # Add the Pandas DataFrame to the nested dict-dict.
        dfs[dataset][variant] = df

    # Convert and return the nested defaultdict to a normal dict-dict.
    return dict(dfs)

##########################################################################

class AllDatasets:
    """
    Load all valid datasets and variants as Pandas DataFrames.
    Also provide functions for easy lookup and iteration over datasets.
    """

    def __init__(self, *args, **kwargs):
        """
        Accepts the same args as the `sf.load()` function, except for
        dataset and variant. For example, `refresh_days` can be set
        to 0 to ensure all datasets are downloaded again, which is
        useful for testing purposes.
        """
        # Load all datasets into a nested dict-dict.
        self._dfs = load_all_datasets(*args, **kwargs)

    def get(self, dataset, variant=None):
        """
        Return the Pandas DataFrame for a single dataset and variant.

        :param dataset: String with name of the dataset.
        :param variant: String with the dataset variant.
        :return: Pandas DataFrame with the dataset.
        """
        return self._dfs[dataset][variant]

    def iter(self, datasets=None, variants=None):
        """
        Iterate over all valid datasets and variants, or only use
        the ones specified.

        Example:

        for dataset, variant, df in iter():
            # dataset and variant are strings with the names.
            # df is a Pandas DataFrame with the actual data.

        :param datasets:
            Default is None which uses all valid datasets.
            Otherwise a list of strings with the dataset-names to use.

        :param variants:
            Default is None which uses all valid variants for a dataset.
            Otherwise a list of strings with the variant-names to use.

        :return:
            Generator which iterates over:
            dataset (string), variant (string), df (Pandas DataFrame)
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

            # For all the selected variants.
            for variant in _variants:
                yield dataset, variant, self._dfs[dataset][variant]

##########################################################################
