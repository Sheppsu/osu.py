from util_for_examples import get_user_client


client = get_user_client()

room = client.get_rooms()[49]
data = client.get_room_leaderboard(room.id)
print(data['leaderboard'])
print(data['user_score'])
