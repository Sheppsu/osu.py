from util_for_examples import get_lazer_client
from osu import UserBeatmapType, PlaylistItemUtil


client = get_lazer_client()
me = client.get_own_data()
# Get favorited beatmaps and pick out the highest difficulty from each
favorites = client.get_user_beatmaps(me.id, UserBeatmapType.FAVOURITE, 10)
favorites = [sorted([
    (beatmap.id, beatmap.mode_int, beatmap.difficulty_rating) for beatmap in beatmapset.beatmaps
], key=lambda item: item[2])[-1][:2] for beatmapset in favorites]
room = client.create_playlist(f"{me.username}'s favorites", list(map(
    lambda beatmap: PlaylistItemUtil(beatmap[0], beatmap[1]), favorites)),
                              30)
print(room)
