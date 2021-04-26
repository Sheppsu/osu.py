osu.py
-------

Easy to use API wrapper for osu!api written in Python. 
This uses osu!api v2, which is still under development. 
So some code that was originally working may break overnight. 
However, I'll do my best to fix any issues I find as quick as possible. 
You can report issues [here](https://github.com/Sheepposu/osu.py/issues) 
or make a [pull request](https://github.com/Sheepposu/osu.py/pulls) 
if you'd like to contribute.

# Installation
*Installing the current version out on pypi:*

Linux/macOS
```commandline
python3 -m pip install -U osu.py
```
Windows
```commandline
py -3 -m pip install -U osu.py
```

# Example
```Python
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
```

To learn more you can go to the documentation [here](https://osupy.readthedocs.io/en/latest/)
