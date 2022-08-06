import os
import random
from osu import Client, MatchSort


client_id = int(os.getenv('osu_client_id'))
client_secret = os.getenv('osu_client_secret')
redirect_url = "http://127.0.0.1:8080"

client = Client.from_client_credentials(client_id, client_secret, redirect_url)

data = client.get_matches(sort=MatchSort.OLDEST)
for match in data['matches']:
    print(f"{match.name} - https://osu.ppy.sh/community/matches/{match.id}")


match = client.get_match(random.choice(data['matches']).id)
print(match)
print(match.users)
print(match.events)
