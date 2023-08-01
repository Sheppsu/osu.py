from util_for_examples import get_lazer_client


client = get_lazer_client()

osu_channel_id = 5
me = client.get_own_data()

client.join_channel(osu_channel_id, me.id)
osu_channel = client.get_channel(osu_channel_id)
client.leave_channel(osu_channel_id, me.id)
print(osu_channel)
