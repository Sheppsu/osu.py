from util_for_examples import get_user_client
from osu import RoomType, RoomFilterMode


client = get_user_client()
realtime_rooms = client.get_rooms(room_type=RoomType.REALTIME)
print(realtime_rooms)
playlists = client.get_rooms(room_type=RoomType.PLAYLISTS)
print(playlists)
finished_playlists = client.get_rooms(room_type=RoomType.PLAYLISTS, limit=5, filter_mode=RoomFilterMode.ENDED)
print(finished_playlists)
my_rooms = client.get_rooms(filter_mode=RoomFilterMode.OWNED)
print(my_rooms)
