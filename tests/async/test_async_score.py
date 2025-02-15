import pytest
import asyncio

from osu import SoloScore, LegacyScore, Mods


class TestAsynchronousScore:
    @pytest.mark.asyncio
    async def test_get_beatmap_scores(self, async_client, sample_beatmap_scores):
        scores = await async_client.get_beatmap_scores(sample_beatmap_scores["beatmap_id"])
        assert scores
        assert len(scores) == 50

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
        assert round(score.accuracy, 4) == round(sample_user_beatmap_score["accuracy"], 4)

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
                "mods": score.mods,
            }
            for score in scores
        ]
        for score1, score2 in zip(scores, sample_user_beatmap_scores["scores"]):
            assert round(score1["accuracy"], 4) == round(score2["accuracy"], 4)
            assert len(score1["mods"]) == len(score2["mods"])
            for mod in score1["mods"]:
                assert mod.mod in score2["mods"]

    @pytest.mark.asyncio
    async def test_get_score_by_id(self, async_client, sample_scores):
        for sample_score in sample_scores:
            score = await async_client.get_score_by_id_only(sample_score["id"])
            assert score
            assert score.id == sample_score["id"]
            assert score.user_id == sample_score["user_id"]

    @pytest.mark.asyncio
    async def test_get_all_scores(self, async_client):
        ret = await async_client.get_all_scores()
        assert ret

        await asyncio.sleep(0.5)

        new_ret = await async_client.get_all_scores(cursor=ret.cursor)
        assert new_ret
        assert new_ret.scores[0].id != ret.scores[0].id
