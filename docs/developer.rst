Developer Guidelines
======================

This document details adding a new booru/engine to retaggr. This document is not intended for someone
who wants to merely use retaggr in their application. If you want to use retaggr, see :ref:`user`.

Step 1: Making the booru class
--------------------------------

- Start by creating a new file in the boorus folder.
- In this file, import the base :class:`Booru` class and subclass it. This class will be used as a base for the booru class.
- Implement the search logic in the :meth:`search_image` method. This method accepts one parameter, which is the image URL.
- If your booru/engine needs an API key or some other user defined variable, add it to the :meth:`__init__` method.
- Define if the booru/engine needs to download the image locally in order to search it by setting the :attr:`Booru.download_required` attribute.
- Define the :attr:`Booru.host` attribute. This should be a human-visitable URL that links to the engine or the booru itself. 
  
  Note that in the case of an engine for a specific booru, the engine should be used here.

Step 2: Expanding the config object.
--------------------------------------

This is purely documentation. Add your new parameters to :class:`ReverseSearchConfig`, where their names should be prefixed with
``filename_``, where ``filename`` is the file you made in step 1.


Step 3: Adding it to core
---------------------------

- Add the filename you just created to :attr:`ReverseSearch._all_boorus`.
- In the :meth:`__init__`, verify that the variables you need are in the config object and if they are, 
  instantiate the class you just made in the :meth:`__init__` and assign it to :attr:`ReverseSearch.accessible_boorus`
  where the key is the variable you added to :attr:`ReverseSearch._all_boorus` and the value the class.

Step 4: Writing tests
-----------------------

You only need to write one test. This test should search an image using the class you just created, directly instantiating it's underlying
object (so not through ReverseSearch) by calling the :meth:`search_image` method and then asserting the results with an existing list.

If your engine needs an API key or a user defined variable, add it to an environment variable and load it in (reference the start of `test_booru.py`).

Step 5: PR the changes
------------------------

As it says on the tin. Specify any new environment variables that are required for CI to work in your PR.

Running the tests
-------------------

Running the tests requires accounts at Danbooru and E621. 

Before running your tests, add the following environment variables and install `test-requirements.txt` using pip.

- DANBOORU_USERNAME
- DANBOORU_API_KEY
- E621_USERNAME
- APP_NAME
- APP_VERSION
- SAUCENAO_API_KEY

After that you can execute the tests with pytest.