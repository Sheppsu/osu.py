from .user import UserCompact


class Comment:
    """
    Represents a single comment.

    **Attributes**

    commentable_id: :class:`int`
        ID of the object the comment is attached to

    commentable_type: :class:`str`
        type of object the comment is attached to

    created_at: :ref:`Timestamp`
        ISO 8601 date

    deleted_at: :ref:`Timestamp`
        ISO 8601 date if the comment was deleted; null, otherwise

    edited_at: :ref:`Timestamp`
        ISO 8601 date if the comment was edited; null, otherwise

    edited_by_id: :class:`int`
        user id of the user that edited the post; null, otherwise

    id: :class:`int`
        the ID of the comment

    legacy_name: :class:`str`
        username displayed on legacy comments

    message: :class:`str`
        markdown of the comment's content

    message_html: :class:`str`
        html version of the comment's content

    parent_id: :class:`int`
        ID of the comment's parent

    pinned: :class:`bool`
        Pin status of the comment

    replies_count: :class:`int`
        number of replies to the comment

    updated_at: :ref:`Timestamp`
        ISO 8601 date

    user_id: :class:`int`
        user ID of the poster

    votes_count: :class:`int`
        number of votes
    """
    __slots__ = (
        "commentable_id", "commentable_type", "created_at", "deleted_at", "edited_at", "edited_by_id",
        "id", "legacy_name", "message", "message_html", "parent_id", "pinned", "replies_count", "updated_at",
        "user_id", "votes_count"
    )

    def __init__(self, data):
        self.commentable_id = data['commentable_id']
        self.commentable_type = data['commentable_type']
        self.created_at = data['created_at']
        self.deleted_at = data['deleted_at']
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


class CommentBundle:
    """
    Comments and related data.

    **Attributes**

    commentable_meta: :class:`list`
        list containing objects of type :class:`CommentableMeta`. ID of the object the comment is attached to

    comments: :class:`list`
        list containing objects of type :class:`Comment`. List of comments ordered according to sort

    cursor:	:class:`dict`
        To be used to query the next page

    has_more: :class:`bool`
        If there are more comments or replies available

    has_more_id: :class:`id`

    included_comments: :class:`list`
        list containing objects of type :class:`Comment`. Related comments; e.g. parent comments and nested replies

    pinned_comments: :class:`list`
        list containing objects of type :class:`Comment`. Pinned comments

    sort: :class:`str`
        one of the following:
            new (created_at (descending), id (descending))
            old (created_at (ascending), id (ascending))
            top (votes_count (descending), created_at (descending), id (descending))

    top_level_count: :class:`int`
        Number of comments at the top level. Not returned for replies.

    total: :class:`int`
        Total number of comments. Not retuned for replies.

    user_follow: :class:`bool`
        is the current user watching the comment thread?

    user_votes: :class:`list`
        list containing objects of type :class:`int`.IDs of the comments in the bundle the current user has upvoted

    users: :class:`list`
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
        self.pinned_comments = list(map(Comment, data['pinned_comments']))
        self.sort = data['sort']
        self.top_level_count = data['top_level_count']
        self.total = data['total']
        self.user_follow = data['user_follow']
        self.user_votes = data['user_votes']
        self.users = list(map(UserCompact, data['users']))


class CommentableMeta:
    """
    Metadata of the object that a comment is attached to.

    **Attributes**

    id: :class:`int`
        the ID of the object

    title: :class:`str`
        display title

    type: :class:`str`
        the type of the object

    url: :class:`str`
        url of the object
    """
    __slots__ = (
        "id", "title", "type", "url"
    )

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.type = data['type']
        self.url = data['url']
