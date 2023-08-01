class TestChangelog:
    def test_get_changelog_build(self, client, sample_build):
        build = client.get_changelog_build(sample_build["stream"], sample_build["version"])
        assert build

    def test_get_changelog_listings(self, client):
        # TODO: test parameters
        ret = client.get_changelog_listing()
        assert ret

    def test_lookup_changelog_build(self, client, sample_build):
        # TODO: test parameters more
        build = client.lookup_changelog_build(changelog=sample_build["version"])
        assert build
