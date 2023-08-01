from osu import (
    Client,
    BeatmapsetSearchFilter as Filter,
    BeatmapsetSearchStatus as Status,
    BeatmapsetSearchGeneral as General,
    BeatmapsetSearchExtra as Extra,
    BeatmapsetLanguage as Language,
    BeatmapsetGenre as Genre
)
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
    .set_language(Language.JAPANESE)
    .set_status(Status.RANKED)
)
russian_rock_loved = client.search_beatmapsets(
    Filter()
    .set_language(Language.ENGLISH)
    .set_genre(Genre.METAL)
    .set_status(Status.LOVED)
)
english_featured_artists_has_video_and_storyboard_including_converts = client.search_beatmapsets(
    Filter()
    .set_language(Language.ENGLISH)
    .set_generals([General.FEATURED_ARTISTS, General.CONVERTS])
    .set_extra([Extra.VIDEO, Extra.STORYBOARD])
    .set_status(Status.ANY)
)

print(f"Default: {default_search_result}\n")
print(f"Japanese ranked: {japanese_ranked}\n")
print(f"Russian rock loved: {russian_rock_loved}\n")
print(f"English featured artists has video and storyboard including converts: {english_featured_artists_has_video_and_storyboard_including_converts}")
