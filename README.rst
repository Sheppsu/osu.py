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
.. image:: https://readthedocs.org/projects/osupy/badge/?version=v1.0.0&style=flat
   :target: https://osupy.readthedocs.io
   :alt: Documentation

Easy to use API wrapper for osu!api v2 written in Python.
Has a high-level interface while still allowing ways to do more complex things.

Major features/capabilties
--------------------------
- Client class which carries out all api requests.
- AsynchronousClient class which is the same as Client but all api request functions are asynchronous.
- NotificationWebsocket class for using the notification websocket feature of osu api v2.
- Support for Authorization Code Grant and Client Credentials Grant.
- Builtin rate limit handling
- Storage efficient objects used to contain almost all the data returned from osu.py for any given api request.
- Refresh and access token is automatically managed.
- Utility functions and classes that make your life easier.
- Documentation that covers everything osu.py is capable of.

Installation
------------

.. code:: sh

    # Installs the latest version out on pypi

    # Linux/macOS
    python3 -m pip install -U osu.py

    # Windows
    py -3 -m pip install -U osu.py

    # Installing straight from github (downloads latest code, which is not guaranteed to be stable)
    [python prefix used above] -m pip install git+https://github.com/Sheepposu/osu.py.git
	
	# Install with features
	[python prefix] -m pip install -U osu.py[replay,notifications]
	
	# Install from github with features
	git clone https://github.com/sheppsu/osu.py
	cd osu.py
	[python prefix] -m pip install -U .[replay,notifications]

Example
-------

.. code:: py

	from osu import Client, GameModeStr

	client = Client.from_client_credentials(0, "*****", None)
	user = client.get_user(14895608, GameModeStr.STANDARD)
	print(user)

Links
-----

- `Issues <https://github.com/Sheepposu/osu.py/issues>`_
- `Contribute <https://github.com/Sheepposu/osu.py/pulls>`_
- `Discussion <https://github.com/Sheepposu/osu.py/discussions>`_
- `Discord server <https://discord.gg/Z2J6SSRPcE>`_
- `Example code <https://github.com/Sheepposu/osu.py/tree/main/examples>`_
- `Getting started guide <https://osupy.readthedocs.io/en/latest/guide.html>`_
- `Documentation <https://osupy.readthedocs.io>`_
