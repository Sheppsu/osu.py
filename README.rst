osu.py
-------

.. image:: https://discordapp.com/api/guilds/836755328493420614/widget.png?style=shield
   :target: https://discord.gg/Z2J6SSRPcE
   :alt: Discord server invite
.. image:: https://img.shields.io/pypi/v/osu.py.svg
   :target: https://pypi.python.org/pypi/osu.py
   :alt: PyPI version info

Easy to use API wrapper for osu!api written in Python. 
This uses osu!api v2, which is still under development. 
So some code that was originally working may break overnight. 
However, I'll do my best to fix any issues I find as quick as possible. 
You can report issues [here](https://github.com/Sheepposu/osu.py/issues) 
or make a [pull request](https://github.com/Sheepposu/osu.py/pulls) 
if you'd like to contribute.

# Installation
*Installing the current version out on pypi:*


.. code:: sh
    # Linux/macOS
    python3 -m pip install -U osu.py

    # Windows
    py -3 -m pip install -U osu.py

# Example

.. code:: py

    from osu import Client, AuthHandler


    client_id = 0
    client_secret = "***"
    redirect_uri = "http://127.0.0.1:8080"

    auth = AuthHandler(client_id, client_secret, redirect_uri)
    auth.get_auth_token()

    client = Client(auth)

    user_id = 14895608
    mode = 'osu'
    user = client.get_user(user_id, mode)
    print(user.username)

To learn more you can go to the documentation [here](https://osupy.readthedocs.io/en/latest/)
