from util_for_examples import get_user_client
import random

client = get_user_client()

rooms = client.get_rooms()
print(rooms, len(rooms))
room = random.choice(rooms)
scores = client.get_scores(room.id, room.playlist[0].id)
print(scores)
