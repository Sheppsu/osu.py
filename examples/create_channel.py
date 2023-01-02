from util_for_examples import get_lazer_client
from osu import ChatChannelType


client = get_lazer_client()
channel = client.create_channel(ChatChannelType.PM, 3)
print(channel)
print(channel.recent_messages)

# this won't work unless you have access to do announcements
channel = client.create_channel(ChatChannelType.ANNOUNCE, message="hi",
                                channel={"name": "haihai", "description": "hello"})
