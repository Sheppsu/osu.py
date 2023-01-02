from util_for_examples import get_lazer_client
from time import sleep


client = get_lazer_client()
comment_id = 2195224
print(client.add_comment_vote(comment_id))
sleep(5)
print(client.remove_comment_vote(comment_id))
