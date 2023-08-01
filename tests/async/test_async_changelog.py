import pytest


class TestAsynchronousChangelog:
    @pytest.mark.asyncio
    async def test_get_changelog_build(self, async_client, sample_build):
        build = await async_client.get_changelog_build(sample_build["stream"], sample_build["version"])
        assert build

    @pytest.mark.asyncio
    async def test_get_changelog_listings(self, async_client):
        # TODO: test parameters
        ret = await async_client.get_changelog_listing()
        assert ret

    @pytest.mark.asyncio
    async def test_lookup_changelog_build(self, async_client, sample_build):
        # TODO: test parameters more
        build = await async_client.lookup_changelog_build(changelog=sample_build["version"])
        assert build
