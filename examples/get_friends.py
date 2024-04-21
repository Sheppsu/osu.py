from osu import Client, AuthHandler, Scope
import os


auth = AuthHandler(
    int(os.getenv('CLIENT_ID')),
    os.getenv('CLIENT_SECRET'),
    os.getenv('REDIRECT_URI'),
    Scope("public", "identify", "friends.read")
)
auth.get_auth_token(input(f"{auth.get_auth_url()}\nCode: "))
client = Client(auth)

print(client.get_friends())
