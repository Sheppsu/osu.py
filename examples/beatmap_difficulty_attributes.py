from osu import Client, Mods, GameModeStr
import os


client_id = int(os.getenv('osu_client_id'))
client_secret = os.getenv('osu_client_secret')
redirect_url = "http://127.0.0.1:8080"

client = Client.from_credentials(client_id, client_secret, redirect_url)

bm_id = 3149839
HDHR = Mods.get_from_abbreviation("HD") | Mods.HardRock  # This is a valid argument for mods
# HDHR = Mods.get_from_list([Mods.Hidden, Mods.get_from_abbreviation("HR")])  # This is also way to construct the mods argument
HDDTHRFL = [HDHR, "DT", "Flashlight"]  # This is also a valid argument for mods
attributes = client.get_beatmap_attributes(bm_id, ruleset=GameModeStr.STANDARD, mods=HDDTHRFL)  # String names of the mods will automatically be parsed
print(f"Star rating: {attributes.star_rating}")
for attr in dir(attributes.mode_attributes):
    if not attr.startswith("__"):
        print(f"{attr}: {getattr(attributes.mode_attributes, attr)}")

