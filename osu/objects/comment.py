from .user import UserCompact
from dateutil import parser

from ..util import prettify


class Comment:
    """
    Represents a single comment.

    **Attributes**

    commentable_id: :class:`int`
        ID of the object the comment is attached to

    commentable_type: :class:`str`
        type of object the comment is attached to

    created_at: :class:`datetime.datetime`
        ISO 8601 date

    deleted_at: :class:`datetime.datetime` or :class:`NoneType`
        ISO 8601 date if the comment was deleted; null, otherwise

    edited_at: :class:`datetime.datetime` or :class:`NoneType`
        ISO 8601 date if the comment was edited; null, otherwise

    edited_by_id: :class:`int` or :class:`NoneType`
        user id of the user that edited the post; null, otherwise

    id: :class:`int`
        the ID of the comment

    legacy_name: :class:`str` or :class:`NoneType`
        username displayed on legacy comments

    message: :class:`str` or :class:`NoneType`
        markdown of the comment's content

    message_html: :class:`str` or :class:`NoneType`
        html version of the comment's content

    parent_id: :class:`int` or :class:`NoneType`
        ID of the comment's parent

    pinned: :class:`bool`
        Pin status of the comment

    replies_count: :class:`int`
        number of replies to the comment

    updated_at: :class:`datetime.datetime`
        ISO 8601 date

    user_id: :class:`int`
        user ID of the poster

    votes_count: :class:`int`
        number of votes

    url: :class:`str`
        URL to the comment
    """
    __slots__ = (
        "commentable_id", "commentable_type", "created_at", "deleted_at", "edited_at", "edited_by_id",
        "id", "legacy_name", "message", "message_html", "parent_id", "pinned", "replies_count", "updated_at",
        "user_id", "votes_count"
    )

    def __init__(self, data):
        self.commentable_id = data['commentable_id']
        self.commentable_type = data['commentable_type']
        self.created_at = parser.parse(data['created_at'])
        self.deleted_at = parser.parse(data['deleted_at']) if data['deleted_at'] is not None else None
        self.edited_at = data['edited_at']
        self.edited_by_id = data['edited_by_id']
        self.id = data['id']
        self.legacy_name = data['legacy_name']
        self.message = data['message']
        self.message_html = data['message_html']
        self.parent_id = data['parent_id']
        self.pinned = data['pinned']
        self.replies_count = data['replies_count']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.votes_count = data['votes_count']

    @property
    def url(self):
        return f"https://osu.ppy.sh/comments/{self.id}"

    def __repr__(self):
        return prettify(self, 'message', 'user_id', 'created_at')


class CommentBundle:
    """
    Comments and related data.

    **Attributes**

    commentable_meta: Sequence[:class:`CommentableMeta`]
        ID of the object the comment is attached to

    comments: Sequence[:class:`Comment`]
        List of comments ordered according to sort

    cursor:	:class:`Cursor`
        To be used to query the next page

    has_more: :class:`bool`
        If there are more comments or replies available

    has_more_id: :class:`id` or :class:`NoneType`

    included_comments: Sequence[:class:`Comment`]
        Related comments; e.g. parent comments and nested replies

    pinned_comments: Sequence[:class:`Comment`] or :class:`NoneType`
        Pinned comments

    sort: :class:`str`
        one of the following:
            new (created_at (descending), id (descending))
            old (created_at (ascending), id (ascending))
            top (votes_count (descending), created_at (descending), id (descending))

    top_level_count: :class:`int` or :class:`NoneType`
        Number of comments at the top level. Not returned for replies.

    total: :class:`int` or :class:`NoneType`
        Total number of comments. Not retuned for replies.

    user_follow: :class:`bool`
        is the current user watching the comment thread?

    user_votes: Sequence[:class:`int`]
        IDs of the comments in the bundle the current user has upvoted

    users: Sequence[:class:`UserCompact`]
        list containing objects of type :class:`UserCompact`. list of users related to the comments
    """
    __slots__ = (
        "commentable_meta", "comments", "cursor", "has_more", "has_more_id", "included_comments",
        "pinned_comments", "sort", "top_level_count", "total", "user_follow", "user_votes", "users"
    )

    def __init__(self, data):
        self.commentable_meta = list(map(CommentableMeta, data['commentable_meta']))
        self.comments = list(map(Comment, data['comments']))
        self.cursor = data['cursor']
        self.has_more = data['has_more']
        self.has_more_id = data['has_more_id']
        self.included_comments = list(map(Comment, data['included_comments']))
        self.pinned_comments = list(map(Comment, data['pinned_comments'])) \
            if data.get('pinned_comments') is not None else None
        self.sort = data['sort']
        self.top_level_count = data['top_level_count']
        self.total = data['total']
        self.user_follow = data['user_follow']
        self.user_votes = data['user_votes']
        self.users = list(map(UserCompact, data['users']))

    def __repr__(self):
        return prettify(self, 'commentable_meta', 'comments', 'users')


class CommentableMeta:
    """
    Metadata of the object that a comment is attached to.
    Not all attributes are guaranteed to have a value, for example
    if the comment is delete.

    **Attributes**

    id: :class:`int`
        the ID of the object

    title: :class:`str`
        display title

    type: :class:`str`
        the type of the object

    url: :class:`str`
        url of the object

    owner_id: :class:`int`:
        the ID of the owner of the object

    owner_title: :class:`int`
        undocumented
    """
    __slots__ = (
        "id", "title", "type", "url", "owner_id", "owner_title"
    )

    def __init__(self, data):
        self.id = data.get('id')
        self.title = data.get('title')
        self.type = data.get('type')
        self.url = data.get('url')

    def __repr__(self):
        return prettify(self, 'title', 'url')
