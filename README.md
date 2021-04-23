osu.py
-------

Easy to use API wrapper for osu!api written in Python.

# Installation
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
