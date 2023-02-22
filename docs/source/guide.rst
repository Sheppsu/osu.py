Getting started  with osu.py
============================

Structure of osu.py
^^^^^^^^^^^^^^^^^^^
There are five major classes responsible for making and assisting with api requests/authentication:
Client, Path, HTTPHandler, RateLimitHandler, and AuthHandler.
 - Client contains all functions that contain the logic for making a request to an endpoint. These functions use the Path and HTTPHandler classes to make the actual request. The function creates a Path object and passes it to HTTPHandler.make_request.
 - Path is a class that contains information about how to make a request and to where. It's instantiated using classmethods and passed to HTTPHandler when making a request.
 - HTTPHandler contains the logic for making any request based on the information given to it. The Path object tells it the endpoint and auth requirements and all other request-specific details specified by the function calling make_request. The required authentication information is provided by an AuthHandler object and HTTPHandler relies on RateLimitHandler to stay within the specified rate limit.
 - RateLimitHandler keeps track of all requests performed and helps the HTTPHandler not go over the rate limit.
 - AuthHandler contains all the logic for authorizing with the api, managing the auth token and also automatically refreshing it when necessary.

Client and AuthHandler
^^^^^^^^^^^^^^^^^^^^^^^^^^^
The simplest way to initialise the client class using client credential grant is like so.

.. code:: py

	from osu import Client
	
	client = Client.from_client_credentials(client_id, client_secret, redirect_uri)
	
If you're unsure of where to obtain a client id and secret, read `here <https://osu.ppy.sh/docs/index.html#managing-oauth-applications>`_.
	
There are also four more optional arguments you can use: scope, code, request_wait_time, and limit_per_minute.
You can read more about them `here <api.html#osu.Client.from_client_credentials>`_.

The other way to initialise the Client class is as normally.

.. code:: py

	from osu import Client
	
	client = Client(auth)
	
There are three optional parameters - request_wait_time, limit_per_minute, and use_lazer - which you can read about `here <api.html#osu.Client>`_.

The auth parameter for the client is an AuthHandler object. You can initialise it like so.

.. code:: py

	from osu import AuthHandler
	
	auth = AuthHandler(client_id, client_secret, redirect_uri)
	auth.get_auth_token()
	
AuthHandler also has an optional parameter scope, which is a Scope object. You can read more about it `here <api.html#osu.AuthHandler>`_.

All those involved client credential grant, but you can also use authorization code grant.
Here's a full code example (this code is from the examples folder on the osu.py repo `here <https://github.com/Sheepposu/osu.py/blob/main/examples/auth_url.py>`_)

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

If you want to learn more about what api requests you can make,
either read about it on the `official osu!api v2 documentation <https://osu.ppy.sh/docs/index.html>`_ or
read through the `osu.py documentation of the Client class <api.html#osu.Client>`_.
The names of the functions are modeled very similary to the title of the request listed on the osu!api v2 documentation.

Finally, you can use your osu username and password to use Password grant.
Password grant is the only method currently of gaining access to the lazer endpoints and is also the grant that osu!lazer uses with the api.
This also authorizes under being able to use all scopes by default and does not have an option to not do so.

It's simple just like the client credential grant:

.. code:: py

	from osu import Client
	
	client = Client.from_osu_credentials(username, password)
	
This method also has two optional arguments: request_wait_time and limit_per_minute. 
You can read about them under the `Client's init docs <api.html#osu.Client>`_.

This method of authorization uses the LazerAuthHandler class as opposed to the AuthHandler class.

.. code:: py

	from osu import LazerAuthHandler
	
	auth = LazerAuthHandler(username, password)
	auth.get_auth_token()

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
	scope = Scope("pubic", "identify", "friends.read")
	
You can see a list of all valid scopes and their descriptions either on the `official osu!api v2 documentation <https://osu.ppy.sh/docs/index.html#scopes>`_ or on the `osu.py documentation of the Scope class <api.html#osu.Scope>`_.

You can look at more code examples `here <https://github.com/Sheepposu/osu.py/tree/main/examples>`_.
