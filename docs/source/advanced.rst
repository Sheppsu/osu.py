Advanced usage of osu.py
========================

Structure of osu.py
-------------------
To start, let's go over the structure of osu.py.

Path
^^^^
:class:`osu.Path` defines an endpoint and how to make a request to it.
It's used by the client classes to specify endpoints and you can
use it if you want to use an endpoint that's not supported by osu.py.

HTTPHandler
^^^^^^^^^^^
:class:`osu.http.HTTPHandler` and :class:`osu.asyncio.http.AsynchronousHTTPHandler` are
in charge of handling requests and used by the client classes. They interpret
:class:`osu.Path` objects to make requests.

AuthHandler
^^^^^^^^^^^
:class:`osu.AuthHandler` and :class:`osu.AsynchronousAuthHandler` manage authentication
with the api. When the api token expires, they automatically renew it. They both inherit
from :class:`osu.FunctionalAuthHandler`, which inherits from :class:`BaseAuthHandler`.
The functional and base auth handler classes can be used if you need to implement some
custom authentication for whatever reason.

Client
^^^^^^
:class:`osu.Client` and :class:`osu.AsynchronousClient` implements the previous 3 classes
to easily make requests and just worry about user-facing stuff.

Making custom requests
----------------------
You can utilize api endpoints that aren't implemented by creating a :class:`osu.Client` and
using its ``http`` attribute, which is an :class:`osu.http.HTTPHandler`. Create a
:class:`osu.Path` object to represent the endpoint, pass it to
:func:`osu.http.HTTPHandler.make_request`, and fill in other necessary parameters.

.. code:: py

    client = Client.from_credentials(0, "****", None)
    resp = client.http.make_request(
        Path("get", "matches", "public"),
        limit=10
    )
    matches = list(map(Match, resp["matches"]))

Using a different domain/url
---------------------------------
You can use :func:`osu.Client.set_domain` or :func:`osu.BaseAuthHandler.set_domain` to
set the domain used for api requests. If you set the domain on the auth handler and then
pass it to a client, the client's domain will be updated automatically. However, this
assumes the domain uses https. Normal example and workaround for http is below.

.. code:: py

    client = Client.from_credentials(0, "****", None)
    client.set_domain("dev.ppy.sh")

    # or

    auth = AuthHandler(0, "****", None)
    auth.set_domain("dev.ppy.sh")
    client = Client(auth)

    # workaround for http

    client = Client.from_credentials(0, "****", None)
    client.http.base_url = "http://localhost:8080/api/v2/"
    client.auth.auth_url = "http://localhost:8080/oauth/authorize/"
    client.auth.token_url = "http://localhost:8080/oauth/token/"

Using a different api version
-----------------------------
The client classes have a ``api_version`` init parameter and ``set_api_version`` function
for specifying to use a certain version. By default, the version is set to the current date
at the time of its initialization (to avoid random breaking changes at runtime).
This could be utilized if you want to access older response formats from the api.