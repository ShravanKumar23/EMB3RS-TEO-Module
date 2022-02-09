=================================
Structure of the TEO Module
=================================

The ‘sets’ define the physical structure of a model, usually independent from the specific scenarios which will be run. They define the time domain and time split, the spatial coverage, the technologies and energy vectors to be considered, etc. For instance, when a variable is defined as a function of the set ‘YEAR’ it will be indicated as variablename[y] at it will be computed for every year listed in the set. The sets of the TEO are presented in the Table below [3].

.. csv-table:: SETS
   :file: sets.csv
   :widths: 20, 80
   :header-rows: 1
