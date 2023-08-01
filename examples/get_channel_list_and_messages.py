from util_for_examples import get_lazer_client


client = get_lazer_client()

me = client.get_own_data()
channels = client.get_channel_list()
channel = channels[0]
print("Joining "+channel.name)
client.join_channel(channel.channel_id, me.id)
print("Fetching recent messages")
messages = client.get_channel_messages(channel.channel_id)
print("10 recent messages:\n"+"\n".join(map(lambda m: f"{m.sender.username}: {m.content}", messages[-10:])))
print("Leaving "+channel.name)
client.leave_channel(channel.channel_id, me.id)
