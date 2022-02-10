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
