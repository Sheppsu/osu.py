from osu import Client
import os


client_id = int(os.getenv('CLIENT_ID'))
client_secret = os.getenv('CLIENT_SECRET')
redirect_url = None

client = Client.from_credentials(client_id, client_secret, redirect_url)

result = client.get_topic_and_posts(1699086)
print(result.topic.title+"\n"+("#"*len(result.topic.title)))
users = client.get_users(tuple(set(map(lambda p: p.user_id, result.posts))))
for post in result.posts:
    user = next(filter(lambda u: u.id == post.user_id, users))
    print(f"{user.username}: {post.body.raw}")
