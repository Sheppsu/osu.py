from dateutil import parser

from ..util import prettify


class Build:
    """
    **Attributes**

    created_at: :class:`datetime.datetime`

    display_version: :class:`str`

    id: :class:`int`

    update_stream: :class:`UpdateStream` or :class:`NoneType`

    users: :class:`int`

    version :class:`str` or :class:`NoneType`

    **Optional Attributes**

    changelog_entries: :class:`list`
        list of :class:`ChangelogEntry` objects. If the build has no changelog entries, a placeholder is generated.

    versions: :class:`Versions`
    """
    __slots__ = (
        "created_at", "display_version", "id", "update_stream", "users", "version",
        "changelog_entries", "versions"
    )

    def __init__(self, data):
        self.created_at = parser.parse(data["created_at"])
        self.display_version = data['display_version']
        self.id = data['id']
        self.update_stream = UpdateStream(data['update_stream']) if data.get('update_stream') is not None else None
        self.users = data['users']
        self.version = data['version']
        self.changelog_entries = list(map(ChangelogEntry, data['changelog_entries'])) if data.get("changelog_entries") is not None else []
        self.versions = Versions(data) if "versions" in data else None

    def __repr__(self):
        return prettify(self, 'id', 'version')


class Versions:
    """
    **Optional Attributes**

    next: :class:`Build` or :class:`NoneType`
        May be null if there is not a next build.

    previous: :class:`Build` or :class:`NoneType`
        May be null if there is not a previous build.
    """
    __slots__ = ("next", "previous")

    def __init__(self, data):
        self.next = Build(data['next']) if data.get('next') is not None else None
        self.previous = Build(data['previous']) if data.get('previous') is not None else None

    def __repr__(self):
        fields = [getattr(self, slot) for slot in self.__slots__ if getattr(self, slot, None)]
        return prettify(self, *fields)


class UpdateStream:
    """
    **Attributes**

    display_name: :class:`str` or :class:`NoneType`

    id: :class:`int`

    is_featured: :class:`bool`

    name: :class:`str`

    **Optional Attributes**

    latest_build: :class:`Build`

    user_count: :class:`int`
    """
    __slots__ = (
        "display_name", "id", "is_featured", "name",
        "latest_build", "user_count"
    )

    def __init__(self, data):
        self.display_name = data['display_name']
        self.id = data['id']
        self.is_featured = data['is_featured']
        self.name = data['name']
        self.latest_build = Build(data['latest_build']) if 'latest_build' in data else None
        self.user_count = data.get('user_count', None)

    def __repr__(self):
        return prettify(self, 'display_name')


class ChangelogEntry:
    """
    **Attributes**

    category: :class:`str`

    created_at: :class:`datetime.datetime` or :class:`NoneType`

    github_pull_request_id: :class:`int` or :class:`NoneType`

    github_url: :class:`str` or :class:`NoneType`

    id: :class:`int` or :class:`NoneType`

    major: :class:`bool`

    repository: :class:`str` or :class:`NoneType`

    title: :class:`str` or :class:`NoneType`

    type: :class:`str`

    url: :class:`str` or :class:`NoneType`

    **Optional Attributes**

    github_user: :class:`GithubUser`
        If the changelog entry has no GitHub user, a placeholder is generated.

    message: :class:`str`
        Entry message in Markdown format. Embedded HTML is allowed.

    message_html: :class:`str`
        Entry message in HTML format.
    """
    __slots__ = (
        "category", "created_at", "github_pull_request_id", "github_url",
        "id", "major", "repository", "title", "type", "url", "github_user",
        "message", "message_html"
    )

    def __init__(self, data):
        self.category = data['category']
        self.created_at = parser.parse(data['created_at']) if data['created_at'] is not None else None
        self.github_pull_request_id = data['github_pull_request_id']
        self.github_url = data['github_url']
        self.id = data['id']
        self.major = data['major']
        self.repository = data['repository']
        self.title = data['title']
        self.type = data['type']
        self.url = data['url']
        self.github_user = GithubUser(data['github_user']) if 'github_user' in data else None
        self.message = data.get('message', '')
        self.message_html = data.get('message_html', '')

    def __repr__(self):
        return prettify(self, 'title', 'major', 'created_at')


class GithubUser:
    """
    **Attributes**

    display_name: :class:`str`

    github_url: :class:`str` or :class:`NoneType`

    id: :class:`int` or :class:`NoneType`

    osu_username: :class:`str` or :class:`NoneType`

    user_id: :class:`int` or :class:`NoneType`

    user_url: :class:`str` or :class:`NoneType`
    """
    __slots__ = (
        "display_name", "github_url", "id", "osu_username",
        "user_id", "user_url"
    )

    def __init__(self, data):
        self.display_name = data['display_name']
        self.github_url = data['github_url']
        self.id = data['id']
        self.osu_username = data['osu_username']
        self.user_id = data['user_id']
        self.user_url = data['user_url']

    def __repr__(self):
        return prettify(self, 'display_name')
