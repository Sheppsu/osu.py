osu.py
-------

.. image:: https://discordapp.com/api/guilds/836755328493420614/widget.png?style=shield
   :target: https://discord.gg/Z2J6SSRPcE
   :alt: Discord server invite
.. image:: https://img.shields.io/pypi/v/osu.py.svg
   :target: https://pypi.python.org/pypi/osu.py
   :alt: PyPI version info
.. image:: https://static.pepy.tech/personalized-badge/osu-py?period=month&units=international_system&left_color=blue&right_color=brightgreen&left_text=Downloads/month
   :target: https://pepy.tech/project/osu-py
   :alt: Download metric

Easy to use API wrapper for osu!api v2 written in Python.

Major features/capabilties:
 - Client class which carries out all api requests.
 - AsynchronousClient class which is the same as Client but all api request functions are asynchronous.
 - NotificationWebsocket class for using the notification websocket feature of osu api v2
 - Currently implements all endpoints including undocumented ones.
 - Builtin rate limit handling
 - Storage efficient objects used to contain almost all the data returned from osu.py for any given api request.
 - Support for Authorization Code Grant and Client Credentials Grant.
 - Refresh and access token is automatically managed.
 - Support for all scopes (even lazer which is not usable by the general public).
 - Documentation that covers everything osu.py is capable of.
This uses osu!api v2, which is still under development. 
So some code that was originally working may break overnight. 
However, I'll do my best to fix any issues I find as quick as possible. 
You can report issues `here <https://github.com/Sheepposu/osu.py/issues>`_
or make a `pull requests <https://github.com/Sheepposu/osu.py/pulls>`_
if you'd like to contribute. General discussion can go `here <https://github.com/Sheepposu/osu.py/discussions>`_
or you can join the `Discord server <https://discord.gg/Z2J6SSRPcE>`_

Installation
------------

.. code:: sh

    # Installs the latest version out on pypi

    # Linux/macOS
    python3 -m pip install -U osu.py

    # Windows
    py -3 -m pip install -U osu.py

    # Installing straight from github (downloads latest code which may contain bugs)
    [python prefix used above] pip install git+https://github.com/Sheepposu/osu.py.git

Example
-------

.. code:: py

	from osu import Client

	client_id = 0
	client_secret = "***"
	redirect_url = "http://127.0.0.1:8080"

	client = Client.from_client_credentials(client_id, client_secret, redirect_url)

	user_id = 14895608
	mode = 'osu'
	user = client.get_user(user_id, mode)
	print(user.username)

You can see more examples `here <https://github.com/Sheepposu/osu.py/tree/main/examples>`_, 
check out the `guide <https://osupy.readthedocs.io/en/latest/guide.html>`_ if you're new to osu.py, and 
to learn more you can go to the `documentation <https://osupy.readthedocs.io/en/latest/>`_
