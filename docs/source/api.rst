=============
API Reference
=============

This page covers basically everything osu.py is capable of.


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
Some endpoints return specific responses that don't represent any specific objects.

.. automodule:: osu.results
    :members:

Objects
-------

.. automodule:: osu.objects
    :members:

Utility
-------

.. automodule:: osu.util
    :members:

Enums
-----

.. automodule:: osu.enums
    :members:
