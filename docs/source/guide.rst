Getting started  with osu.py
============================

Structure of osu.py
^^^^^^^^^^^^^^^^^^^
There are three classes responsible for making and assisting with api requests/authentication. 
The Client class contains a function for all documented api requests. 
For each request, a path object is made and passed to the HTTPHandler class. 
The HTTPHandler class makes all checks the user's scopes against the url required scopes and makes the request with the given info. 
The data returned from the endpoint is then formatted correctly and returned. 
The third class is the AuthHandler class. 
This class handles everything around authorizing with the api.

Client and AuthHandler
^^^^^^^^^^^^^^^^^^^^^^^^^^^
The simplest way to initialise the client class using client credential grant is like so.

.. code:: py

	from osu import Client
	
	client = Client.from_client_credentials(client_id, client_secret, redirect_uri)
	
If you're unsure of where to obtain a client id and secret, read `here <https://osu.ppy.sh/docs/index.html#managing-oauth-applications>`_.
	
There are also three more optional arguments you can use (scope, code, and limit_per_second). You can read more about them `here <api.html#osu.Client.from_client_credentials>`_.

The other way to initialise the Client class is as normally.

.. code:: py

	from osu import Client
	
	client = Client(auth)
	
There's also an optional parameter limit_per_second which you can read about `here <api.html#osu.Client>`_.

The auth parameter for the client is an AuthHandler object. You can initialise it like so.

.. code:: py

	from osu import AuthHandler
	
	auth = AuthHandler(client_id, client_secret, redirect_uri)
	
AuthHandler also has an optional parameter scope, which is a Scope object. You can read more about it `here <api.html#osu.AuthHandler>`_.

All those involved client credential grant, but you can also use authorization code grant. Here's a full code example (this code is from the examples folder on the osu.py repo `here <https://github.com/Sheepposu/osu.py/blob/main/examples/auth_url.py>`_)

.. code:: py

	from osu import Client, AuthHandler, Scope
	import os


	client_id = int(os.getenv('osu_client_id'))
	client_secret = os.getenv('osu_client_secret')
	redirect_url = "http://127.0.0.1:8080"

	# Usually you would redirect a user on your site
	# to the authorize url with the redirect being back
	# to your site where you can grab the code and get
	# an access token.
	auth = AuthHandler(client_id, client_secret, redirect_url, Scope.identify())
	print(auth.get_auth_url())
	auth.get_auth_token(input("Code: "))  # The code is found in the redirect url (Ex. http://127.0.0.1:8080/?code=***********)
	client = Client(auth)
	
	mode = 'osu'
	user = client.get_own_data(mode)
	print(user.username)

If you want to learn more about what api requests you can make, either read about it on the `official osu!api v2 documentation <https://osu.ppy.sh/docs/index.html>`_ or read through the `osu.py documentation of the Client class <api.html#osu.Client>`_.
The names of the functions are modeled very similary to the title of the request listed on the osu!api v2 documentation.

AsynchronousClient
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This class is the exact same as the Client class, but all api request functions are asynchronous. You can see it in use `here <https://github.com/Sheepposu/osu.py/blob/main/examples/asynchronous_client.py>`_ on the github.

Scope
^^^^^^^^^^^^^^^^^^^^^^^^^^
The purpose of the scope class is to authorize under the desired scopes and to check the client scope against the scope required for a specific request.

You can create a Scope object in any of the ways shown below.

.. code:: py

	scope = Scope.default()  # public
	scope = Scope.identify() # public, identify
	scope = Scope(["pubic", "identify", "friends.read"])
	scope = Scope("public identify chat.write")
	
You can see a list of all valid scopes and their descriptions either on the `official osu!api v2 documentation <https://osu.ppy.sh/docs/index.html#scopes>`_ or on the `osu.py documentation of the Scope class <api.html#osu.Scope>`_.

More info to come soon...
