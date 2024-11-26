from osu import Client, MessageType
import os


client_id = int(os.getenv('osu_client_id'))
client_secret = os.getenv('osu_client_secret')
redirect_url = "http://127.0.0.1:8080"

client = Client.from_credentials(client_id, client_secret, redirect_url)

bm_id = 1031991  # PepeLaugh
result = client.get_beatmapset_discussions(beatmapset_id=1145452, message_types=[MessageType.PROBLEM, MessageType.REVIEW, MessageType.SUGGESTION])


def get_user(users, user_id):
    for user in users:
        if user.id == user_id:
            return user


for disc in result.discussions:
    post = disc.starting_post
    print("----------------------------------------------------")
    votes_result = client.get_beatmapset_discussion_votes(disc.id)
    votes = votes_result.votes
    user = get_user(result.users, post.user_id)
    print(f"{user.username} created {disc.message_type.value} Post{post.beatmapset_discussion_id} at {post.created_at} (Score: {sum(map(lambda vote: vote.score, votes))}): {post.message}")

    if disc.posts is not None:
        posts = disc.posts
        posts_users = result.users
    else:
        posts_result = client.get_beatmapset_discussion_posts(disc.id)
        posts = posts_result.posts
        posts_users = posts_result.users
    for post in sorted(posts, key=lambda p: p.created_at):
        print("################################################")
        user = get_user(posts_users, post.user_id)
        print(f"{user.username} replied with Post{post.beatmapset_discussion_id} at {post.created_at}: {post.message}")


