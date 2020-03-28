.. currentmodule:: retaggr

Engines
========

This file documents some general information about the engines you can search.

You generally shouldn't instantiate these classes yourself, rather you should use them as a reference.

ImageResult
------------

.. autoclass:: retaggr.engines.ImageResult

Danbooru
----------

.. autoclass:: retaggr.engines.Danbooru
    :members:

Iqdb
------

.. autoclass:: retaggr.engines.Iqdb
    :members:

Paheal
------

.. autoclass:: retaggr.engines.Paheal
    :members:


SauceNao
--------

.. autoclass:: retaggr.engines.SauceNao
    :members:

Base
------

This class is the base class for all engines that exist in the application. The attributes and methods listed here should exist in some form on
all the previous classes.

.. autoclass:: retaggr.engines.Engine
    :members:
