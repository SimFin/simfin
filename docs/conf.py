# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------

project = 'SimFin'
copyright = '2020, SimFin'
author = 'SimFin, Hvass-Labs'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.linkcode']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Combine the doc-strings for a class and its __init__ method.
autoclass_content = 'both'

# Fix: https://stackoverflow.com/questions/56336234/build-fail-sphinx-error-contents-rst-not-found
master_doc = 'index'


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'nature'

# Settings for the left sidebar.
html_sidebars = { '**': ['globaltoc.html', 'searchbox.html'] }

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


# -- Add this to the beginning of every rst file -----------------------------

rst_prolog = """
.. |note_namespace| replace:: For convenience, the most important functions
    can be called directly from the `simfin` namespace. For example, instead
    of calling `simfin.load.load_income()` you can simply call
    `simfin.load_income()`

.. The following are external links to the tutorials, because I could not get
    sphinx.ext.extlinks to work. Use `Tutorial 01`_ to insert link in your document.
.. _functools.partial: https://docs.python.org/3/library/functools.html#functools.partial
.. _Tutorial 01: https://github.com/SimFin/simfin-tutorials/blob/master/01_Basics.ipynb
.. _Tutorial 02: https://github.com/SimFin/simfin-tutorials/blob/master/02_Resampling.ipynb 
.. _Tutorial 03: https://github.com/SimFin/simfin-tutorials/blob/master/03_Growth_Returns.ipynb
.. _Tutorial 04: https://github.com/SimFin/simfin-tutorials/blob/master/04_Signals.ipynb
.. _Tutorial 05: https://github.com/SimFin/simfin-tutorials/blob/master/05_Data_Hubs.ipynb
.. _Tutorial 06: https://github.com/SimFin/simfin-tutorials/blob/master/06_Performance_Tips.ipynb
"""


# -- Create a link to the source-file on GitHub ------------------------------

import inspect
from os.path import relpath, dirname

# Resolve function for the linkcode extension.
# Original: https://github.com/numpy/numpy/blob/master/doc/source/conf.py
# The only modification is the last few lines changed to simfin.
def linkcode_resolve(domain, info):
    """
    Determine the URL corresponding to Python object
    """
    if domain != 'py':
        return None

    modname = info['module']
    fullname = info['fullname']

    submod = sys.modules.get(modname)
    if submod is None:
        return None

    obj = submod
    for part in fullname.split('.'):
        try:
            obj = getattr(obj, part)
        except Exception:
            return None

    # strip decorators, which would resolve to the source of the decorator
    # possibly an upstream bug in getsourcefile, bpo-1764286
    try:
        unwrap = inspect.unwrap
    except AttributeError:
        pass
    else:
        obj = unwrap(obj)

    try:
        fn = inspect.getsourcefile(obj)
    except Exception:
        fn = None
    if not fn:
        return None

    try:
        source, lineno = inspect.getsourcelines(obj)
    except Exception:
        lineno = None

    if lineno:
        linespec = "#L%d-L%d" % (lineno, lineno + len(source) - 1)
    else:
        linespec = ""

    # Create URL for simfin's github repo.
    import simfin
    fn = relpath(fn, start=dirname(simfin.__file__))
    url = "https://github.com/simfin/simfin/blob/master/simfin/%s%s" % (fn, linespec)

    return url
