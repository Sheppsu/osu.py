class TestScore:
    def test_get_beatmap_scores(self, client, sample_beatmap_scores):
        scores = client.get_beatmap_scores(sample_beatmap_scores["beatmap_id"])
        for received_score, sample_score in zip(scores.scores[:3], sample_beatmap_scores["scores"]):
            assert received_score.id == sample_score["id"]
            assert received_score.user_id == sample_score["user_id"]
            assert received_score.max_combo == sample_score["max_combo"]

    def test_get_lazer_beatmap_scores(self, client, sample_beatmap_scores):
        client.get_lazer_beatmap_scores(sample_beatmap_scores["beatmap_id"])
        # TODO: add some asserts

    def test_get_user_beatmap_score(self, client, sample_user_beatmap_score):
        score = (client.get_user_beatmap_score(
            beatmap=sample_user_beatmap_score["beatmap_id"],
            user=sample_user_beatmap_score["user_id"],
        )).score
        assert score
        assert score.user_id == sample_user_beatmap_score["user_id"]
        assert score.accuracy == sample_user_beatmap_score["accuracy"]

    def test_get_user_beatmap_scores(self, client, sample_user_beatmap_scores):
        scores = client.get_user_beatmap_scores(
            beatmap=sample_user_beatmap_scores["beatmap_id"],
            user=sample_user_beatmap_scores["user_id"],
        )
        assert scores
        for score in scores:
            keys = sample_user_beatmap_scores["scores"][0].keys()
            assert {key: getattr(score, key) for key in keys} in sample_user_beatmap_scores["scores"]

    def test_get_score_by_id(self, client, sample_scores):
        for sample_score in sample_scores:
            score = client.get_score_by_id(sample_score["mode"], sample_score["id"])
            assert score
            assert score.id == sample_score["id"]
            assert score.user_id == sample_score["user_id"]
            assert score.accuracy == sample_score["accuracy"]
            assert score.accuracy == sample_score["accuracy"]
            assert score.score == sample_score["score"]
