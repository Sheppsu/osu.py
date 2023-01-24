import pytest

from osu import CommentSort


class TestAsynchronousComment:
    def assert_comment_bundle(self, comments, sample_comment):
        assert comments
        assert comments.comments
        comment = comments.comments[0]
        assert comment
        assert comment.id == sample_comment["id"]
        assert comment.message == sample_comment["message"]
        assert comment.user_id == sample_comment["user_id"]

    @pytest.mark.asyncio
    async def test_get_comments(self, async_client, sample_comment):
        comments = await async_client.get_comments(sort=CommentSort.OLD)
        self.assert_comment_bundle(comments, sample_comment)

    @pytest.mark.asyncio
    async def test_post_new_comment(self, lazer_async_client):
        # This is kinda ehhhhhhhhh to implement
        pass

    @pytest.mark.asyncio
    async def test_get_comment(self, async_client, sample_comment):
        comments = await async_client.get_comment(sample_comment["id"])
        self.assert_comment_bundle(comments, sample_comment)

    @pytest.mark.asyncio
    async def test_edit_comment(self, lazer_async_client):
        # This is kinda ehhhhhhhhh to implement
        pass

    @pytest.mark.asyncio
    async def test_delete_comment(self, lazer_async_client):
        # This is kinda ehhhhhhhhh to implement
        pass

    @pytest.mark.asyncio
    async def test_add_comment_vote(self, lazer_async_client, sample_comment):
        comments = await lazer_async_client.add_comment_vote(sample_comment["id"])
        self.assert_comment_bundle(comments, sample_comment)

    @pytest.mark.asyncio
    async def test_remove_comment_vote(self, lazer_async_client, sample_comment):
        comments = await lazer_async_client.remove_comment_vote(sample_comment["id"])
        self.assert_comment_bundle(comments, sample_comment)
