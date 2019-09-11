API Reference
===============

The following pages lay out the API of retaggr.

Version reference
-------------------

To check the installed retaggr version, there are two variables you can use.

retaggr follows semantic versioning. Older releases are considered unsupported and will be yanked if they contain major issues.

.. data:: version_info

    A named tuple similar to :py:obj:`sys.version_info`.

.. data:: __version__

    A string representation of the major, minor and micro version. eg. ``"1.2.0"``.

Table of contents
-------------------

.. toctree::
   :maxdepth: 2
   :caption: API reference:

   core
   config
   engines
   exceptions