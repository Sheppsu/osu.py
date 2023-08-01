from osu import Client, CommentSort, ObjectType


client = Client()
comments = client.get_comments(sort=CommentSort.OLD)
print(comments.comments[0])  # Oldest comment

comments = client.get_comments(commentable_type=ObjectType.Beatmapset, commentable_id=41823)
print(comments.pinned_comments)  # Pinned comments on osu.ppy.sh/beatmapsets/41823
