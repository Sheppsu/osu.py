from util_for_examples import get_lazer_client


client = get_lazer_client()
osu_channel = client.get_channel(5)
print(osu_channel)
