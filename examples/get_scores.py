from util_for_examples import get_user_client

client = get_user_client()

room = client.get_rooms()[49]
scores = client.get_scores(room.id, room.playlist[0].id)
print(scores)
