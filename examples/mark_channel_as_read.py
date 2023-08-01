from util_for_examples import get_lazer_client
from osu import Client


client: Client = get_lazer_client()

ret = client.get_updates()
channel = ret.presence[-1]
messages = client.get_channel_messages(channel.channel_id, limit=10)
print(f"Last 10 messages of {channel.name} ({channel.channel_id})")
for message in messages:
    print(f"{message.sender.username}: {message.content}")
client.mark_channel_as_read(channel.channel_id, messages[-1].message_id)
