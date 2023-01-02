from util_for_examples import get_lazer_client


beatmapset_id = 1545382
client = get_lazer_client()
count = client.favourite_beatmapset(beatmapset_id, True)
print(f"The beatmapset now has {count} favorites")
