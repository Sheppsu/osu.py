from osu import Client, AuthHandler, Scope
import os


auth = AuthHandler(int(os.getenv('osu_client_id')), os.getenv('osu_client_secret'),
                   os.getenv('osu_redirect_uri'), Scope('friends.read'))
print(auth.get_auth_url())
auth.get_auth_token(input("Code: "))
client = Client(auth)

print(client.get_friends())
