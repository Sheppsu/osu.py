from pytest import fixture
from datetime import datetime, timezone


@fixture
def sample_news_post():
    yield dict(
        id=1257,
        slug="2023-01-21-new-featured-artist-kakichoco",
        author="pishifat",
        title="New Featured Artist: kakichoco",
    )


@fixture
def sample_wiki_page():
    yield dict(
        locale="en",
        path="Client/File_formats/osr_(file_format)",
        title=".osr (file format)",
    )


@fixture
def sample_match():
    yield dict(
        id=16161232,
        name="CWC 2015: (Netherlands) vs (Indonesia)",
        start_time=datetime(2015, 5, 16, 13, 51, 29, tzinfo=timezone.utc),
        end_time=datetime(2015, 5, 16, 14, 52, 45, tzinfo=timezone.utc),
    )
