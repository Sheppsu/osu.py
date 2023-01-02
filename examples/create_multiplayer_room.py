from util_for_examples import get_lazer_client
from osu import PlaylistItemUtil, GameModeInt
from time import sleep


client = get_lazer_client()
me = client.get_own_data()
room_name = "test"
room_password = "aaaaaaaaaaaaaaaaaaaaaaaa"
beatmap = PlaylistItemUtil(3461417, GameModeInt.STANDARD)
room = client.create_multiplayer_room(room_name, beatmap, password=room_password)
print(room)
client.join_user_to_room(room.id, me.id, room_password)
sleep(10)
client.kick_user_from_room(room.id, me.id)
