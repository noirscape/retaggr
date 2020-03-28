SauceNao Handler Guidelines
=============================

This document details the rough process of adding new handlers to SauceNao

Step 1: Locate the engine ID
------------------------------

A list of all the engine IDs can be located at https://saucenao.com/status.html . Make sure to note it down.

Step 2: Copy the base class
-----------------------------

A base interface class can be found in the handlers folder (`base.py`). 
Copy it and rename the file and class to your new engine.
The rule is that each handler is suffixed with Handler and the name before that must be descriptive of the handler.

Step 3: Implement the methods
-------------------------------

Assuming your handler does not need additional API keys or such, simply implement the :meth:`get_tag_data` and :meth:`get_source_data` methods.

These methods receive the subset of the result data that is relevant. Usually it is possible to locate an ID of some sorts that can be used to retrieve additional information.

Step 3a: Additional API keys
------------------------------

If you need additional API keys, follow the instructions on how to change the config in the adding a new engine section of the documentation. The config entry does not have to be changed for this to function.

Step 4: Writing tests
-----------------------

Write a single test for your handler. Mock the relevant input data that your handler needs to function.

Step 5: Add it to the SauceNao engine
---------------------------------------

As written. If you don't need extra API keys, just add an instance to the :attr:`handlers` dictionary that is created at instantiation time. The key is the engine ID.

Step 5a: Additional API keys
-------------------------------

If you have additional API keys, don't add an instance to the :attr:`handlers` attribute, but instead write an additional method that adds the instance to the dictionary. Then modify the core to use this activation method.

Step 6: PR the changes
------------------------

As it says on the tin. Specify any new environment variables that are required for CI to work in your PR.
