import pytest

from tests.util import as_async


class TestAsynchronousChangelog:
    @pytest.mark.asyncio
    async def test_get_changelog_build(self, client, sample_build):
        async_client = as_async(client)
        build = await async_client.get_changelog_build(sample_build["stream"], sample_build["version"])
        assert build

    @pytest.mark.asyncio
    async def test_get_changelog_listings(self, client):
        async_client = as_async(client)
        # TODO: test parameters
        ret = await async_client.get_changelog_listing()
        assert ret

    @pytest.mark.asyncio
    async def test_lookup_changelog_build(self, client, sample_build):
        async_client = as_async(client)
        # TODO: test parameters more
        build = await async_client.lookup_changelog_build(changelog=sample_build["version"])
        assert build
