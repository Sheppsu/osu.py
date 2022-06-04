from osu import Client
import os


client_id = int(os.getenv('osu_client_id'))
client_secret = os.getenv('osu_client_secret')
redirect_url = "http://127.0.0.1:8080"

client = Client.from_client_credentials(client_id, client_secret, redirect_url)

bm_id = 1031991  # PepeLaugh
discussions = client.get_beatmapset_discussions(beatmapset_id=1145452, message_types=["problem", "review", "suggestion"])
for disc in discussions['discussions']:
    post = disc.starting_post
    print("----------------------------------------------------")
    votes = client.get_beatmapset_discussion_votes(disc.id)["votes"]
    print(f"User{post.user_id} created Post{post.beatmapset_discussion_id} at {post.created_at} (Score: {sum(map(lambda vote: vote.score, votes))}): {post.message}")

    if disc.posts is not None:
        posts = disc.posts
    else:
        posts = client.get_beatmapset_discussion_posts(disc.id)["posts"]
    for post in posts:
        print("################################################")
        print(f"User{post.user_id} replied with Post{post.beatmapset_discussion_id} at {post.created_at}: {post.message}")


