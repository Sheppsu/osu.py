import os
import json
from osu import AuthHandler, Scope


CLIENT_ID = int(os.getenv("CLIENT_ID"))
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

DEV_CLIENT_ID = int(os.getenv("DEV_CLIENT_ID"))
DEV_CLIENT_SECRET = os.getenv("DEV_CLIENT_SECRET")
DEV_REDIRECT_URI = os.getenv("DEV_REDIRECT_URI")


auth = AuthHandler(
    CLIENT_ID,
    CLIENT_SECRET,
    REDIRECT_URI,
    Scope("public", "identify", "friends.read"),
)
auth.get_auth_token(input(f"{auth.get_auth_url()}\nCode: "))
with open("tests/auth.json", "w") as f:
    json.dump(auth.get_save_data(), f)

auth = AuthHandler(
    DEV_CLIENT_ID,
    DEV_CLIENT_SECRET,
    DEV_REDIRECT_URI,
    Scope("public", "identify", "friends.read", "forum.write", "chat.read")
)
auth.set_domain("dev.ppy.sh")
auth.get_auth_token(input(f"{auth.get_auth_url()}\nCode: "))
with open("tests/dev-auth.json", "w") as f:
    json.dump(auth.get_save_data(), f)
