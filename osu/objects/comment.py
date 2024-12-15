from typing import Optional, List, TYPE_CHECKING

from ..util import prettify, get_optional, get_required, fromisoformat
from ..enums import CommentSort
from .user import UserCompact
from .current_user_attributes import CommentableMetaAttributes


if TYPE_CHECKING:
    from datetime import datetime


__all__ = ("Comment", "CommentBundle", "CommentableMeta")


class Comment:
    """
    Represents a single comment.

    **Attributes**

    commentable_id: int
        ID of the object the comment is attached to

    commentable_type: str
        type of object the comment is attached to

    created_at: :py:class:`datetime.datetime`

    deleted_at: Option[:py:class:`datetime.datetime`]

    deleted_by_id: Optional[int]
        user id of the user that deleted the post; null, otherwise

    edited_at: Optional[:py:class:`datetime.datetime`]

    edited_by_id: Optional[int]
        user id of the user that edited the post; null, otherwise

    id: int
        the ID of the comment

    legacy_name: Optional[str]
        username displayed on legacy comments

    message: Optional[str]
        markdown of the comment's content

    message_html: Optional[str]
        html version of the comment's content

    parent_id: Optional[int]
        ID of the comment's parent

    pinned: bool
        Pin status of the comment

    replies_count: int
        number of replies to the comment

    updated_at: :py:class:`datetime.datetime`

    user: Optional[:class:`UserCompact`]

    user_id: int
        user ID of the poster

    votes_count: int
        number of votes

    url: str
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
        self.commentable_id: int = get_required(data, "commentable_id")
        self.commentable_type: str = get_required(data, "commentable_type")
        self.created_at: datetime = fromisoformat(get_required(data, "created_at"))
        self.deleted_at: Optional[datetime] = get_optional(data, "deleted_at", fromisoformat)
        self.deleted_by_id: Optional[int] = data.get("deleted_by_id")
        self.edited_at: Optional[datetime] = get_optional(data, "edited_at", fromisoformat)
        self.edited_by_id: Optional[int] = get_required(data, "edited_by_id")
        self.id: int = get_required(data, "id")
        self.legacy_name: Optional[str] = get_required(data, "legacy_name")
        self.message: Optional[str] = data.get("message")
        self.message_html: Optional[str] = data.get("message_html")
        self.parent_id: Optional[int] = get_required(data, "parent_id")
        self.pinned: bool = get_required(data, "pinned")
        self.replies_count: int = get_required(data, "replies_count")
        self.updated_at: datetime = fromisoformat(get_required(data, "updated_at"))
        self.user: Optional[UserCompact] = get_optional(data, "user", UserCompact)
        self.user_id: int = get_required(data, "user_id")
        self.votes_count: int = get_required(data, "votes_count")

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

    has_more: bool
        If there are more comments or replies available

    has_more_id: int

    included_comments: List[:class:`Comment`]
        Related comments; e.g. parent comments and nested replies

    pinned_comments: List[:class:`Comment`]
        Pinned comments

    sort: :class:`CommentSort`

    cursor: :class:`dict`

    top_level_count: Optional[int]
        Number of comments at the top level. Not returned for replies.

    total: Optional[int]
        Total number of comments. Not returned for replies.

    user_follow: bool
        is the current user watching the comment thread?

    user_votes: List[int]
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
        "cursor",
        "top_level_count",
        "total",
        "user_follow",
        "user_votes",
        "users",
    )

    def __init__(self, data):
        self.commentable_meta: List[CommentableMeta] = list(
            map(CommentableMeta, get_required(data, "commentable_meta"))
        )
        self.comments: List[Comment] = list(map(Comment, get_required(data, "comments")))
        self.has_more: bool = get_required(data, "has_more")
        self.has_more_id: int = get_required(data, "has_more_id")
        self.included_comments: List[Comment] = list(map(Comment, get_required(data, "included_comments")))
        self.pinned_comments: List[Comment] = list(map(Comment, get_required(data, "pinned_comments")))
        self.sort: CommentSort = CommentSort(get_required(data, "sort"))
        self.cursor: dict = get_required(data, "cursor")
        self.top_level_count: Optional[int] = data.get("top_level_count")
        self.total: Optional[int] = data.get("total")
        self.user_follow: bool = get_required(data, "user_follow")
        self.user_votes: List[int] = get_required(data, "user_votes")
        self.users: List[UserCompact] = list(map(UserCompact, get_required(data, "users")))

    def __repr__(self):
        return prettify(self, "commentable_meta", "comments", "users")


class CommentableMeta:
    """
    Metadata of the object that a comment is attached to.
    If the object is deleted then title is the only attribute with a value.

    **Attributes**

    id: Optional[int]
        the ID of the object

    owner_id: Optional[int]
        the ID of the owner of the object

    owner_title: Optional[int]
        undocumented

    title: Optional[str]
        display title

    type: Optional[str]
        the type of the object

    url: Optional[str]
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
