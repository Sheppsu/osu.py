from util_for_examples import get_lazer_client
from osu import ObjectType
from time import sleep


client = get_lazer_client()
comment = client.post_comment(ObjectType.Beatmapset, 1794009, "aaaaaa")
print(comment)
sleep(5)
new_comment = client.edit_comment(comment.comments[0].id, "bbbbbbb")
print(new_comment)
sleep(5)
deleted_comment = client.delete_comment(comment.comments[0].id)
print(deleted_comment)
