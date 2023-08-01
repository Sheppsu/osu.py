from dateutil import parser
from typing import Optional, List, TYPE_CHECKING

from ..util import prettify, get_optional, get_optional_list


if TYPE_CHECKING:
    from datetime import datetime


class Build:
    """
    **Attributes**

    created_at: :class:`datetime.datetime`

    display_version: :class:`str`

    id: :class:`int`

    update_stream: Optional[:class:`UpdateStream`]

    users: :class:`int`

    version Optional[:class:`str`]

    changelog_entries: Optional[List[:class:`ChangelogEntry`]]
        If the build has no changelog entries, a placeholder is generated.

    versions: Optional[:class:`Versions`]
    """

    __slots__ = (
        "created_at",
        "display_version",
        "id",
        "update_stream",
        "users",
        "version",
        "changelog_entries",
        "versions",
    )

    def __init__(self, data):
        self.created_at: datetime = parser.parse(data["created_at"])
        self.display_version: str = data["display_version"]
        self.id: int = data["id"]
        self.update_stream: Optional[UpdateStream] = get_optional(data, "update_stream", UpdateStream)
        self.users: int = data["users"]
        self.version: Optional[str] = data["version"]
        self.changelog_entries: Optional[List[ChangelogEntry]] = get_optional_list(
            data, "changelog_entries", ChangelogEntry
        )
        self.versions: Optional[Versions] = get_optional(data, "versions", Versions)

    def __repr__(self):
        return prettify(self, "id", "version")


class Versions:
    """
    **Optional Attributes**

    next: Optional[:class:`Build`]
        May be null if there is not a next build.

    previous: Optional[:class:`Build`]
        May be null if there is not a previous build.
    """

    __slots__ = ("next", "previous")

    def __init__(self, data):
        self.next: Optional[Build] = get_optional(data, "next", Build)
        self.previous: Optional[Build] = get_optional(data, "previous", Build)

    def __repr__(self):
        fields = [getattr(self, slot) for slot in self.__slots__ if getattr(self, slot, None)]
        return prettify(self, *fields)


class UpdateStream:
    """
    **Attributes**

    display_name: Optional[:class:`str`]

    id: :class:`int`

    is_featured: :class:`bool`

    name: :class:`str`

    latest_build: Optional[:class:`Build`]

    user_count: Optional[:class:`int`]
    """

    __slots__ = (
        "display_name",
        "id",
        "is_featured",
        "name",
        "latest_build",
        "user_count",
    )

    def __init__(self, data):
        self.display_name: Optional[str] = data["display_name"]
        self.id: int = data["id"]
        self.is_featured: bool = data["is_featured"]
        self.name: str = data["name"]
        self.latest_build: Optional[Build] = get_optional(data, "latest_build", Build)
        self.user_count: Optional[int] = data.get("user_count")

    def __repr__(self):
        return prettify(self, "name")


class ChangelogEntry:
    """
    **Attributes**

    category: :class:`str`

    created_at: Optional[:class:`datetime.datetime`]

    github_pull_request_id: Optional[:class:`int`]

    github_url: Optional[:class:`str`]

    id: Optional[:class:`int`]

    major: :class:`bool`

    repository: Optional[:class:`str`]

    title: Optional[:class:`str`]

    type: :class:`str`

    url: Optional[:class:`str`]

    github_user: Optional[:class:`GithubUser`]
        If the changelog entry has no GitHub user, a placeholder is generated.

    message: Optional[:class:`str`]
        Entry message in Markdown format. Embedded HTML is allowed.

    message_html: Optional[:class:`str`]
        Entry message in HTML format.
    """

    __slots__ = (
        "category",
        "created_at",
        "github_pull_request_id",
        "github_url",
        "id",
        "major",
        "repository",
        "title",
        "type",
        "url",
        "github_user",
        "message",
        "message_html",
    )

    def __init__(self, data):
        self.category: str = data["category"]
        self.created_at: Optional[datetime] = get_optional(data, "created_at", parser.parse)
        self.github_pull_request_id: Optional[int] = data["github_pull_request_id"]
        self.github_url: Optional[str] = data["github_url"]
        self.id: Optional[int] = data["id"]
        self.major: bool = data["major"]
        self.repository: Optional[str] = data["repository"]
        self.title: Optional[str] = data["title"]
        self.type: str = data["type"]
        self.url: Optional[str] = data["url"]

        self.github_user: Optional[GithubUser] = get_optional(data, "github_user", GithubUser)
        self.message: Optional[str] = data.get("message")
        self.message_html: Optional[str] = data.get("message_html")

    def __repr__(self):
        return prettify(self, "title", "major", "created_at")


class GithubUser:
    """
    **Attributes**

    display_name: :class:`str`

    github_url: Optional[:class:`str`]

    id: Optional[:class:`int`]

    osu_username: Optional[:class:`str`]

    user_id: Optional[:class:`int`]

    user_url: Optional[:class:`str`]
    """

    __slots__ = (
        "display_name",
        "github_url",
        "id",
        "osu_username",
        "user_id",
        "user_url",
    )

    def __init__(self, data):
        self.display_name: str = data["display_name"]
        self.github_url: Optional[str] = data["github_url"]
        self.id: Optional[int] = data["id"]
        self.osu_username: Optional[str] = data["osu_username"]
        self.user_id: Optional[int] = data["user_id"]
        self.user_url: Optional[str] = data["user_url"]

    def __repr__(self):
        return prettify(self, "display_name")
