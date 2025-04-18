import pytest

from osu import CommentSort

from tests.util import as_async


class TestAsynchronousComment:
    def _assert_comment_bundle(self, comments, sample_comment):
        assert comments
        assert comments.comments
        comment = comments.comments[0]
        assert comment
        assert comment.id == sample_comment["id"]
        assert comment.message == sample_comment["message"]
        assert comment.user_id == sample_comment["user_id"]

    @pytest.mark.asyncio
    async def test_get_comments(self, client, sample_comment):
        async_client = as_async(client)
        comments = await async_client.get_comments(sort=CommentSort.OLD)
        self._assert_comment_bundle(comments, sample_comment)

    @pytest.mark.asyncio
    async def test_get_comment(self, client, sample_comment):
        async_client = as_async(client)
        comments = await async_client.get_comment(sample_comment["id"])
        self._assert_comment_bundle(comments, sample_comment)
