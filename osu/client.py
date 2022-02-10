from .http import HTTPHandler
from .objects import *
from .auth import AuthHandler


class Client:
    """
    Main object for interacting with osu!api

    **Init Parameters**

    auth: :class:`AuthHandler`
        The AuthHandler object passed in when initiating the Client object

    limit_per_second: :class:`float`
        This defines the amount of time that should pass before you can make another request. Peppy has requested that
        only 60 requests per minute maximum be made to the api. If you lower the limit, please be
        knowledgeable of the Terms of Use and be careful about making too many requests. The Terms of Use are
        stated in the osu!api v2 documentation as follows:

        Use the API for good. Don't overdo it. If in doubt, ask before (ab)using :). this section may expand as necessary.

        Current rate limit is set at an insanely high 1200 requests per minute, with burst capability of up to 200 beyond that.
        If you require more, you probably fall into the above category of abuse. If you are doing more than 60 requests a minute,
        you should probably give peppy a yell.
    """
    def __init__(self, auth, limit_per_second=1):
        self.auth = auth
        self.http = HTTPHandler(auth, self, limit_per_second)

    @classmethod
    def from_client_credentials(cls, client_id: int, client_secret: str, redirect_url: str, scope: Scope = Scope.default(), last_session_code=None, limit_per_second=1):
        auth = AuthHandler(client_id, client_secret, redirect_url, scope)
        auth.get_auth_token(last_session_code)
        return cls(auth, limit_per_second)

    def lookup_beatmap(self, checksum=None, filename=None, id=None):
        """
        Returns beatmap.

        Requires OAuth and scope public

        **Parameters**

        checksum(optional): :class:`str`
            A beatmap checksum.

        filename(optional): :class:`str`
            A filename to lookup

        id(optional): :class:`int`
            A beatmap ID to lookup

        **Returns**

        :class:`Beatmap`
        """
        return Beatmap(self.http.get(Path.beatmap_lookup(), checksum=checksum, filename=filename, id=id))

    def get_user_beatmap_score(self, beatmap, user, mode=None, mods=None):
        """
        Returns a :class:`User`'s score on a Beatmap

        Requires OAuth and scope public

        **Parameters**

        beatmap: :class:`int`
            Id of the beatmap

        user: :class:`int`
            Id of the user

        mode(optional): :class:`str`
            The GameMode to get scores for

        mods(optional): :class:`array`
            An array of matching Mods, or none

        **Returns**

        :class:`BeatmapUserScore`
        """
        return BeatmapUserScore(self.http.get(Path.user_beatmap_score(beatmap, user), mode=mode, mods=mods))

    def get_beatmap_scores(self, beatmap, mode=None, mods=None, type=None):
        """
        Returns the top scores for a beatmap

        Requires OAuth and scope public

        **Parameters**

        beatmap: :class:`int`
            Id of the beatmap

        mode(optional): :class:`str`
            The GameMode to get scores for

        mods(optional): :class:`array`
            An array of matching Mods, or none

        type(optional): :class:`str`
            Beatmap score ranking type

        **Returns**

        :class:`BeatmapScores`
        """
        return BeatmapScores(self.http.get(Path.beatmap_scores(beatmap), mode=mode, mods=mods, type=type))

    def get_beatmap(self, beatmap):
        """
        Gets beatmap data for the specified beatmap ID.

        Requires OAuth and scope public

        **Parameters**

        beatmap: :class:`int`
            The ID of the beatmap

        **Returns**

        :class:`Beatmap`
            Includes attributes beatmapset, failtimes, and max_combo
        """
        return Beatmap(self.http.get(Path.beatmap(beatmap)))

    def get_beatmapset_discussion_posts(self, beatmapset_discussion_id=None, limit=None, page=None, sort=None, user=None, with_deleted=None):
        """
        Returns the posts of the beatmapset discussions

        Requires OAuth and scope public

        **Parameters**

        beatmapset_discussion_id: :class:`id`
            id of the BeatmapsetDiscussion

        limit: :class:`id`
            Maximum number of results

        page: :class:`int`
            Search results page.

        sort: :class:`str`
            id_desc for newest first; id_asc for oldest first. Defaults to id_desc

        user: :class:`int`
            The id of the User

        with_deleted
            The param has no effect as api calls do not currently receive group permissions

        **Returns**

        :class:`dict`
            {
            beatmapsets: :class:`BeatmapsetCompact`,

            cursor: :class:`dict`,

            posts: [ :class:`BeatmapsetDiscussionPost`, ...],

            users: :class:`UserCompact`
            }
        """
        # TODO: Change is supposed to occur on the response given back from the server, make sure to change it when that happens.
        resp = self.http.get(Path.beatmapset_discussion_posts(), beatmapset_discussion_id=beatmapset_discussion_id,
                             limit=limit, page=page, sort=sort, user=user, with_deleted=with_deleted)
        return {
            'beatmapsets': BeatmapsetCompact(resp['beatmapsets']),
            'cursor': resp['cursor'],
            'posts': [BeatmapsetDiscussionPost(post) for post in resp['posts']],
            'users': UserCompact(resp['users'])
        }

    def get_beatmapset_discussion_votes(self, beatmapset_discussion_id=None, limit=None, page=None, receiver=None, score=None, sort=None, user=None, with_deleted=None):
        """
        Returns the votes given to beatmapset discussions

        Requires OAuth and scope public

        **Parameters**

        beatmapset_discussion_id: :class:`id`
            id of the BeatmapsetDiscussion

        limit: :class:`id`
            Maximum number of results

        page: :class:`int`
            Search results page.

        receiver: :class:`int`
            The id of the User receiving the votes.

        score: :class:`int`
            1 for upvote, -1 for downvote

        sort: :class:`str`
            id_desc for newest first; id_asc for oldest first. Defaults to id_desc

        user: :class:`int`
            The id of the User giving the votes.

        with_deleted
            The param has no effect as api calls do not currently receive group permissions

        **Returns**

        :class:`dict`
            {
            cursor: :class:`dict`,

            discussions: :class:`BeatmapsetDiscussions`,

            users: :class:`UserCompact`,

            votes: [ :class:`BeatmapsetDiscussionVote`, ...]
            }
        """
        # TODO: Change is supposed to occur on the response given back from the server, make sure to change it when that happens.
        resp = self.http.get(Path.beatmapset_discussion_votes(), beatmapset_discussion_id=beatmapset_discussion_id,
                             limit=limit, receiver=receiver, score=score, page=page, sort=sort, user=user, with_deleted=with_deleted)
        return {
            'cursor': resp['cursor'],
            'discussions': BeatmapsetDiscussion(resp['discussions']),
            'users': UserCompact(resp['users']),
            'votes': [BeatmapsetDiscussionVote(vote) for vote in resp['votes']]
        }

    def get_beatmapset_discussions(self, beatmap_id=None, beatmapset_id=None, beatmapset_status=None, limit=None, message_type=None, only_unresolved=None, page=None, sort=None, user=None, with_deleted=None):
        """
        Returns a list of beatmapset discussions

        Requires OAuth and scope public

        **Parameters**

        beatmap_id: :class:`int`
            id of the Beatmap

        beatmapset_id: :class:`int`
            id of the Beatmapset

        beatmapset_status: :class:`str`
            One of all, ranked, qualified, disqualified, never_qualified. Defaults to all.

        limit: :class:`int`
            Maximum number of results.

        message_types[]: :class:`str`
            suggestion, problem, mapper_note, praise, hype, review. Blank defaults to all types.

        only_unresolved: :class:`bool`
            true to show only unresolved issues; false, otherwise. Defaults to false.

        page: :class:`int`
            Search result page.

        sort: :class:`str`
            id_desc for newest first; id_asc for oldest first. Defaults to id_desc.

        user: :class:`int`
            The id of the User.

        with_deleted
            This param has no effect as api calls do not currently receive group permissions.

        **Returns**

        :class:`dict`
            {
            beatmaps: [ :class:`Beatmap`, ...],
                List of beatmaps associated with the discussions returned.

            cursor: :class:`dict`,

            discussions: [ :class:`BeatmapsetDiscussion`, ...],
                List of discussions according to sort order.

            included_discussions: [ :class:`BeatmapsetDiscussion`, ...],
                Additional discussions related to discussions.

            reviews_config.max_blocks: :class:`int`
                Maximum number of blocks allowed in a review.

            users: [ :class:`UserCompact`, ...]
                List of users associated with the discussions returned.
            }
        """
        # TODO: Change is supposed to occur on the response given back from the server, make sure to change it when that happens.
        resp = self.http.get(Path.beatmapset_discussions(), beatmap_id=beatmap_id, beatmapset_id=beatmapset_id,
                             beatmapset_status=beatmapset_status, limit=limit, message_type=message_type,
                             only_unresolved=only_unresolved, page=page, sort=sort, user=user, with_deleted=with_deleted)
        return {
            'beatmaps': [Beatmap(beatmap) for beatmap in resp['beatmaps']],
            'cursor': resp['cursor'],
            'discussions': [BeatmapsetDiscussion(disc) for disc in resp['discussions']],
            'included_discussions': [BeatmapsetDiscussion(disc) for disc in resp['included_discussions']],
            'reviews_config.max_blocks': resp['reviews_config'],
            'users': [UserCompact(user) for user in resp['users']]
        }

    def create_new_pm(self, target_id, message, is_action):
        """
        This endpoint allows you to create a new PM channel.

        Requires OAuth and scope chat.write

        **Parameters**

        target_id: :class:`int`
            user_id of user to start PM with

        message: :class:`str`
            message to send

        is_action: :class:`bool`
            whether the message is an action

        **Returns**

        :class:`dict`
            {
            new_channel_id: :class:`int`
                channel_id of newly created ChatChannel

            presence: [ :class:`ChatChannel`, ...]
                array of ChatChannel

            message: :class:`ChatMessage`
                the sent ChatMessage

            }
        """
        data = {'target_id': target_id, 'message': message, 'is_action': is_action}
        resp = self.http.post(Path.create_new_pm(), data=data)
        return {
            'new_channel_id': resp['new_channel_id'],
            'presence': [ChatChannel(channel) for channel in resp['presence']],
            'message': ChatMessage(resp['message'])
        }

    def get_updates(self, since, channel_id=None, limit=None):
        """
        This endpoint returns new messages since the given message_id along with updated channel 'presence' data.

        Requires OAuth and scope lazer

        **Parameters**

        since: :class:`int`
            The message_id of the last message to retrieve messages since

        channel_id: :class:`int`
            If provided, will only return messages for the given channel

        limit: :class:`int`
            number of messages to return (max of 50)

        **Returns**

        :class:`dict`
            {
            presence: [ :class:`ChatChannel`, ...],

            messages: [ :class:`ChatMessage`, ...]

            }
        """
        resp = self.http.post(Path.get_updates(), since=since, channel_id=channel_id, limit=limit)
        return {
            'presence': [ChatChannel(channel) for channel in resp['presence']],
            'messages': [ChatMessage(msg) for msg in resp['messages']],
            'silences': [UserSilence(silence) for silence in resp['silences']]
        }

    def get_channel_messages(self, channel_id, limit=None, since=None, until=None):
        """
        This endpoint returns the chat messages for a specific channel.

        Requires OAuth and scope lazer

        **Parameter**

        channel_id: :class:`int`
            The ID of the channel to retrieve messages for

        limit: :class:`int`
            number of messages to return (max of 50)

        since: :class:`int`
            messages after the specified message id will be returned

        until: :class:`int`
            messages up to but not including the specified message id will be returned

        **Returns**

        :class:`list`
            list containing objects of type :class:`ChatMessage`
        """
        return [ChatMessage(msg) for msg in self.http.post(Path.get_channel_messages(channel_id), limit=limit, since=since, until=until)]

    def send_message_to_channel(self, channel_id, message, is_action):
        """
        This endpoint returns the chat messages for a specific channel.

        Requires OAuth and scope lazer

        **Parameters**

        message: :class:`str`
            message to send

        is_action: :class:`bool`
            whether the message is an action

        channel_id: :class:`int`
            The channel_id of the channel to send message to

        **Returns**

        :class:`ChatMessage`
        """
        data = {'message': message, 'is_action': is_action}
        return ChatMessage(self.http.post(Path.send_message_to_channel(channel_id), data=data))

    def join_channel(self, channel, user):
        """
        This endpoint allows you to join a public channel.

        Requires OAuth and scope lazer

        **Parameters**

        channel: :class:`int`

        user: :class:`int`

        **Returns**

        :class:`ChatChannel`
        """
        return ChatChannel(self.http.put(Path.join_channel(channel, user)))

    def leave_channel(self, channel, user):
        """
        This endpoint allows you to leave a public channel.

        Requires OAuth and scope lazer

        **Parameters**

        channel: :class:`int`

        user: :class:`int`
        """
        self.http.delete(Path.leave_channel(channel, user))

    def mark_channel_as_read(self, channel, message, channel_id, message_id):
        """
        This endpoint marks the channel as having being read up to the given message_id.

        Requires OAuth and scope lazer

        **Parameters**

        channel_id: :class:`int`
            The channel_id of the channel to mark as read

        message_id: :class:`int`
            The message_id of the message to mark as read up to
        """
        self.http.put(Path.mark_channel_as_read(channel, message), channel_id=channel_id, message_id=message_id)

    def get_channel_list(self):
        """
        This endpoint returns a list of all joinable public channels.

        Requires OAuth and scope lazer

        **Returns**

        :class:`list`
            list containing objects of type :class:`ChatChannel`
        """
        return [ChatChannel(channel) for channel in self.http.get(Path.get_channel_list())]

    def create_channel(self, type, target_id=None):
        """
        This endpoint creates a new channel if doesn't exist and joins it. Currently only for rejoining existing PM channels which the user has left.

        Requires OAuth and scope lazer

        **Parameter**

        type: :class:`str`
            channel type (currently only supports "PM")

        target_id: :class:`int`
            target user id for type PM

        **Returns**

        :class:`ChatChannel`
             contains recent_messages attribute. Note that if there's no existing PM channel,
             most of the fields will be blank. In that case, send a message (create_new_pm) instead to create the channel.
        """
        data = {'type': type, 'target_id': target_id}
        return ChatChannel(self.http.post(Path.create_channel(), data=data))

    def get_channel(self, channel):
        """
        Gets details of a chat channel.

        Requires OAuth and scope lazer

        **Parameter**

        channel: :class:`int`

        **Returns**

        :class:`dict`
            {
            channel: :class:`ChatChannel`,

            users: :class:`UserCompact`

            }
        """
        resp = self.http.get(Path.get_channel(channel))
        return {
            'channel': ChatChannel(resp['channel']),
            'users': UserCompact(resp['users']),
        }

    def get_comments(self, commentable_type=None, commentable_id=None, cursor=None, parent_id=None, sort=None):
        """
        Returns a list comments and their replies up to 2 levels deep.

        Does not require OAuth

        **Parameter**

        commentable_type: :class:`str`
            The type of resource to get comments for.

        commentable_id: :class:`int`
            The id of the resource to get comments for.

        cursor: :class:`dict`
            Pagination option. See CommentSort for detail. The format follows Cursor except it's not currently included in the response.

        parent_id: :class:`int`
            Limit to comments which are reply to the specified id. Specify 0 to get top level comments.

        sort: :class:`str`
            Sort option as defined in CommentSort. Defaults to new for guests and user-specified default when authenticated.

        **Returns**

        :class:`CommentBundle`
            pinned_comments is only included when commentable_type and commentable_id are specified.
        """
        return CommentBundle(self.http.get(Path.get_comments(), commentable_type=commentable_type, commentable_id=commentable_id,
                                           **cursor if cursor else {}, parent_id=parent_id, sort=sort))

    def post_comment(self, commentable_id=None, commentable_type=None, message=None, parent_id=None):
        """
        Posts a new comment to a comment thread.

        Requires OAuth and scope lazer

        **Parameter**

        commentable_id: :class:`int`
            Resource ID the comment thread is attached to

        commentable_type: :class:`str`
            Resource type the comment thread is attached to

        message: :class:`str`
            Text of the comment

        parent_id: :class:`int`
            The id of the comment to reply to, null if not a reply

        **Returns**

        :class:`CommentBundle`
        """
        params = {
            'comment.commentable_id': commentable_id,
            'comment_commentable_type': commentable_type,
            'comment.message': message,
            'comment.parent_id': parent_id
        }
        return CommentBundle(self.http.post(Path.post_new_comment(), params=params))

    def get_comment(self, comment):
        """
        Gets a comment and its replies up to 2 levels deep.

        Does not require OAuth

        **Parameters**

        comment: :class:`int`
            Comment id

        **Returns**

        :class:`CommentBundle`
        """
        return CommentBundle(self.http.get(Path.get_comment(comment)))

    def edit_comment(self, comment, message=None):
        """
        Edit an existing comment.

        Requires OAuth and scope lazer

        **Parameters**

        comment: :class:`int`
            Comment id

        message: :class:`str`
            New text of the comment

        **Returns**

        :class:`CommentBundle`
        """
        params = {'comment.message': message}
        return CommentBundle(self.http.patch(Path.edit_comment(comment), params=params))

    def delete_comment(self, comment):
        """
        Deletes the specified comment.

        Requires OAuth and scope lazer

        **Parameters**

        comment: :class:`int`
            Comment id

        **Returns**

        :class:`CommentBundle`
        """
        return CommentBundle(self.http.delete(Path.delete_comment(comment)))

    def add_comment_vote(self, comment):
        """
        Upvotes a comment.

        Requires OAuth and scope lazer

        **Parameters**

        comment: :class:`int`
            Comment id

        **Returns**

        :class:`CommentBundle`
        """
        return CommentBundle(self.http.post(Path.add_comment_vote(comment)))

    def remove_comment_vote(self, comment):
        """
        Un-upvotes a comment.

        Requires OAuth and scope lazer

        **Parameters**

        comment: :class:`int`
            Comment id

        **Returns**

        :class:`CommentBundle`
        """
        return CommentBundle(self.http.delete(Path.remove_comment_vote(comment)))

    def reply_topic(self, topic, body):
        """
        Create a post replying to the specified topic.

        Requires OAuth and scope forum.write

        **Parameters**

        topic: :class:`int`
            Id of the topic to be replied to.

        body: :class:`str`
            Content of the reply post.

        **Returns**

        :class:`ForumPost`
            body attributes included
        """
        data = {'body': body}
        return ForumPost(self.http.post(Path.reply_topic(topic), data=data))

    def create_topic(self, body, forum_id, title, with_poll=None, hide_results=None, length_days=None, max_options=None, poll_options=None, poll_title=None, vote_change=None):
        """
        Create a new topic.

        Requires OAuth and scope forum.write

        **Parameters**

        body: :class:`str`
            Content of the topic.

        forum_id: :class:`int`
            Forum to create the topic in.

        title: :class:`str`
            Title of the topic.

        with_poll: :class:`bool`
            Enable this to also create poll in the topic (default: false).

        hide_results: :class:`bool`
            Enable this to hide result until voting period ends (default: false).

        length_days: :class:`int`
            Number of days for voting period. 0 means the voting will never ends (default: 0). This parameter is required if hide_results option is enabled.

        max_options: :class:`int`
            Maximum number of votes each user can cast (default: 1).

        poll_options: :class:`str`
            Newline-separated list of voting options. BBCode is supported.

        poll_title: :class:`str`
            Title of the poll.

        vote_change: :class:`bool`
            Enable this to allow user to change their votes (default: false).

        **Returns**

        :class:`dict`
            {
            topic: :class:`ForumTopic`

            post: :class:`ForumPost`
                includes body

            }
        """
        data = {'body': body, 'forum_id': forum_id, 'title': title, 'with_poll': with_poll}
        if with_poll:
            if poll_options is None or poll_title is None:
                raise TypeError("poll_options and poll_title are required since the topic has a poll.")
            data.update({'forum_topic_poll': {
                'hide_results': hide_results,'length_days': length_days,
                'max_options': max_options, 'poll_options': poll_options,
                'poll_title': poll_title, 'vote_change': vote_change
            }})
        resp = self.http.post(Path.create_topic(), data=data)
        return {
            'topic': ForumTopic(resp['topic']),
            'post': ForumPost(resp['post'])
        }

    def get_topic_and_posts(self, topic, cursor=None, sort=None, limit=None, start=None, end=None):
        """
        Get topic and its posts.

        Requires OAuth and scope public

        **Parameters**

        topic: :class:`int`
            Id of the topic.

        cursor: :class:`Cursor`
            To be used to fetch the next page of results

        sort: :class:`str`
            Post sorting option. Valid values are id_asc (default) and id_desc.

        limit: :class:`int`
            Maximum number of posts to be returned (20 default, 50 at most).

        start: :class:`int`
            First post id to be returned with sort set to id_asc. This parameter is ignored if cursor is specified.

        end: :class:`int`
            First post id to be returned with sort set to id_desc. This parameter is ignored if cursor is specified.

        **Returns**

        :class:`dict`
            {
            cursor: :class:`dict`,

            search: :class:`dict`,

            posts: [ :class:`ForumPost`, ...],

            topic: :class:`ForumTopic`

            }
        """
        resp = self.http.get(Path.get_topic_and_posts(topic), **cursor if cursor else {}, sort=sort, limit=limit, start=start, end=end)
        return {
            'cursor': resp['cursor'],
            'search': resp['search'],
            'posts': [ForumPost(post) for post in resp['posts']],
            'topic': ForumTopic(resp['topic'])
        }

    def edit_topic(self, topic, topic_title):
        """
        Edit topic. Only title can be edited through this endpoint.

        Requires OAuth and scope forum.write

        **Parameters**

        topic: :class:`int`
            Id of the topic.

        topic_title: :class:`str`
            New topic title.

        **Returns**

        :class:`ForumTopic`
        """
        data = {'forum_topic': {'topic_title': topic_title}}
        return ForumTopic(self.http.patch(Path.edit_topic(topic), data=data))

    def edit_post(self, post, body):
        """
        Edit specified forum post.

        Requires OAuth and scope forum.write

        post: :class:`int`
            Id of the post.

        body: :class:`str`
            New post content in BBCode format.

        **Returns**

        :class:`ForumPost`
        """
        data = {'body': body}
        return ForumPost(self.http.patch(Path.edit_post(post), data=data))

    def search(self, mode=None, query=None, page=None):
        """
        Searches users and wiki pages.

        Requires OAuth and scope public

        **Parameters**

        mode: :class:`str`
            Either all, user, or wiki_page. Default is all.

        query: :class:`str`
            Search keyword.

        page: :class:`int`
            Search result page. Ignored for mode all.

        **Returns**

        :class:`dict`
            {
            user: :class:`dict`
                For all or user mode. Only first 100 results are accessible
                {
                results: :class:`list`

                total: :class:`int`
                }

            wiki_page: :class:`dict`
                For all or wiki_page mode
                {
                results: :class:`list`

                total: :class:`int`
                }

            }
        """
        resp = self.http.get(Path.search(), mode=mode, query=query, page=page)
        return {
            'user': {'results': resp['user']['data'], 'total': resp['user']['total']} if mode is None or mode == 'all' or mode == 'user' else None,
            'wiki_page': {'results': resp['wiki_page']['data'], 'total': resp['wiki_page']['total']} if mode is None or mode == 'all' or mode == 'wiki_page' else None
        }

    def get_user_highscore(self, room, playlist, user):
        """
        Requires OAuth and scope lazer

        **Parameters**

        room: :class:`int`
            Id of the room.

        playlist: :class:`int`
            Id of the playlist item.

        user: :class:`int`
            User id.

        **Returns**

        Return type is undocumented
        """
        # Doesn't say response type
        return self.http.get(Path.get_user_high_score(room, playlist, user))

    def get_scores(self, room, playlist, limit=None, sort=None, cursor=None):
        """
        Requires OAuth and scope public

        **Parameters**

        room: :class:`int`
            Id of the room.

        playlist: :class:`int`
            Id of the playlist item.

        limit: :class:`int`
            Number of scores to be returned.

        sort: :class:`str`
            MultiplayerScoresSort parameter.

        cursor: :class:`dict`

        **Returns**

        Return type is undocumented
        """
        # Doesn't say response type
        return self.http.get(Path.get_scores(room, playlist), limit=limit, sort=sort, **cursor if cursor else {})

    def get_score(self, room, playlist, score):
        """
        Requires OAuth and scope lazer

        **Parameters**

        room: :class:`int`
            Id of the room.

        playlist: :class:`int`
            Id of the playlist item.

        score: :class:`int`
            Id of the score.

        **Returns**

        Return type is undocumented
        """
        # Doesn't say response type
        return self.http.get(Path.get_score(room, playlist, score))

    def get_notifications(self, max_id=None):
        """
        This endpoint returns a list of the user's unread notifications. Sorted descending by id with limit of 50.

        Requires OAuth and scope lazer

        **Parameters**

        max_id: :class:`int`
            Maximum id fetched. Can be used to load earlier notifications. Defaults to no limit (fetch latest notifications)

        **Returns**

        :class:`dict`
            {
            has_more: :class:`bool`,
                whether or not there are more notifications

            notifications: [ :class:`Notification`, ...],

            unread_count: :class:`bool`
                total unread notifications

            notification_endpoint: :class:`str`
                url to connect to websocket server

            }
        """
        resp = self.http.get(Path.get_notifications(), max_id=max_id)
        return {
            'has_more': resp['has_more'],
            'notifications': [Notification(notif) for notif in resp['notifications']],
            'unread_count': resp['unread_count'],
            'notification_endpoint': resp['notification_endpoint'],
        }

    def mark_notifications_read(self, ids):
        """
        This endpoint allows you to mark notifications read.

        Requires OAuth and scope lazer

        **Parameters**

        ids: :class:`list`
            list containing object of type :class:`int`. id of notifications to be marked as read.
        """
        data = {'ids': ids}
        self.http.post(Path.mark_notifications_as_read(), data=data)

    def revoke_current_token(self):
        """
        Requires OAuth
        """
        self.http.delete(self, Path.revoke_current_token())

    def get_ranking(self, mode, type, country=None, cursor=None, filter=None, spotlight=None, variant=None):
        """
        Gets the current ranking for the specified type and game mode.

        Requires OAuth and scope public

        mode: :class:`str`
            GameMode

        type: :class:`str`
            RankingType

        country: :class:`str`
            Filter ranking by country code. Only available for type of performance.

        cursor: :class:`dict`

        filter: :class:`str`
            Either all (default) or friends.

        spotlight: :class:`int`
            The id of the spotlight if type is charts. Ranking for latest spotlight will be returned if not specified.

        variant: :class:`str`
            Filter ranking to specified mode variant. For mode of mania, it's either 4k or 7k. Only available for type of performance.

        **Returns**

        :class:`Rankings`
        """
        return Rankings(self.http.get(Path.get_ranking(mode, type), country=country, **cursor if cursor else {}, filter=filter,
                                      spotlight=spotlight, variant=variant))

    def get_spotlights(self):
        """
        Gets the list of spotlights.

        Requires OAuth and scope public

        **Returns**

        :class:`Spotlights`
        """
        return Spotlights(self.http.get(Path.get_spotlights()))

    def get_own_data(self, mode=""):
        """
        Similar to get_user but with authenticated user (token owner) as user id.

        Requires OAuth and scope identify

        **Parameters**

        mode: :class:`str`
            GameMode. User default mode will be used if not specified.

        **Returns**

        See return for get_user
        """
        return User(self.http.get(Path.get_own_data(mode)))

    def get_user_kudosu(self, user, limit=None, offset=None):
        """
        Returns kudosu history.

        Requires OAuth and scope public

        **Parameters**

        user: :class:`int`
            Id of the user.

        limit: :class:`int`
            Maximum number of results.

        offset: :class:`int`
            Result offset for pagination.

        **Returns**

        :class:`list`
            list containing objects of type :class:`KudosuHistory`
        """
        return [KudosuHistory(kud) for kud in self.http.get(Path.get_user_kudosu(user), limit=limit, offset=offset)]

    def get_user_scores(self, user, type, include_fails=None, mode=None, limit=None, offset=None):
        """
        This endpoint returns the scores of specified user.

        Requires OAuth and scope public

        **Parameters**

        user: :class:`int`
            Id of the user.

        type: :class:`str`
            Score type. Must be one of these: best, firsts, recent

        include_fails: :class:`int`
            Only for recent scores, include scores of failed plays. Set to 1 to include them. Defaults to 0.

        mode: :class:`str`
            GameMode of the scores to be returned. Defaults to the specified user's mode.

        limit: :class:`int`
            Maximum number of results.

        offset: :class:`int`
            Result offset for pagination.

        **Returns**

        :class:`list`
            list obtaining objects of type :class:`Score`. Includes attributes

            beatmap, beatmapset, weight: Only for type best, user
        """
        return [Score(score) for score in self.http.get(Path.get_user_scores(user, type), include_fails=include_fails, mode=mode, limit=limit, offset=offset)]

    def get_user_beatmaps(self, user, type, limit=None, offset=None):
        """
        Returns the beatmaps of specified user.

        Requires OAuth and scope public

        **Parameters**

        user: :class:`int`
            Id of the user.

        type: :class:`str`
            Beatmap type. Can be one of the following - favourite, graveyard, loved, most_played, pending, ranked.

        limit: :class:`int`
            Maximum number of results.

        offset: :class:`int`
            Result offset for pagination.

        **Returns**

        :class:`list`
            list containing objects of type BeatmapPlaycount (for type most_played) or Beatmapset (any other type).
        """
        object_type = Beatmapset
        if type == 'most_played':
            object_type = BeatmapPlaycount
        return [object_type(bm) for bm in self.http.get(Path.get_user_beatmaps(user, type), limit=limit, offset=offset)]

    def get_user_recent_activity(self, user, limit=None, offset=None):
        """
        Returns recent activity.

        Requires OAuth and scope public

        **Parameters**

        user: :class:`int`
            Id of the user.

        limit: :class:`int`
            Maximum number of results.

        offset: :class:`int`
            Result offset for pagination.

        **Returns**

        :class:`list`
            list containing objects of type :class:`Event`
        """
        return [Event(event) for event in self.http.get(Path.get_user_recent_activity(user), limit=limit, offset=offset)]

    def get_user(self, user, mode='', key=None):
        """
        This endpoint returns the detail of specified user.

        Requires OAuth and scope public

        **Parameters**

        user: :class:`int`
            Id or username of the user. Id lookup is prioritised unless key parameter is specified.
            Previous usernames are also checked in some cases.

        mode: :class:`str`
            GameMode. User default mode will be used if not specified.

        key: :class:`str`
            Type of user passed in url parameter. Can be either id or username
            to limit lookup by their respective type. Passing empty or invalid
            value will result in id lookup followed by username lookup if not found.

        **Returns**

        :class:`User`
            Includes attributes account_history, active_tournament_banner,
            badges, beatmap_playcounts_count, favourite_beatmapset_count,
            follower_count, graveyard_beatmapset_count, groups,
            loved_beatmapset_count, monthly_playcounts, page,
            previous_usernames, rank_history: For specified mode,
            ranked_and_approved_beatmapset_count, replays_watched_counts,
            scores_best_count: For specified mode., scores_first_count: For specified mode.,
            scores_recent_count: For specified mode.,
            statistics: For specified mode. Inludes rank and variants attributes.,
            support_level, unranked_beatmapset_count, user_achievements
        """
        return User(self.http.get(Path.get_user(user, mode), key=key))

    def get_users(self, ids):
        """
        Returns list of users.

        Requires OAuth and scope lazer

        **Parameters**

        ids: :class:`list`
            User id to be returned. Specify once for each user id requested. Up to 50 users can be requested at once.

        **Returns**

        :class:`list`
            list containing objects of type :class:`UserCompact`.
            Includes attributes: country, cover, groups, statistics_fruits,
            statistics_mania, statistics_osu, statistics_taiko.
        """
        return [UserCompact(user) for user in self.http.get(Path.get_users(), ids=ids)]

    def get_wiki_page(self, locale, path, page=None):
        """
        The wiki article or image data.

        No OAuth required.

        **Parameters**

        locale

        path

        page: :class:`str`
            The path name of the wiki page.

        **Returns**

        :class:`WikiPage`
        """
        return WikiPage(self.http.get(Path.get_wiki_page(locale, path), page=page))

    def make_request(self, method, path, scope, **kwargs):
        """
        Gives you freedom to format the contents of the request.

        **Parameters**

        method: :class:`str`
            The request method (get, post, delete, patch, or put)

        path: :class:`str`
            Url path to send request to (excluding the base api url) Ex. "beatmapsets/search"

        scope: :class:`str`
            Used for the purpose of creating the Path object but will also be checked against the scopes you are valid for.
            For valid scopes check :class:`Scope.valid_scopes`
        """
        return getattr(self.http, method)(Path(path, scope), **kwargs)

    # Undocumented

    def search_beatmapsets(self, filters=None, page=None):
        resp = self.http.get(Path(f'beatmapsets/search', 'public'), page=page, **filters)
        return {
            'content': {
                'beatmapsets': [Beatmapset(beatmapset) for beatmapset in resp['content']['beatmapsets']],
                'cursor': resp['content']['cursor'],
                'search': resp['content']['search'],
                'recommended_difficulty': resp['content']['recommended_difficulty'],
                'error': resp['content']['error'],
                'total': resp['content']['total']
            },
            'status': resp['status']
        }

    def get_score_by_id(self, mode, score):
        return Score(self.http.get(Path.get_score_by_id(mode, score)))
