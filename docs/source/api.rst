=============
API Reference
=============

This page covers basically everything osu.py is capable of.

.. note::

    Some cross-references in the docs may be broken and certain parts
    may have inconsistent formatting. I'm working on cleaning it up,
    but it's not high priority and takes a while because of the sheer
    amount of documentation.

Core Classes
------------

Clients
^^^^^^^

.. autoclass:: osu.Client
    :members:
    :member-order: bysource

.. autoclass:: osu.AsynchronousClient
    :members: from_client_credentials, from_credentials

.. autoclass:: osu.http.HTTPHandler
    :members:

.. autoclass:: osu.asyncio.http.AsynchronousHTTPHandler
    :members:

.. autoclass:: osu.Path

.. autoclass:: osu.http.BaseHTTPHandler
    :members:

Authentication
^^^^^^^^^^^^^^

.. autoclass:: osu.BaseAuthHandler
    :members:

.. autoclass:: osu.FunctionalAuthHandler
    :members:

.. autoclass:: osu.AuthHandler
    :members:

.. autoclass:: osu.AsynchronousAuthHandler
    :members:

.. autoclass:: osu.Scope
    :members:

Endpoint results
----------------
.. note::

    These can be imported directly from ``osu``

    Some endpoints return responses that don't represent any specific objects;
    that's what these are for.

.. automodule:: osu.results
    :members:

Objects
-------

.. note::

    These can be imported directly from ``osu``

.. automodule:: osu.objects
    :members:

Utility
-------

.. note::

    These can be imported directly from ``osu``

.. automodule:: osu.util
    :members:

Enums
-----

.. note::

    These can be imported directly from ``osu``

.. automodule:: osu.enums
    :members:
