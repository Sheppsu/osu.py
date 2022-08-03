"""
Note: Docstrings in this file may be outdated due to laziness of not copying
over docstring edits in the osu/client.py file.
"""
from .http import AsynchronousHTTPHandler as HTTPHandler
from ..objects import *
from ..path import Path
from ..enums import *
from ..auth import AuthHandler
from ..util import parse_mods_arg
from typing import Union, Optional, Sequence


class AsynchronousClient:
    """
    Main object for interacting with osu!api

    **Init Parameters**

    auth: :class:`AuthHandler`
        The AuthHandler object passed in when initiating the Client object

    request_wait_time: Optional[:class:`float`]
        Default is 1.

        This defines the amount of time that the client should wait before making another request.
        It can make it easier to stay within the rate limits without using all your requests up quickly
        and then waiting forever to make another. It's most applicable in bot-type apps.

    limit_per_minute: Optional[:class:`float`]
        Default is 60 because that's the limit peppy requests that we stay under.

        This sets a cap on the number of requests the client is allowed to make within 1 minute of time.

        Use the API for good. Don't overdo it. If in doubt, ask before (ab)using :). this section may expand as necessary.

        Current rate limit is set at an insanely high 1200 requests per minute, with burst capability of up to 200 beyond that.
        If you require more, you probably fall into the above category of abuse. If you are doing more than 60 requests a minute,
        you should probably give peppy a yell.
    """

    def __init__(self, auth=None, request_wait_time: Optional[float] = 1.0,
                 limit_per_minute: Optional[float] = 60.0):
        self.auth = auth
        self.http = HTTPHandler(auth, self, request_wait_time, limit_per_minute)

    @classmethod
    def from_client_credentials(cls, client_id: int, client_secret: str, redirect_url: str,
                                scope: Optional[Scope] = Scope.default(), code: Optional[str] = None,
                                request_wait_time: Optional[float] = 1.0,
                                limit_per_minute: Optional[float] = 60.0):
        """
        Returns a :class:`Client` object from client id, client secret, redirect uri, and scope.

        **Parameters**

        client_id: :class:`int`
            API Client id

        client_secret: :class:`int`
            API Client secret

        redirect_uri: :class:`str`
            API redirect uri

        scope: Optional[:class:`Scope`]
            Scopes to use. Default is Scope.default() which is just the public scope.

        code: Optional[:class:`str`]
            If provided, is used to authorize. Read more about this under :class:`AuthHandler.get_auth_token`

        request_wait_time: Optional[:class:`float`]
            Read under Client init parameters.

        limit_per_minute: Optional[:class:`float`]
            Read under Client init parameters.

        **Returns**

        :class:`Client`
        """
        auth = AuthHandler(client_id, client_secret, redirect_url, scope)
        auth.get_auth_token(code)
        return cls(auth, request_wait_time, limit_per_minute)

    async def lookup_beatmap(self, checksum: Optional[str] = None, filename: Optional[str] = None, id: Optional[int] = None) -> Beatmap:
        """
        Returns beatmap.

        Requires OAuth and scope public

        **Parameters**

        checksum: Optional[:class:`str`]
            An md5 beatmap checksum.

        filename: Optional[:class:`str`]
            A filename to lookup

        id: Optional[:class:`int`]
            A beatmap ID to lookup

        **Returns**

        :class:`Beatmap`
        """
        return Beatmap(await self.http.get(Path.beatmap_lookup(), checksum=checksum, filename=filename, id=id))

    async def get_user_beatmap_score(self, beatmap: int, user: int, mode: Optional[Union[str, GameModeStr]] = None, mods: Optional[Sequence[str]] = None) -> BeatmapUserScore:
        """
        Returns a user's score on a Beatmap

        Requires OAuth and scope public

        **Parameters**

        beatmap: :class:`int`
            Id of the beatmap

        user: :class:`int`
            Id of the user

        mode: Optional[Union[:class:`str`, :class:`GameModeStr`]]
            The game mode to get scores for

        mods: Optional[Sequence[:class:`str`]]
            An array of matching mods, or none. Currently doesn't do anything.

        **Returns**

        :class:`BeatmapUserScore`
        """
        if isinstance(mode, GameModeStr):
            mode = mode.value
        return BeatmapUserScore(await self.http.get(Path.user_beatmap_score(beatmap, user), mode=mode, mods=mods))

    async def get_user_beatmap_scores(self, beatmap: int, user: int, mode: Optional[Union[str, GameModeStr]] = None) -> Sequence[Score]:
        """
        Returns a user's scores on a Beatmap

        Requires OAuth and scope public

        **Parameters**

        beatmap: :class:`int`
            Id of the beatmap

        user: :class:`int`
            Id of the user

        mode: Optional[Union[:class:`str`, :class:`GameModeStr`]]
            The game mode to get scores for

        **Returns**

        Sequence[:class:`Score`]
        """
        if isinstance(mode, GameModeStr):
            mode = mode.value
        return list(map(Score, (await self.http.get(Path.user_beatmap_scores(beatmap, user), mode=mode))["scores"]))

    async def get_beatmap_scores(self, beatmap: int, mode: Optional[Union[str, GameModeStr]] = None, mods: Optional[Sequence[str]] = None, type: Optional[Sequence[str]] = None) -> BeatmapScores:
        """
        Returns the top scores for a beatmap

        Requires OAuth and scope public

        **Parameters**

        beatmap: :class:`int`
            Id of the beatmap

        mode: Optional[Union[:class:`str`, :class:`GameModeStr`]]
            The game mode to get scores for

        mods: Optional[Sequence[:class:`str`]]
            An array of matching mods, or none. Currently doesn't do anything.

        type: Optional[Sequence[:class:`str`]]
            Beatmap score ranking type. Currently doesn't do anything.

        **Returns**

        :class:`BeatmapScores`
        """
        if isinstance(mode, GameModeStr):
            mode = mode.value
        return BeatmapScores(await self.http.get(Path.beatmap_scores(beatmap), mode=mode, mods=mods, type=type))

    async def get_beatmap(self, beatmap: int) -> Beatmap:
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
        return Beatmap(await self.http.get(Path.beatmap(beatmap)))

    async def get_beatmaps(self, ids: Optional[Sequence[int]] = None) -> Sequence[Beatmap]:
        """
        Returns list of beatmaps.

        Requires OAuth and scope public

        **Parameters**

        ids: Optional[List[:class:`int`]]
            Beatmap id to be returned. Specify once for each beatmap id requested. Up to 50 beatmaps can be requested at once.

        **Returns**

        Sequence[:class:`BeatmapCompact`]
            Includes: beatmapset (with ratings), failtimes, max_combo.
        """
        results = await self.http.get(Path.beatmaps(), **{"ids[]": ids})
        return list(map(Beatmap, results['beatmaps'])) if results else []

    async def get_beatmap_attributes(self, beatmap: int, mods: Optional[Union[int, Mods, Sequence[Union[str, Mods, int]]]]=None, ruleset: Optional[Union[str, GameModeStr]] = None, ruleset_id: Optional[Union[int, GameModeInt]] = None) -> BeatmapDifficultyAttributes:
        """
        Returns difficulty attributes of beatmap with specific mode and mods combination.

        Requires OAuth and scope public

        **Parameters**

        beatmap: :class:`int`
            Beatmap id.

        mods: Optional[Union[:class:`int`, Sequence[Union[:class:`str`, :class:`Mods`, :class:`int`]], :class:`Mods`]]
            Mod combination. Can be either a bitset of mods, a Mods enum, or array of any. Defaults to no mods.
            Some mods may cause the api to throw an HTTP 422 error depending on the map's gamemode.

        ruleset: Optional[Union[:class:`GameModeStr`, :class:`int`]]
            Ruleset of the difficulty attributes. Only valid if it's the beatmap ruleset or the beatmap can be converted to the specified ruleset. Defaults to ruleset of the specified beatmap.

        ruleset_id: Optional[Union[:class:`GameModeInt`, :class:`int`]]
            The same as ruleset but in integer form.

        **Returns**

        :class:`BeatmapDifficultyAttributes`
        """
        if isinstance(ruleset, GameModeStr):
            ruleset = ruleset.value
        if isinstance(ruleset_id, GameModeInt):
            ruleset_id = ruleset_id.value
        return BeatmapDifficultyAttributes(await self.http.post(Path.get_beatmap_attributes(beatmap), mods=parse_mods_arg(mods), ruleset=ruleset, ruleset_id=ruleset_id))

    async def get_beatmapset_discussion_posts(self, beatmapset_discussion_id: Optional[int] = None, limit: Optional[int] = None,
                                        page: Optional[int] = None, sort: Optional[str] = None, user: Optional[int] = None,
                                        with_deleted: Optional[str] = None) -> dict:
        """
        Returns the posts of the beatmapset discussions

        Requires OAuth and scope public

        **Parameters**

        beatmapset_discussion_id: Optional[:class:`int`]
            id of the BeatmapsetDiscussion

        limit: Optional[:class:`int`]
            Maximum number of results

        page: Optional[:class:`int`]
            Search results page.

        sort: Optional[:class:`str`]
            id_desc for newest first; id_asc for oldest first. Defaults to id_desc

        user: Optional[:class:`int`]
            The id of the User

        with_deleted: Optional[:class:`str`]
            The param has no effect as api calls do not currently receive group permissions

        **Returns**

        :class:`dict`
            {
            beatmapsets: :class:`BeatmapsetCompact`,

            cursor: :class:`dict`,

            posts: Sequence[:class:`BeatmapsetDiscussionPost`],

            users: :class:`UserCompact`
            }
        """
        # TODO: Change is supposed to occur on the response given back from the server, make sure to change it when that happens.
        resp = await self.http.get(Path.beatmapset_discussion_posts(), beatmapset_discussion_id=beatmapset_discussion_id,
                             limit=limit, page=page, sort=sort, user=user, with_deleted=with_deleted)
        return {
            'beatmapsets': list(map(BeatmapsetCompact, resp['beatmapsets'])),
            'cursor': resp['cursor'],
            'posts': list(map(BeatmapsetDiscussionPost, resp['posts'])),
            'users': list(map(UserCompact, resp['users']))
        }

    async def get_beatmapset_discussion_votes(self, beatmapset_discussion_id: Optional[int] = None, limit: Optional[int] = None,
                                        page: Optional[int] = None, receiver: Optional[int] = None, score: Optional[int] = None,
                                        sort: Optional[str] = None, user: Optional[int] = None, with_deleted: Optional[str] = None) -> dict:
        """
        Returns the votes given to beatmapset discussions

        Requires OAuth and scope public

        **Parameters**

        beatmapset_discussion_id: Optional[:class:`int`]
            id of the BeatmapsetDiscussion

        limit: Optional[:class:`int`]
            Maximum number of results

        page: Optional[:class:`int`]
            Search results page.

        receiver: Optional[:class:`int`]
            The id of the User receiving the votes.

        score: Optional[:class:`int`]
            1 for upvote, -1 for downvote

        sort: Optional[:class:`str`]
            id_desc for newest first; id_asc for oldest first. Defaults to id_desc

        user: Optional[:class:`int`]
            The id of the User giving the votes.

        with_deleted: Optional[:class:`str`]
            The param has no effect as api calls do not currently receive group permissions

        **Returns**

        :class:`dict`
            {
            cursor: :class:`dict`,

            discussions: Sequence[:class:`BeatmapsetDiscussion`],

            users: Sequence[:class:`UserCompact`],

            votes: Sequence[:class:`BeatmapsetDiscussionVote`]
            }
        """
        # TODO: Change is supposed to occur on the response given back from the server, make sure to change it when that happens.
        resp = await self.http.get(Path.beatmapset_discussion_votes(), beatmapset_discussion_id=beatmapset_discussion_id,
                             limit=limit, receiver=receiver, score=score, page=page, sort=sort, user=user, with_deleted=with_deleted)
        return {
            'cursor': resp['cursor'],
            'discussions': list(map(BeatmapsetDiscussion, resp['discussions'])),
            'users': list(map(UserCompact, resp['users'])),
            'votes': list(map(BeatmapsetDiscussionVote, resp['votes']))
        }

    async def get_beatmapset_discussions(self, beatmap_id: Optional[int] = None, beatmapset_id: Optional[int] = None,
                                   beatmapset_status: Optional[str] = None, limit: Optional[int] = None,
                                   message_types: Optional[Sequence[str]] = None, only_unresolved: Optional[bool] = None,
                                   page: Optional[int] = None, sort: Optional[str] = None, user: Optional[int] = None,
                                   with_deleted: Optional[str] = None) -> dict:
        """
        Returns a list of beatmapset discussions

        Requires OAuth and scope public

        **Parameters**

        beatmap_id: Optional[:class:`int`]
            id of the Beatmap

        beatmapset_id: Optional[:class:`int`]
            id of the Beatmapset

        beatmapset_status: Optional[:class:`str`]
            One of all, ranked, qualified, disqualified, never_qualified. Defaults to all.

        limit: Optional[:class:`int`]
            Maximum number of results.

        message_types: Optional[Sequence[:class:`str`]]
            suggestion, problem, mapper_note, praise, hype, review. Blank defaults to all types.

        only_unresolved: Optional[:class:`bool`]
            true to show only unresolved issues; false, otherwise. Defaults to false.

        page: Optional[:class:`int`]
            Search result page.

        sort: Optional[:class:`str`]
            id_desc for newest first; id_asc for oldest first. Defaults to id_desc.

        user: Optional[:class:`int`]
            The id of the User.

        with_deleted: Optional[:class:`str`]
            This param has no effect as api calls do not currently receive group permissions.

        **Returns**

        :class:`dict`
            {

            beatmaps: Sequence[:class:`Beatmap`],
                List of beatmaps associated with the discussions returned.

            cursor: :class:`dict`,

            discussions: Sequence[:class:`BeatmapsetDiscussion`],
                List of discussions according to sort order.

            included_discussions: Sequence[:class:`BeatmapsetDiscussion`],
                Additional discussions related to discussions.

            reviews_config.max_blocks: :class:`int`,
                Maximum number of blocks allowed in a review.

            users: Sequence[:class:`UserCompact`]
                List of users associated with the discussions returned.

            }
        """
        # TODO: Change is supposed to occur on the response given back from the server, make sure to change it when that happens.
        message_types = {"message_types[]": message_types}
        resp = await self.http.get(Path.beatmapset_discussions(), beatmap_id=beatmap_id, beatmapset_id=beatmapset_id,
                             beatmapset_status=beatmapset_status, limit=limit, only_unresolved=only_unresolved,
                             page=page, sort=sort, user=user, with_deleted=with_deleted, **message_types)
        return {
            'beatmaps': list(map(Beatmap, resp['beatmaps'])),
            'cursor': resp['cursor'],
            'discussions': list(map(BeatmapsetDiscussion, resp['discussions'])),
            'included_discussions': list(map(BeatmapsetDiscussion, resp['included_discussions'])),
            'reviews_config.max_blocks': resp['reviews_config'],
            'users': list(map(UserCompact, resp['users']))
        }

    async def get_changelog_build(self, stream: str, build: str) -> Build:
        """
        Returns details of the specified build.

        **Parameters**

        stream: :class:`str`
            Update stream name.

        build: :class:`str`
            Build version.

        **Returns**

        A :class:`Build` with changelog_entries, changelog_entries.github_user, and versions included.
        """
        return Build(await self.http.get(Path.get_changelog_build(stream, build)))

    async def get_changelog_listing(self, from_version: Optional[str] = None, max_id: Optional[int] = None,
                              stream: Optional[str] = None, to: Optional[str] = None,
                              message_formats: Optional[Sequence[str]] = None) -> dict:
        """
        Returns a listing of update streams, builds, and changelog entries.

        **Parameters**

        from_version: Optional[:class:`str`]
            Minimum build version.

        max_id: Optional[:class:`int`]
            Maximum build ID.

        stream: Optional[:class:`str`]
            Stream name to return builds from.

        to: Optional[:class:`str`]
            Maximum build version.

        message_formats: Optional[Sequence[:class:`str`]]
            html, markdown. Default to both.

        **Returns**

        {

        "build": Sequence[:class:`Build`]

        "search": {

            "from": :class:`str`
                from_version input.

            "limit": :class:`int`
                Always 21.

            "max_id": :class:`int`
                max_id input.

            "stream": :class:`str`
                stream input.

            "to": :class:`str`
                to input.

        }

        "streams": Sequence[:class:`UpdateStream`]

        }
        """
        response = await self.http.get(Path.get_changelog_listing(), max_id=max_id, stream=stream, to=to, message_formats=message_formats, **{"from": from_version})
        return {
            "build": list(map(Build, response['builds'])),
            "search": response['search'],
            "streams": list(map(UpdateStream, response['streams'])),
        }

    async def lookup_changelog_build(self, changelog: str, key: Optional[str] = None, message_formats: Optional[Sequence[str]] = None) -> Build:
        """
        Returns details of the specified build.

        **Parameter**

        changelog: :class:`str`
            Build version, update stream name, or build ID.

        key: Optional[:class:`str`]
            Unset to query by build version or stream name, or id to query by build ID.

        message_formats: Optional[Sequence[:class:`str`]]
            html, markdown. Default to both.

        **Returns**

        A :class:`Build` with changelog_entries, changelog_entries.github_user, and versions included.
        """
        return Build(await self.http.get(Path.lookup_changelog_build(changelog), key=key, message_formats=message_formats))

    async def create_new_pm(self, target_id: int, message: str, is_action: bool) -> dict:
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

            presence: Sequence[:class:`ChatChannel`]
                array of ChatChannel

            message: :class:`ChatMessage`
                the sent ChatMessage

            }
        """
        data = {'target_id': target_id, 'message': message, 'is_action': is_action}
        resp = await self.http.post(Path.create_new_pm(), data=data)
        return {
            'new_channel_id': resp['new_channel_id'],
            'presence': list(map(ChatChannel, resp['presence'])),
            'message': ChatMessage(resp['message'])
        }

    async def get_updates(self, since: int, channel_id: Optional[int] = None, limit: Optional[int] = None) -> dict:
        """
        This endpoint returns new messages since the given message_id along with updated channel 'presence' data.

        Requires OAuth and scope lazer

        **Parameters**

        since: :class:`int`
            The message_id of the last message to retrieve messages since

        channel_id: Optional[:class:`int`]
            If provided, will only return messages for the given channel

        limit: Optional[:class:`int`]
            number of messages to return (max of 50)

        **Returns**

        :class:`dict`
            {
            presence: List[:class:`ChatChannel`],

            messages: List[:class:`ChatMessage`]

            }
        """
        resp = await self.http.post(Path.get_updates(), since=since, channel_id=channel_id, limit=limit)
        return {
            'presence': list(map(ChatChannel, resp['presence'])),
            'messages': list(map(ChatMessage, resp['messages'])),
            'silences': list(map(UserSilence, resp['silences']))
        }

    async def get_channel_messages(self, channel_id: int, limit: Optional[int] = None, since: Optional[int] = None, until: Optional[int] = None) -> Sequence[ChatMessage]:
        """
        This endpoint returns the chat messages for a specific channel.

        Requires OAuth and scope lazer

        **Parameter**

        channel_id: :class:`int`
            The ID of the channel to retrieve messages for

        limit: Optional[:class:`int`]
            number of messages to return (max of 50)

        since: Optional[:class:`int`]
            messages after the specified message id will be returned

        until: Optional[:class:`int`]
            messages up to but not including the specified message id will be returned

        **Returns**

        Sequence[:class:`ChatMessage`]
            list containing :class:`ChatMessage` objects
        """
        return list(map(ChatMessage, await self.http.post(Path.get_channel_messages(channel_id), limit=limit, since=since, until=until)))

    async def send_message_to_channel(self, channel_id: int, message: str, is_action: bool) -> ChatMessage:
        """
        This endpoint sends a message to the specified channel.

        Requires OAuth and scope lazer

        **Parameters**

        channel_id: :class:`int`
            The channel_id of the channel to send message to

        message: :class:`str`
            message to send

        is_action: :class:`bool`
            whether the message is an action

        **Returns**

        :class:`ChatMessage`
        """
        data = {'message': message, 'is_action': is_action}
        return ChatMessage(await self.http.post(Path.send_message_to_channel(channel_id), data=data))

    async def join_channel(self, channel: int, user: int) -> ChatChannel:
        """
        This endpoint allows you to join a public channel.

        Requires OAuth and scope lazer

        **Parameters**

        channel: :class:`int`

        user: :class:`int`

        **Returns**

        :class:`ChatChannel`
        """
        return ChatChannel(await self.http.put(Path.join_channel(channel, user)))

    async def leave_channel(self, channel: int, user: int):
        """
        This endpoint allows you to leave a public channel.

        Requires OAuth and scope lazer

        **Parameters**

        channel: :class:`int`

        user: :class:`int`
        """
        await self.http.delete(Path.leave_channel(channel, user))

    async def mark_channel_as_read(self, channel: str, message: str, channel_id: int, message_id: int):
        """
        This endpoint marks the channel as having being read up to the given message_id.

        Requires OAuth and scope lazer

        **Parameters**

        channel: :class:`str`

        message: :class:`str`

        channel_id: :class:`int`
            The channel_id of the channel to mark as read

        message_id: :class:`int`
            The message_id of the message to mark as read up to
        """
        await self.http.put(Path.mark_channel_as_read(channel, message), channel_id=channel_id, message_id=message_id)

    async def get_channel_list(self) -> Sequence[ChatChannel]:
        """
        This endpoint returns a list of all joinable public channels.

        Requires OAuth and scope lazer

        **Returns**

        Sequence[:class:`ChatChannel`]
        """
        return list(map(ChatChannel, await self.http.get(Path.get_channel_list())))

    async def create_channel(self, type: str, target_id: Optional[int] = None) -> ChatChannel:
        """
        This endpoint creates a new channel if doesn't exist and joins it. Currently only for rejoining existing PM channels which the user has left.

        Requires OAuth and scope lazer

        **Parameter**

        type: :class:`str`
            channel type (currently only supports "PM")

        target_id: Optional[:class:`int`]
            target user id for type PM

        **Returns**

        :class:`ChatChannel`
             contains recent_messages attribute. Note that if there's no existing PM channel,
             most of the fields will be blank. In that case, send a message (create_new_pm) instead to create the channel.
        """
        data = {'type': type, 'target_id': target_id}
        return ChatChannel(await self.http.post(Path.create_channel(), data=data))

    async def get_channel(self, channel: int) -> dict:
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
        resp = await self.http.get(Path.get_channel(channel))
        return {
            'channel': ChatChannel(resp['channel']),
            'users': UserCompact(resp['users']),
        }

    async def get_comments(self, commentable_type: Optional[str] = None, commentable_id: Optional[int] = None,
                     cursor: Optional[dict] = None, parent_id: Optional[int] = None, sort: Optional[str] = None) -> CommentBundle:
        """
        Returns a list comments and their replies up to 2 levels deep.

        Does not require OAuth

        **Parameter**

        commentable_type: Optional[:class:`str`]
            The type of resource to get comments for.

        commentable_id: Optional[:class:`int`]
            The id of the resource to get comments for.

        cursor: Optional[:class:`dict`]
            Pagination option. See :ref:`CommentSort` for detail. The format follows Cursor except it's not currently included in the response.

        parent_id: Optional[:class:`int`]
            Limit to comments which are reply to the specified id. Specify 0 to get top level comments.

        sort: Optional[:class:`str`]
            Sort option as defined in :ref:`CommentSort`. Defaults to new for guests and user-specified default when authenticated.

        **Returns**

        :class:`CommentBundle`
            pinned_comments is only included when commentable_type and commentable_id are specified.
        """
        return CommentBundle(await self.http.get(Path.get_comments(), commentable_type=commentable_type, commentable_id=commentable_id,
                                           **cursor if cursor else {}, parent_id=parent_id, sort=sort))

    async def post_comment(self, commentable_id: Optional[int] = None, commentable_type: Optional[str] = None,
                     message: Optional[str] = None, parent_id: Optional[int] = None) -> CommentBundle:
        """
        Posts a new comment to a comment thread.

        Requires OAuth and scope lazer

        **Parameter**

        commentable_id: Optional[:class:`int`]
            Resource ID the comment thread is attached to

        commentable_type: Optional[:class:`str`]
            Resource type the comment thread is attached to

        message: Optional[:class:`str`]
            Text of the comment

        parent_id: Optional[:class:`int`]
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
        return CommentBundle(await self.http.post(Path.post_new_comment(), params=params))

    async def get_comment(self, comment: int) -> CommentBundle:
        """
        Gets a comment and its replies up to 2 levels deep.

        Does not require OAuth

        **Parameters**

        comment: :class:`int`
            Comment id

        **Returns**

        :class:`CommentBundle`
        """
        return CommentBundle(await self.http.get(Path.get_comment(comment)))

    async def edit_comment(self, comment: int, message: Optional[str] = None) -> CommentBundle:
        """
        Edit an existing comment.

        Requires OAuth and scope lazer

        **Parameters**

        comment: :class:`int`
            Comment id

        message: Optional[:class:`str`]
            New text of the comment

        **Returns**

        :class:`CommentBundle`
        """
        params = {'comment.message': message}
        return CommentBundle(await self.http.patch(Path.edit_comment(comment), params=params))

    async def delete_comment(self, comment: int) -> CommentBundle:
        """
        Deletes the specified comment.

        Requires OAuth and scope lazer

        **Parameters**

        comment: :class:`int`
            Comment id

        **Returns**

        :class:`CommentBundle`
        """
        return CommentBundle(await self.http.delete(Path.delete_comment(comment)))

    async def add_comment_vote(self, comment: int) -> CommentBundle:
        """
        Upvotes a comment.

        Requires OAuth and scope lazer

        **Parameters**

        comment: :class:`int`
            Comment id

        **Returns**

        :class:`CommentBundle`
        """
        return CommentBundle(await self.http.post(Path.add_comment_vote(comment)))

    async def remove_comment_vote(self, comment: int) -> CommentBundle:
        """
        Un-upvotes a comment.

        Requires OAuth and scope lazer

        **Parameters**

        comment: :class:`int`
            Comment id

        **Returns**

        :class:`CommentBundle`
        """
        return CommentBundle(await self.http.delete(Path.remove_comment_vote(comment)))

    async def reply_topic(self, topic: int, body: str) -> ForumPost:
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
        return ForumPost(await self.http.post(Path.reply_topic(topic), data=data))

    async def create_topic(self, body: str, forum_id: int, title: str, with_poll: Optional[bool] = None,
                     hide_results: Optional[bool] = None, length_days: Optional[int] = None,
                     max_options: Optional[int] = None, poll_options: Optional[str] = None,
                     poll_title: Optional[str] = None, vote_change: Optional[bool] = None) -> dict:
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

        with_poll: Optional[:class:`bool`]
            Enable this to also create poll in the topic (default: false).

        hide_results: Optional[:class:`bool`]
            Enable this to hide result until voting period ends (default: false).

        length_days: Optional[:class:`int`]
            Number of days for voting period. 0 means the voting will never ends (default: 0). This parameter is required if hide_results option is enabled.

        max_options: Optional[:class:`int`]
            Maximum number of votes each user can cast (default: 1).

        poll_options: Optional[:class:`str`]
            Newline-separated list of voting options. BBCode is supported.

        poll_title: Optional[:class:`str`]
            Title of the poll.

        vote_change: Optional[:class:`bool`]
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
        resp = await self.http.post(Path.create_topic(), data=data)
        return {
            'topic': ForumTopic(resp['topic']),
            'post': ForumPost(resp['post'])
        }

    async def get_topic_and_posts(self, topic: int, cursor: Optional[dict] = None, sort: Optional[str] = None,
                            limit: Optional[int] = None, start: Optional[int] = None, end: Optional[int] = None) -> dict:
        """
        Get topic and its posts.

        Requires OAuth and scope public

        **Parameters**

        topic: :class:`int`
            Id of the topic.

        cursor: Optional[:class:`dict`]
            To be used to fetch the next page of results

        sort: Optional[:class:`str`]
            Post sorting option. Valid values are id_asc (default) and id_desc.

        limit: Optional[:class:`int`]
            Maximum number of posts to be returned (20 default, 50 at most).

        start: Optional[:class:`int`]
            First post id to be returned with sort set to id_asc. This parameter is ignored if cursor is specified.

        end: Optional[:class:`int`]
            First post id to be returned with sort set to id_desc. This parameter is ignored if cursor is specified.

        **Returns**

        :class:`dict`
            {
            cursor: :class:`dict`,

            search: :class:`dict`,

            posts: Sequence[:class:`ForumPost`],

            topic: :class:`ForumTopic`

            }
        """
        resp = await self.http.get(Path.get_topic_and_posts(topic), **cursor if cursor else {}, sort=sort, limit=limit, start=start, end=end)
        return {
            'cursor': resp['cursor'],
            'search': resp['search'],
            'posts': list(map(ForumPost, resp['posts'])),
            'topic': ForumTopic(resp['topic'])
        }

    async def edit_topic(self, topic: int, topic_title: str) -> ForumTopic:
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
        return ForumTopic(await self.http.patch(Path.edit_topic(topic), data=data))

    async def edit_post(self, post: int, body: str) -> ForumPost:
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
        return ForumPost(await self.http.patch(Path.edit_post(post), data=data))

    async def search(self, mode: Optional[Union[str, WikiSearchMode]] = None, query: Optional[str] = None, page: Optional[int] = None) -> dict:
        """
        Searches users and wiki pages.

        Requires OAuth and scope public

        **Parameters**

        mode: Optional[Union[:class:`str`, :class:`GameModeStr`]]
            Either all, user, or wiki_page. Default is all.

        query: Optional[:class:`str`]
            Search keyword.

        page: Optional[:class:`int`]
            Search result page. Ignored for mode all.

        **Returns**

        :class:`dict`
            {

            user: :class:`dict`
                For all or user mode. Only first 100 results are accessible
                {
                results: Sequence

                total: :class:`int`
                }

            wiki_page: :class:`dict`
                For all or wiki_page mode
                {
                results: Sequence

                total: :class:`int`
                }

            }
        """
        if isinstance(mode, WikiSearchMode):
            mode = mode.value
        resp = await self.http.get(Path.search(), mode=mode, query=query, page=page)
        return {
            'user': {'results': resp['user']['data'], 'total': resp['user']['total']} if mode is None or mode == 'all' or mode == 'user' else None,
            'wiki_page': {'results': resp['wiki_page']['data'], 'total': resp['wiki_page']['total']} if mode is None or mode == 'all' or mode == 'wiki_page' else None
        }

    async def get_user_highscore(self, room: int, playlist: int, user: int) -> MultiplayerScores:
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

        :class:`MultiplayerScores`
        """
        # Doesn't say response type
        return MultiplayerScores(await self.http.get(Path.get_user_high_score(room, playlist, user)))

    async def get_scores(self, room: int, playlist: int, limit: Optional[int] = None,
                   sort: Optional[str] = None, cursor: Optional[dict] = None) -> MultiplayerScores:
        """
        Requires OAuth and scope public

        **Parameters**

        room: :class:`int`
            Id of the room.

        playlist: :class:`int`
            Id of the playlist item.

        limit: Optional[:class:`int`]
            Number of scores to be returned.

        sort: Optional[:class:`str`]
            :ref:`MultiplayerScoresSort` parameter.

        cursor: Optional[:class:`dict`]

        **Returns**

        :class:`MultiplayerScores`
        """
        # Doesn't say response type
        return MultiplayerScores(await self.http.get(Path.get_scores(room, playlist), limit=limit, sort=sort, **cursor if cursor else {}))

    async def get_score(self, room: int, playlist: int, score: int) -> MultiplayerScore:
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

        :class:`MultiplayerScore`
        """
        # Doesn't say response type
        return MultiplayerScore(await self.http.get(Path.get_score(room, playlist, score)))

    async def get_news_listing(self, limit: Optional[int] = None, year: Optional[int] = None, cursor: Optional[dict] = None) -> dict:
        """
        Returns a list of news posts and related metadata.

        **Parameters**

        limit: Optional[:class:`int`]
            Maximum number of posts (12 default, 1 minimum, 21 maximum).

        year: Optional[:class:`int`]
            Year to return posts from.

        cursor: Optional[:class:`dict`]
            Cursor for pagination.

        **Returns**

        {

        cursor: :class:`dict`

        news_posts: Sequence[:class:`NewsPost`]
            Includes preview.

        news_sidebar: {

            current_year: :class:`int`
                Year of the first post's publish time, or current year if no posts returned.

            years: :class:`int`
                All years during which posts have been published.

            news_posts: Sequence[:class:`NewsPost`]
                All posts published during current_year.

        }

        search: {

            limit: :class:`int`
                Clamped limit input.

            sort: :class:`str`
                Always published_desc.

            }

        }
        """
        response = await self.http.get(Path.get_news_listing(), limit=limit, year=year, cursor=cursor)
        return {
            "cursor": response['cursor'],
            "news_posts": list(map(NewsPost, response["news_posts"])),
            "news_sidebar": {
                "current_year": response['news_sidebar']['current_year'],
                "years": response['news_sidebar']['years'],
                "news_posts": list(map(NewsPost, response['news_sidebar']['news_posts'])),
            },
            "search": response['search']
        }

    async def get_news_post(self, news: str, key: Optional[str] = None) -> NewsPost:
        """
        Returns details of the specified news post.

        **Parameters**

        news: class:`str`
            News post slug or ID.

        key: Optional[:class:`str`]
            Unset to query by slug, or id to query by ID.

        **Returns**

        Returns a :class:`NewsPost` with content and navigation included.
        """
        return NewsPost(await self.http.get(Path.get_news_post(news), key=key))

    async def get_notifications(self, max_id: Optional[int] = None) -> dict:
        """
        This endpoint returns a list of the user's unread notifications. Sorted descending by id with limit of 50.

        Requires OAuth and scope lazer

        **Parameters**

        max_id: Optional[:class:`int`]
            Maximum id fetched. Can be used to load earlier notifications. Defaults to no limit (fetch latest notifications)

        **Returns**

        :class:`dict`
            {

            has_more: :class:`bool`,
                whether or not there are more notifications

            notifications: Sequence[:class:`Notification`],

            unread_count: :class:`bool`
                total unread notifications

            notification_endpoint: :class:`str`
                url to connect to websocket server

            }
        """
        resp = await self.http.get(Path.get_notifications(), max_id=max_id)
        return {
            'has_more': resp['has_more'],
            'notifications': list(map(Notification, resp['notifications'])),
            'unread_count': resp['unread_count'],
            'notification_endpoint': resp['notification_endpoint'],
        }

    async def mark_notifications_read(self, ids: Sequence[int]):
        """
        This endpoint allows you to mark notifications read.

        Requires OAuth and scope lazer

        **Parameters**

        ids: Sequence[:class:`int`]
            ids of notifications to be marked as read.
        """
        data = {'ids[]': ids}
        await self.http.post(Path.mark_notifications_as_read(), data=data)

    async def revoke_current_token(self):
        """
        Requires OAuth
        """
        await self.http.delete(self, Path.revoke_current_token())

    async def get_ranking(self, mode: Union[str, GameModeStr], type: str, country: Optional[str] = None, cursor: Optional[dict] = None,
                    filter: Optional[str] = None, spotlight: Optional[int] = None, variant: Optional[str] = None) -> Rankings:
        """
        Gets the current ranking for the specified type and game mode.

        Requires OAuth and scope public

        mode: Union[:class:`str`, :class:`GameModeStr`]

        type: :class:`str`
            :ref:`RankingType`

        country: Optional[:class:`str`]
            Filter ranking by country code. Only available for type of performance.

        cursor: Optional[:class:`dict`]

        filter: Optional[:class:`str`]
            Either all (default) or friends.

        spotlight: Optional[:class:`int`]
            The id of the spotlight if type is charts. Ranking for latest spotlight will be returned if not specified.

        variant: Optional[:class:`str`]
            Filter ranking to specified mode variant. For mode of mania, it's either 4k or 7k. Only available for type of performance.

        **Returns**

        :class:`Rankings`
        """
        if isinstance(mode, GameModeStr):
            mode = mode.value
        return Rankings(await self.http.get(Path.get_ranking(mode, type), country=country, **cursor if cursor else {}, filter=filter,
                                      spotlight=spotlight, variant=variant))

    async def get_spotlights(self) -> Spotlights:
        """
        Gets the list of spotlights.

        Requires OAuth and scope public

        **Returns**

        :class:`Spotlights`
        """
        return Spotlights(await self.http.get(Path.get_spotlights()))

    async def get_own_data(self, mode: Union[str, GameModeStr]="") -> User:
        """
        Similar to get_user but with authenticated user (token owner) as user id.

        Requires OAuth and scope identify

        **Parameters**

        mode: Optional[:class:`str`, :class:`GameModeStr`]
            GameMode. User default mode will be used if not specified.

        **Returns**

        See return for get_user
        """
        if isinstance(mode, GameModeStr):
            mode = mode.value
        return User(await self.http.get(Path.get_own_data(mode)))

    async def get_user_kudosu(self, user: int, limit: Optional[int] = None, offset: Optional[int] = None):
        """
        Returns kudosu history.

        Requires OAuth and scope public

        **Parameters**

        user: :class:`int`
            Id of the user.

        limit: Optional[:class:`int`]
            Maximum number of results.

        offset: Optional[:class:`int`]
            Result offset for pagination.

        **Returns**

        Sequence[:class:`KudosuHistory`]
        """
        return list(map(KudosuHistory, await self.http.get(Path.get_user_kudosu(user), limit=limit, offset=offset)))

    async def get_user_scores(self, user: int, type: str, include_fails: Optional[int] = None, mode: Optional[Union[str, GameModeStr]] = None,
                        limit: Optional[int] = None, offset: Optional[int] = None) -> Sequence[Score]:
        """
        This endpoint returns the scores of specified user.

        Requires OAuth and scope public

        **Parameters**

        user: :class:`int`
            Id of the user.

        type: :class:`str`
            Score type. Must be one of these: best, firsts, recent

        include_fails: Optional[:class:`int`]
            Only for recent scores, include scores of failed plays. Set to 1 to include them. Defaults to 0.

        mode: Optional[Union[:class:`str`, :class:`GameModeStr`]]
            game mode of the scores to be returned. Defaults to the specified user's mode.

        limit: Optional[:class:`int`]
            Maximum number of results.

        offset: Optional[:class:`int`]
            Result offset for pagination.

        **Returns**

        Sequence[:class:`Score`]
            Includes attributes beatmap, beatmapset, weight: Only for type best, user
        """
        if isinstance(mode, GameModeStr):
            mode = mode.value
        return [Score(score) for score in await self.http.get(Path.get_user_scores(user, type), include_fails=include_fails, mode=mode, limit=limit, offset=offset)]

    async def get_user_beatmaps(self, user: int, type: Union[str, UserBeatmapType], limit: Optional[int] = None, offset: Optional[int] = None) -> Sequence[Union[BeatmapPlaycount, Beatmapset]]:
        """
        Returns the beatmaps of specified user.

        Requires OAuth and scope public

        **Parameters**

        user: :class:`int`
            Id of the user.

        type: Union[:class:`str`, :class:`UserBeatmapType`]
            Beatmap type. Can be one of the following - favourite, graveyard, loved, most_played, pending, ranked.

        limit: Optional[:class:`int`]
            Maximum number of results.

        offset: Optional[:class:`int`]
            Result offset for pagination.

        **Returns**

        Sequence[Union[:class:`BeatmapPlaycount`, :class:`Beatmapset`]]
            :class:`BeatmapPlaycount` for type most_played or :class:`Beatmapset` for any other type.
        """
        object_type = Beatmapset
        if isinstance(type, UserBeatmapType):
            type = type.value
        if type == 'most_played':
            object_type = BeatmapPlaycount
        return list(map(object_type, await self.http.get(Path.get_user_beatmaps(user, type), limit=limit, offset=offset)))

    async def get_user_recent_activity(self, user: int, limit: Optional[int] = None, offset: Optional[int] = None) -> Sequence[Event]:
        """
        Returns recent activity.

        Requires OAuth and scope public

        **Parameters**

        user: :class:`int`
            Id of the user.

        limit: Optional[:class:`int`]
            Maximum number of results.

        offset: Optional[:class:`int`]
            Result offset for pagination.

        **Returns**

        Sequence[:class:`Event`]
            list of :class:`Event` objects
        """
        return list(map(Event, await self.http.get(Path.get_user_recent_activity(user), limit=limit, offset=offset)))

    async def get_user(self, user: int, mode: Optional[Union[str, GameModeStr]] = '', key: Optional[str] = None) -> User:
        """
        This endpoint returns the detail of specified user.

        Requires OAuth and scope public

        **Parameters**

        user: Union[:class:`int`, :class:`str`]
            Id or username of the user. Id lookup is prioritised unless key parameter is specified.
            Previous usernames are also checked in some cases.

        mode: Optional[Union[:class:`str`, :class:`GameModeStr`]
            User default mode will be used if not specified.

        key: Optional[:class:`str`]
            Type of user passed in url parameter. Can be either id or username
            to limit lookup by their respective type. Passing empty or invalid
            value will result in id lookup followed by username lookup if not found.

        **Returns**

        :class:`User`
            Includes following attributes: account_history, active_tournament_banner,
            badges, beatmap_playcounts_count, favourite_beatmapset_count, follower_count,
            graveyard_beatmapset_count, groups, loved_beatmapset_count,
            mapping_follower_count, monthly_playcounts, page, pending_beatmapset_count,
            previous_usernames, rank_history, ranked_beatmapset_count, replays_watched_counts,
            scores_best_count, scores_first_count, scores_recent_count, statistics,
            statistics.country_rank, statistics.rank, statistics.variants, support_level,
            user_achievements.
        """
        if isinstance(mode, GameModeStr):
            mode = mode.value
        return User(await self.http.get(Path.get_user(user, mode), key=key))

    async def get_users(self, ids: Sequence[int]) -> Sequence[UserCompact]:
        """
        Returns list of users.

        Requires OAuth and scope lazer

        **Parameters**

        ids: Sequence[:class:`int`]
            User id to be returned. Specify once for each user id requested. Up to 50 users can be requested at once.

        **Returns**

        Sequence[:class:`UserCompact`]
            list of :class:`UserCompact` objects.
            Includes attributes: country, cover, groups, statistics_fruits,
            statistics_mania, statistics_osu, statistics_taiko.
        """
        return list(map(UserCompact, await self.http.get(Path.get_users(), ids=ids)))

    async def get_wiki_page(self, locale: str, path: str) -> WikiPage:
        """
        The wiki article or image data.

        No OAuth required.

        **Parameters**

        locale: :class:`str`
            Two-letter language code of the wiki page.

        path: :class:`str`
            The path name of the wiki page.

        **Returns**

        :class:`WikiPage`
        """
        return WikiPage(await self.http.get(Path.get_wiki_page(locale, path)))

    async def make_request(self, method: str, path: str, scope: Union[Scope, str], **kwargs):
        """
        Gives you freedom to format the contents of the request.

        **Parameters**

        method: :class:`str`
            The request method (get, post, delete, patch, or put)

        path: :class:`str`
            Url path to send request to (excluding the base api url) Ex. "beatmapsets/search"

        scope: Union[:class:`Scope`, :class:`str`]
            Used for the purpose of creating the Path object but will also be checked against the scopes you are valid for.
            For valid scopes check :class:`Scope.valid_scopes`
        """
        return getattr(self.http, method)(Path(path, scope), **kwargs)

    # Undocumented

    async def search_beatmapsets(self, filters=None, page=None):
        if filters is None:
            filters = {}
        resp = await self.http.get(Path(f'beatmapsets/search', 'public'), page=page, **filters)
        return {
            'beatmapsets': [Beatmapset(beatmapset) for beatmapset in resp['beatmapsets']],
            'cursor': resp['cursor'],
            'search': resp['search'],
            'recommended_difficulty': resp['recommended_difficulty'],
            'error': resp['error'],
            'total': resp['total'],
        }

    async def get_score_by_id(self, mode, score):
        return Score(await self.http.get(Path.get_score_by_id(mode, score)))
