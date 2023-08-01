from dateutil import parser
from typing import Optional, List, TYPE_CHECKING

from ..util import prettify, get_optional
from ..enums import CommentSort
from .user import UserCompact
from .current_user_attributes import CommentableMetaAttributes


if TYPE_CHECKING:
    from datetime import datetime


class Comment:
    """
    Represents a single comment.

    **Attributes**

    commentable_id: :class:`int`
        ID of the object the comment is attached to

    commentable_type: :class:`str`
        type of object the comment is attached to

    created_at: :class:`datetime.datetime`

    deleted_at: Option[:class:`datetime.datetime`]

    deleted_by_id: Optional[:class:`int`]
        user id of the user that deleted the post; null, otherwise

    edited_at: Optional[:class:`datetime.datetime`]

    edited_by_id: Optional[:class:`int`]
        user id of the user that edited the post; null, otherwise

    id: :class:`int`
        the ID of the comment

    legacy_name: Optional[:class:`str`]
        username displayed on legacy comments

    message: Optional[:class:`str`]
        markdown of the comment's content

    message_html: Optional[:class:`str`]
        html version of the comment's content

    parent_id: Optional[:class:`int`]
        ID of the comment's parent

    pinned: :class:`bool`
        Pin status of the comment

    replies_count: :class:`int`
        number of replies to the comment

    updated_at: :class:`datetime.datetime`

    user: Optional[:class:`UserCompact`]

    user_id: :class:`int`
        user ID of the poster

    votes_count: :class:`int`
        number of votes

    url: :class:`str`
        URL to the comment
    """

    __slots__ = (
        "commentable_id",
        "commentable_type",
        "created_at",
        "deleted_at",
        "deleted_by_id",
        "edited_at",
        "edited_by_id",
        "id",
        "legacy_name",
        "message",
        "message_html",
        "parent_id",
        "pinned",
        "replies_count",
        "updated_at",
        "user",
        "user_id",
        "votes_count",
    )

    def __init__(self, data):
        self.commentable_id: int = data["commentable_id"]
        self.commentable_type: str = data["commentable_type"]
        self.created_at: datetime = parser.parse(data["created_at"])
        self.deleted_at: Optional[datetime] = get_optional(data, "deleted_at", parser.parse)
        self.deleted_by_id: Optional[int] = data.get("deleted_by_id")
        self.edited_at: Optional[datetime] = get_optional(data, "edited_at", parser.parse)
        self.edited_by_id: Optional[int] = data["edited_by_id"]
        self.id: int = data["id"]
        self.legacy_name: Optional[str] = data["legacy_name"]
        self.message: Optional[str] = data.get("message")
        self.message_html: Optional[str] = data.get("message_html")
        self.parent_id: Optional[int] = data["parent_id"]
        self.pinned: bool = data["pinned"]
        self.replies_count: int = data["replies_count"]
        self.updated_at: datetime = parser.parse(data["updated_at"])
        self.user: Optional[UserCompact] = get_optional(data, "user", UserCompact)
        self.user_id: int = data["user_id"]
        self.votes_count: int = data["votes_count"]

    @property
    def url(self) -> str:
        return f"https://osu.ppy.sh/comments/{self.id}"

    def __repr__(self):
        return prettify(self, "user_id", "message")


class CommentBundle:
    """
    Comments and related data.

    **Attributes**

    commentable_meta: List[:class:`CommentableMeta`]
        ID of the object the comment is attached to

    comments: List[:class:`Comment`]
        List of comments ordered according to sort

    has_more: :class:`bool`
        If there are more comments or replies available

    has_more_id: :class:`int`

    included_comments: List[:class:`Comment`]
        Related comments; e.g. parent comments and nested replies

    pinned_comments: List[:class:`Comment`]
        Pinned comments

    sort: :class:`CommentSort`

    top_level_count: Optional[:class:`int`]
        Number of comments at the top level. Not returned for replies.

    total: Optional[:class:`int`]
        Total number of comments. Not returned for replies.

    user_follow: :class:`bool`
        is the current user watching the comment thread?

    user_votes: List[:class:`int`]
        IDs of the comments in the bundle the current user has upvoted

    users: List[:class:`UserCompact`]
        List of users related to the comments
    """

    __slots__ = (
        "commentable_meta",
        "comments",
        "has_more",
        "has_more_id",
        "included_comments",
        "pinned_comments",
        "sort",
        "top_level_count",
        "total",
        "user_follow",
        "user_votes",
        "users",
    )

    def __init__(self, data):
        self.commentable_meta: List[CommentableMeta] = list(map(CommentableMeta, data["commentable_meta"]))
        self.comments: List[Comment] = list(map(Comment, data["comments"]))
        self.has_more: bool = data["has_more"]
        self.has_more_id: int = data["has_more_id"]
        self.included_comments: List[Comment] = list(map(Comment, data["included_comments"]))
        self.pinned_comments: List[Comment] = list(map(Comment, data["pinned_comments"]))
        self.sort: CommentSort = CommentSort(data["sort"])
        self.top_level_count: Optional[int] = data.get("top_level_count")
        self.total: Optional[int] = data.get("total")
        self.user_follow: bool = data["user_follow"]
        self.user_votes: List[int] = data["user_votes"]
        self.users: List[UserCompact] = list(map(UserCompact, data["users"]))

    def __repr__(self):
        return prettify(self, "commentable_meta", "comments", "users")


class CommentableMeta:
    """
    Metadata of the object that a comment is attached to.
    If the object is deleted then title is the only attribute with a value.

    **Attributes**

    id: Optional[:class:`int`]
        the ID of the object

    owner_id: Optional[:class:`int`]
        the ID of the owner of the object

    owner_title: Optional[:class:`int`]
        undocumented

    title: Optional[:class:`str`]
        display title

    type: Optional[:class:`str`]
        the type of the object

    url: Optional[:class:`str`]
        url of the object

    current_user_attributes: :class:`CommentableMetaAttributes`
    """

    __slots__ = (
        "id",
        "title",
        "type",
        "url",
        "owner_id",
        "owner_title",
        "current_user_attributes",
    )

    def __init__(self, data):
        self.id: Optional[int] = data.get("id")
        self.owner_id: Optional[int] = data.get("owner_id")
        self.owner_title: Optional[str] = data.get("owner_title")
        self.title: str = data.get("title")
        self.type: Optional[str] = data.get("type")
        self.url: Optional[str] = data.get("url")
        self.current_user_attributes: Optional[CommentableMetaAttributes] = get_optional(
            data, "current_user_attributes", CommentableMetaAttributes
        )

    def __repr__(self):
        return prettify(self, "title", "url")
