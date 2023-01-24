from util_for_examples import get_lazer_client


client = get_lazer_client()
room_id = 239531
summer2022 = client.get_room(room_id)
playlist_item = summer2022.playlist[0]
scores = client.get_scores(summer2022.id, playlist_item.id)
print(scores)
colgate_enjoyer = 20198397
colgate_enjoyer_best_score = client.get_user_highscore(summer2022.id, playlist_item.id, colgate_enjoyer)
print(colgate_enjoyer_best_score)
score = client.get_score(summer2022.id, playlist_item.id, colgate_enjoyer_best_score.id)
print(score)
