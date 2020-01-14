.. simfin documentation

Load Data
=========

These functions are used for loading simfin datasets into Pandas DataFrames.
If the data-file does not exist in the data-directory on disk, then it is
first downloaded from the SimFin server and saved in the local data-directory,
so it can be loaded very quickly in the future. The main function is
:obj:`~simfin.load.load` which is specialized using `functools.partial`_ into e.g.
:obj:`~simfin.load.load_companies`, :obj:`~simfin.load.load_shareprices`, etc.
See `Tutorial 01`_ for detailed examples.
If you want to load several datasets, then it is easier to use :doc:`hubs`.

|note_namespace|

.. automodule:: simfin.load
   :members:

