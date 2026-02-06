============================
Getting started  with osu.py
============================

Client and AuthHandler
----------------------
The simplest way to initialise the client class using client credential grant is like so.

.. code:: py

    from osu import Client

    client = Client.from_credentials(client_id, client_secret, redirect_uri)

If you're unsure of where to obtain a client id and secret,
read `managing oauth applications <https://osu.ppy.sh/docs/index.html#managing-oauth-applications>`_ on the osu! docs.

There are also additional optional parameters that you can read about under
`Client.from_credentials <api.html#osu.Client.from_credentials>`_.

The other way to initialise the Client class is directly passing an auth handler.

.. code:: py

    from osu import Client

    auth = ...  # we'll get to this next

    client = Client(auth)

There are similar optional parameters, which you can read about at `Client <api.html#osu.Client>`_.

The auth parameter for the client is an `AuthHandler <api.html#AuthHandler>`_ object. You can initialise it like so (see below).
The `AuthHandler.get_auth_token <api.html#AuthHandler.get_auth_token>`_ call is optional and will be lazily
performed if using client credentials grant.

.. code:: py

    from osu import AuthHandler

    auth = AuthHandler(client_id, client_secret, redirect_uri)
    auth.get_auth_token()  # optional for client credentials grant

`AuthHandler`_ also has an optional parameter ``scope``, which is a `Scope <api.html#osu.Scope>`_ object.
You can read more about it at `AuthHandler`_.

All those examples involved client credential grant, but you can also use authorization code grant.
Here's a full code example (this code is from the examples folder on the osu.py repo:
`auth_url.py <https://github.com/Sheppsu/osu.py/blob/main/examples/auth_url.py>`_)

.. code:: py

    from osu import Client, AuthHandler, Scope, GameModeStr
    import os


    client_id = int(os.getenv('osu_client_id'))
    client_secret = os.getenv('osu_client_secret')
    redirect_url = "http://127.0.0.1:8080"

    # Usually you would redirect a user on your site
    # to the authorize url with the redirect_url being back
    # to your site where you can grab the code and get
    # an access token.
    # For this example, you are redirected to localhost with a code,
    # which you can copy paste from the url
    auth = AuthHandler(client_id, client_secret, redirect_url, Scope.identify())
    print(auth.get_auth_url())
    auth.get_auth_token(input("Code: "))  # The code is found in the redirect url (Ex. http://127.0.0.1:8080/?code=***********)
    client = Client(auth)

    user = client.get_own_data(GameModeStr.STANDARD)
    print(user.username)

If you want to learn more about available api requests, read through the `Client`_'s documentation or
check the `homepage <index.html>`_ for some specific examples.

AsynchronousClient
------------------
This class is the exact same as the Client class, but all api request functions are asynchronous and it uses `AsynchronousAuthHandler <api.html#AsynchronousAuthHandler>`_.
You can see it in use in the `asynchronous_client.py <https://github.com/Sheepposu/osu.py/blob/main/examples/asynchronous_client.py>`_ example on the github.

Scope
-----
The purpose of the scope class is to authorize under the desired scopes and to check the client
scope against the scope required for a specific request.

You can create a Scope object in any of the ways shown below.

.. code:: py

    Scope.default()  # public
    Scope.identify() # public, identify
    Scope("public", "identify", "friends.read")

You can see a list of all valid scopes and their descriptions at `Scope <api.html#osu.Scope>`_.

Further reading
---------------
You can check out the `advanced guide <advanced.html>`_ and/or look at more code examples at
`osu.py/examples <https://github.com/Sheepposu/osu.py/tree/main/examples>`_.
