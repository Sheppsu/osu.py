from osu import Client, CommentSort


client = Client()
comments = client.get_comments(sort=CommentSort.OLD)
print(comments.comments[0].url)  # Oldest comment

