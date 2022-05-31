from osu import Client
import os


client_id = int(os.getenv('osu_client_id'))
client_secret = os.getenv('osu_client_secret')
redirect_url = "http://127.0.0.1:8080"

client = Client.from_client_credentials(client_id, client_secret, redirect_url)

bm_id = 3149839
attributes = client.get_beatmap_attributes(bm_id, ruleset="osu")
for attr in dir(attributes.mode_attributes):
    if not attr.startswith("__"):
        print(f"{attr}: {getattr(attributes.mode_attributes, attr)}")

