from util_for_examples import get_lazer_client
from osu import ObjectType
from time import sleep


client = get_lazer_client()
comment = client.post_comment(ObjectType.Beatmapset, 1937382, "aaaaaa")
print(comment)
sleep(10)  # time to check it
new_comment = client.edit_comment(comment.comments[0].id, "bbbbbbb")
print(new_comment)
sleep(10)  # time to check it
deleted_comment = client.delete_comment(comment.comments[0].id)
print(deleted_comment)
