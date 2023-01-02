from util_for_examples import get_lazer_client


client = get_lazer_client()
me = client.get_own_data()
channel = client.join_channel(5, me.id)
print(f"Joined {channel.name}")
client.leave_channel(5, me.id)
print(f"Left {channel.name}")
