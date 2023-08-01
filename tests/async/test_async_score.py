import pytest

from osu import SoloScore, LegacyScore, Mods


class TestAsynchronousScore:
    @pytest.mark.asyncio
    async def test_get_beatmap_scores(self, async_client, sample_beatmap_scores):
        scores = await async_client.get_beatmap_scores(sample_beatmap_scores["beatmap_id"])
        for received_score, sample_score in zip(scores.scores[:3], sample_beatmap_scores["scores"]):
            assert isinstance(received_score, LegacyScore) or isinstance(received_score, SoloScore)
            assert received_score.id == sample_score["id"]
            assert received_score.user_id == sample_score["user_id"]
            assert received_score.max_combo == sample_score["max_combo"]

    @pytest.mark.asyncio
    async def test_get_lazer_beatmap_scores(self, async_client, sample_beatmap_scores):
        scores = await async_client.get_lazer_beatmap_scores(sample_beatmap_scores["beatmap_id"])
        for score in scores.scores:
            assert isinstance(score, SoloScore)

    @pytest.mark.asyncio
    async def test_get_user_beatmap_score(self, async_client, sample_user_beatmap_score):
        score = (
            await async_client.get_user_beatmap_score(
                beatmap=sample_user_beatmap_score["beatmap_id"],
                user=sample_user_beatmap_score["user_id"],
            )
        ).score
        assert score
        assert score.user_id == sample_user_beatmap_score["user_id"]
        assert score.accuracy == sample_user_beatmap_score["accuracy"]

    @pytest.mark.asyncio
    async def test_get_user_beatmap_scores(self, async_client, sample_user_beatmap_scores):
        scores = await async_client.get_user_beatmap_scores(
            beatmap=sample_user_beatmap_scores["beatmap_id"],
            user=sample_user_beatmap_scores["user_id"],
        )
        assert scores
        scores = [
            {
                "accuracy": score.accuracy,
                "mods": Mods.parse_any_list([mod.mod.name for mod in score.mods]) if score.mods else None,
            }
            for score in scores
        ]
        for score in scores:
            assert score in sample_user_beatmap_scores["scores"]

    @pytest.mark.asyncio
    async def test_get_score_by_id(self, async_client, sample_scores):
        for sample_score in sample_scores:
            score = await async_client.get_score_by_id(sample_score["mode"], sample_score["id"])
            assert score
            assert score.id == sample_score["id"]
            assert score.user_id == sample_score["user_id"]
            assert score.accuracy == sample_score["accuracy"]
            assert (score.score if hasattr(score, "score") else score.total_score) == sample_score["score"]
