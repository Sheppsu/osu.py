from pytest import fixture


@fixture
def sample_news_post():
    yield dict(
        id=1257,
        slug="2023-01-21-new-featured-artist-kakichoco",
        author="pishifat",
        title="New Featured Artist: kakichoco"
    )


@fixture
def sample_wiki_page():
    yield dict(
        locale="en",
        path="Client/File_formats/Osr_(file_format)",
        title=".osr (file format)",
    )
