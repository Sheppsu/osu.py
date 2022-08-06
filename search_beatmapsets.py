from osu import Client, BeatmapsetSearchFilter as Filter, BeatmapsetSearchStatus as Status, \
    BeatmapsetSearchGeneral as General, BeatmapsetSearchExtra as Extra
import os


client_id = int(os.getenv('osu_client_id'))
client_secret = os.getenv('osu_client_secret')
redirect_url = "http://127.0.0.1:8080"

client = Client.from_client_credentials(client_id, client_secret, redirect_url)


default_search_result = client.search_beatmapsets()
recently_qualified = client.search_beatmapsets(
    Filter()
    .set_status(Status.QUALIFIED)
)
japanese_ranked = client.search_beatmapsets(
    Filter()
    .set_language('Japanese')
    .set_status(Status.RANKED)
)
russian_rock_loved = client.search_beatmapsets(
    Filter()
    .set_genre('Rock')
    .set_language('Japanese')
    .set_status(Status.LOVED)
)
english_featured_artists_has_video_and_storyboard_including_converts = client.search_beatmapsets(
    Filter()
    .set_language('English')
    .set_generals([General.FEATURED_ARTISTS, General.CONVERTS])
    .set_extra([Extra.VIDEO, Extra.STORYBOARD])
)
