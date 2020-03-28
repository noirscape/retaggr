.. retaggr documentation master file, created by
   sphinx-quickstart on Sun Aug 18 23:08:51 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to retaggr's documentation!
================================================

Library to reverse search various boorus.

.. code-block:: python

    from retaggr import ReverseSearch, ReverseSearchConfig
    config = ReverseSearchConfig(min_score=80.0)
    rsearch = ReverseSearch(config)

Check the :ref:`user` page for more.

.. toctree::
   :maxdepth: 3
   :caption: Contents:

   usage
   api


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`