##########################################################################
#
# Functions for getting info about the available datasets and columns.
#
##########################################################################
# SimFin - Simple financial data for Python.
# www.simfin.com - www.github.com/simfin/simfin
# See README.md for instructions and LICENSE.txt for license details.
##########################################################################

from textwrap import TextWrapper

from simfin.load_info import load_info_columns, load_info_datasets

##########################################################################

def info_datasets(dataset=None, show_columns=True):
    """
    Show a list of all available datasets, or show the details for the
    given dataset.

    :param dataset:
        String with the exact name of a dataset.
        If None then show a list of all available datasets.

    :param show_columns:
        Boolean whether to show the columns of the given dataset.

    :return:
        `None`
    """

    # Load dict with info about all the datasets.
    info = load_info_datasets()

    if dataset is None:
        # Show all available datasets.

        # String with list of dataset names.
        datasets = sorted(list(info))
        datasets = ', '.join(datasets)

        # Used to ensure the list of datasets looks nice on multiple lines.
        wrapper_datasets = TextWrapper(width=80, break_on_hyphens=False,
                                       break_long_words=False,
                                       initial_indent='All datasets: ',
                                       subsequent_indent='              ')

        # Print the list of datasets.
        datasets = wrapper_datasets.wrap(datasets)
        print('\n'.join(datasets))
    else:
        # Ensure the dataset name is lower-case.
        dataset = dataset.lower()

        # Lookup the info for this dataset.
        x = info.get(dataset)

        if x is None:
            # Dataset does not exist. Print error-message.
            msg = 'Dataset \'{0}\' not found.'
            msg = msg.format(dataset)
            print(msg)
        else:
            # Show dataset name.
            print('Dataset: ', dataset)

            # Used to ensure the list of variants looks nice on multiple lines.
            space_indent = '          '
            wrapper_variants = TextWrapper(width=80,
                                           initial_indent='Variants: ',
                                           subsequent_indent=space_indent)

            # Used to ensure the list of markets looks nice on multiple lines.
            wrapper_markets = TextWrapper(width=80,
                                          initial_indent='Markets:  ',
                                          subsequent_indent=space_indent)

            # Show list of variants for this dataset.
            variants = sorted(x['variants'])
            if len(variants) > 0:
                variants = ', '.join(variants)
            else:
                variants = '-'
            variants = wrapper_variants.wrap(variants)
            variants = '\n'.join(variants)
            print(variants)

            # Show list of markets for this dataset.
            markets = sorted(x['markets'])
            if len(markets) > 0:
                markets = ', '.join(markets)
            else:
                markets = '-'
            markets = wrapper_markets.wrap(markets)
            markets = '\n'.join(markets)
            print(markets)

            # Show columns for this dataset?
            if show_columns:
                print('Columns:  (The * marks data that requires a paid subscription)')

                # Used to ensure the columns look nice on multiple lines.
                wrapper_columns = TextWrapper(width=80,
                                              initial_indent='',
                                              subsequent_indent='   ')

                # For each column in this dataset.
                for column in x['columns']:
                    # String to indicate if column-data is premium or free.
                    is_premium = '*' if column['is_premium'] else '-'

                    # String with list of Python shortcuts.
                    shortcuts = sorted(column['shortcuts'])
                    shortcuts = ', '.join(shortcuts)

                    # String with the column's full name and Python shortcuts.
                    msg = '{0} \"{1}\" {2}'
                    msg = msg.format(is_premium, column['name'], shortcuts)

                    # Break the string into lines of some max-length so it
                    # looks nice if it has to be printed on multiple lines.
                    msg = wrapper_columns.wrap(msg)
                    msg = '\n'.join(msg)

                    # Print the lines.
                    print(msg)

##########################################################################

def info_columns(search):
    """
    Show all columns that match the given search-text.

    :param search:
        String which must be in the column-name, shortcuts or description.
        Case insensitive.

    :return:
        `None`
    """

    # Has a valid search-text been provided?
    if search is None or len(str(search).strip()) == 0:
        # Print error-message.
        print('Please provide a valid search-string for the columns.')
    else:
        # Ensure the search-text is lower-case.
        search = search.lower()

        # Load dict with info about all the columns.
        info = load_info_columns()

        # Used to ensure the list of datasets looks nice on multiple lines.
        space_indent = '             '
        wrapper_datasets = TextWrapper(width=80, break_on_hyphens=False,
                                       break_long_words=False,
                                       initial_indent='Datasets:    ',
                                       subsequent_indent=space_indent)

        # Used to ensure the list of shortcuts looks nice on multiple lines.
        wrapper_shortcuts = TextWrapper(width=80, break_on_hyphens=False,
                                        break_long_words=False,
                                        initial_indent='Shortcuts:   ',
                                        subsequent_indent=space_indent)

        # Used to ensure the description looks nice on multiple lines.
        wrapper_descr = TextWrapper(width=80,
                                    initial_indent='Description: ',
                                    subsequent_indent=space_indent)

        # Number of matching columns found.
        num_found = 0

        # For each column.
        for column in info:
            # Full name of the column e.g. "Shares (Basic)"
            name = column['name']
            name_lower = name.lower()

            # List of shortcuts e.g. SHARES_BASIC
            shortcuts = sorted(column['shortcuts'])
            shortcuts = ', '.join(shortcuts)
            shortcuts_lower = shortcuts.lower()

            # Description of the column.
            descr = column['description'].strip()
            descr_lower = descr.lower()

            if search in name_lower or search in shortcuts_lower \
                                    or search in descr_lower:

                # Increase number of matching columns.
                num_found += 1

                # Boolean whether column is free or premium.
                is_premium = column['is_premium']

                # Show the full column-name. Note the space-alignment.
                print('Name:        \"{0}\"'.format(name))

                # Show list of shortcuts. This is aligned by the text-wrapper.
                shortcuts = wrapper_shortcuts.wrap(shortcuts)
                print('\n'.join(shortcuts))

                # Show whether the data is free or premium. Note the alignment.
                print('Premium:    ', is_premium)

                # Show list of datasets. This is aligned by the text-wrapper.
                datasets = sorted(column['datasets'])
                datasets = ', '.join(datasets)
                datasets = wrapper_datasets.wrap(datasets)
                print('\n'.join(datasets))

                # Show the description. This is aligned by the text-wrapper.
                if len(descr) == 0:
                    descr = '-'
                descr = wrapper_descr.wrap(descr)
                descr = '\n'.join(descr)
                print(descr)

                # Print newline.
                print()

        # Show error if we did not find any matching columns.
        if num_found == 0:
            msg = 'Search-text \'{0}\' was not found.'
            msg = msg.format(search)
            print(msg)

##########################################################################
