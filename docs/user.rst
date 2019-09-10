.. currentmodule:: retaggr
..  _user:

Getting Started
=================

Using retaggr is extremely easy. All functions are provided through the :class:`ReverseSearch` class.

The :class:`ReverseSearch` should be instantiated with the :class:`ReverseSearchConfig` class.

:class:`ReverseSearchConfig` technically doesn't need any parameters, but it's highly recommended to at
least pass ``min_score``.

An example of how to do so can be found below.

.. code-block:: python

    # Relevant imports
    from retaggr import ReverseSearch, ReverseSearchConfig

    # Technically the config object doesn't need any parameters to work.
    # That said, the only option available at that point is Paheal.
    # min_score is required to search IQDB, whilst other engines 
    # will require their own API keys.
    # See the API reference for relevant keys and values.
    config = ReverseSearchConfig(min_score=80.0)

    # Next we instantiate the object
    rsearch = ReverseSearch(config)

After that it's possible to search any properly instantiated engine from an asynchronous context.

.. code-block:: python

    # Searching IQDB using our previous object.
    result = await rsearch.search_image("iqdb", "https://danbooru.donmai.us/data/__tsukumo_benben_touhou_drawn_by_elise_piclic__6e6da59922b923391f02ba1ce78f9b42.jpg")

Acceptable parameters for :meth:`ReverseSearch.search_image` are filenames found in the ``engines`` subfolder.

It is also possible to search all instantiated engines through the :meth:`ReverseSearch.reverse_search` method.

.. code-block:: python

    # This only searches IQDB and Paheal, since we haven't instantiated anything else.
    result = await rsearch.reverse_search("https://danbooru.donmai.us/data/__tsukumo_benben_touhou_drawn_by_elise_piclic__6e6da59922b923391f02ba1ce78f9b42.jpg")

Do note that this method returns a Set, not a List, unlike the search_image function. This is to remove duplicate findings.

About asyncio
---------------

This is an asynchronous library. This means that it can only be called from an asynchronous context.
That said, it might be desirable to call the class methods from a synchronous context. This is possible by
using ``asyncio.run()``

See the example below.

.. code-block:: python

    # Instantiate the main object normally (instantiation is not asynchronous).
    rsearch = ReverseSearch(ReverseSearchConfig())

    # Use asyncio.run() for executing the search methods.
    result = asyncio.run(rsearch.reverse_search("https://danbooru.donmai.us/data/__tsukumo_benben_touhou_drawn_by_elise_piclic__6e6da59922b923391f02ba1ce78f9b42.jpg"))

    # result will have the reverse searched data.

For those using asyncio, this library spawns a couple of threads using ``asyncio.run_in_executor`` at certain points.

The reason for this is due to the fact that the ``aiohttp`` library attempts to sanitize URLs, and as a result, the library
falls back on using ``requests`` when this becomes an issue. 

The ``aiohttp`` developers have stated that since this is due to a server misconfiguration issue,
and as a result that they do not intent to fix this.