from .http import HTTPHandler
from .objects import *
from .path import Path
from .enums import *
from .auth import AuthHandler
from .util import parse_mods_arg, parse_enum_args, BeatmapsetSearchFilter
from typing import Union, Optional, Sequence, Dict
from datetime import datetime
from osrparse import Replay


class Client:
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

    Make sure if you are changing the ratelimit handling that you are still following peppy's
    TOU for using the API:

    Use the API for good. Don't overdo it. If in doubt, ask before (ab)using :).
    this section may expand as necessary.

    Current rate limit is set at an insanely high 1200 requests per minute,
    with burst capability of up to 200 beyond that.
    If you require more, you probably fall into the above category of abuse.
    If you are doing more than 60 requests a minute,
    you should probably give peppy a yell.
    """
    def __init__(self, auth=None, request_wait_time: Optional[float] = 1.0,
                 limit_per_minute: Optional[float] = 60.0):
        self.auth = auth
        self.http = HTTPHandler(self, request_wait_time, limit_per_minute)

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

    def lookup_beatmap(self, checksum: Optional[str] = None, filename: Optional[str] = None,
                       id: Optional[int] = None) -> Beatmap:
        """
        Returns beatmap.

        Requires OAuth and scope public

        **Parameters**

        checksum: Optional[:class:`str`]
            A beatmap checksum.

        filename: Optional[:class:`str`]
            A filename to lookup

        id: Optional[:class:`int`]
            A beatmap ID to lookup

        **Returns**

        :class:`Beatmap`
        """
        return Beatmap(self.http.make_request('get', Path.beatmap_lookup(), checksum=checksum,
                                              filename=filename, id=id))

    def get_user_beatmap_score(self, beatmap: int, user: int, mode: Optional[Union[str, GameModeStr]] = None,
                               mods: Optional[Sequence[str]] = None) -> BeatmapUserScore:
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
        mode = parse_enum_args(mode)
        return BeatmapUserScore(self.http.make_request('get', Path.user_beatmap_score(beatmap, user),
                                                       mode=mode, mods=mods))

    def get_user_beatmap_scores(self, beatmap: int, user: int,
                                mode: Optional[Union[str, GameModeStr]] = None) -> Sequence[LegacyScore]:
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

        Sequence[:class:`LegacyScore`]
        """
        mode = parse_enum_args(mode)
        return list(map(LegacyScore, self.http.make_request('get', Path.user_beatmap_scores(beatmap, user),
                                                      mode=mode)["scores"]))

    def get_beatmap_scores(self, beatmap: int, mode: Optional[Union[str, GameModeStr]] = None,
                           mods: Optional[Sequence[str]] = None,
                           type: Optional[Sequence[str]] = None) -> BeatmapScores:
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
            :class:`LegacyScore` object inside includes "user" and the included user includes "country" and "cover".
        """
        mode = parse_enum_args(mode)
        return BeatmapScores(self.http.make_request('get', Path.beatmap_scores(beatmap), mode=mode,
                                                    mods=mods, type=type))

    def get_lazer_beatmap_scores(self, beatmap: int, mode: Optional[Union[str, GameModeStr]] = None,
                                 mods: Optional[Sequence[str]] = None,
                                 type: Optional[Sequence[str]] = None) -> BeatmapScores:
        """
        Returns the top scores for a beatmap on the lazer client.

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
            :class:`LazerScore` object inside includes "user" and the included user includes "country" and "cover".
        """
        mode = parse_enum_args(mode)
        return BeatmapScores(self.http.make_request('get', Path.lazer_beatmap_scores(beatmap), mode=mode,
                                                    mods=mods, type=type), "lazer")

    def get_beatmap(self, beatmap: int) -> Beatmap:
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
        return Beatmap(self.http.make_request('get', Path.beatmap(beatmap)))

    def get_beatmaps(self, ids: Optional[Sequence[int]] = None) -> Sequence[Beatmap]:
        """
        Returns list of beatmaps.

        Requires OAuth and scope public

        **Parameters**

        ids: Optional[List[:class:`int`]]
            Beatmap id to be returned. Specify once for each beatmap id requested.
            Up to 50 beatmaps can be requested at once.

        **Returns**

        Sequence[:class:`BeatmapCompact`]
            Includes: beatmapset (with ratings), failtimes, max_combo.
        """
        results = self.http.make_request('get', Path.beatmaps(), **{"ids[]": ids})
        return list(map(Beatmap, results['beatmaps'])) if results else []

    def get_beatmap_attributes(self, beatmap: int,
                               mods: Optional[Union[int, Mods, Sequence[Union[str, Mods, int]]]] = None,
                               ruleset: Optional[Union[str, GameModeStr]] = None,
                               ruleset_id: Optional[Union[int, GameModeInt]] = None) -> BeatmapDifficultyAttributes:
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
            Ruleset of the difficulty attributes. Only valid if it's the beatmap ruleset or the beatmap can be
            converted to the specified ruleset. Defaults to ruleset of the specified beatmap.

        ruleset_id: Optional[Union[:class:`GameModeInt`, :class:`int`]]
            The same as ruleset but in integer form.

        **Returns**

        :class:`BeatmapDifficultyAttributes`
        """
        ruleset, ruleset_id = parse_enum_args(ruleset, ruleset_id)
        return BeatmapDifficultyAttributes(self.http.make_request('post', Path.get_beatmap_attributes(beatmap),
                                                                  mods=parse_mods_arg(mods), ruleset=ruleset,
                                                                  ruleset_id=ruleset_id))

    def get_beatmapset(self, beatmapset_id: int) -> Beatmapset:
        """
        Get beatmapset by id.

        Requires OAuth and scope public

        **Parameters**

        beatmapset_id: :class:`int`

        **Returns**

        :class:`Beatmapset`
        """
        return Beatmapset(self.http.make_request('get', Path.get_beatmapset(beatmapset_id)))

    def get_beatmapset_discussion_posts(self, beatmapset_discussion_id: Optional[int] = None,
                                        limit: Optional[int] = None, page: Optional[int] = None,
                                        sort: Optional[str] = None, user: Optional[int] = None,
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
        # TODO: Change is supposed to occur on the response given back from the server,
        #  make sure to change it when that happens.
        resp = self.http.make_request('get', Path.beatmapset_discussion_posts(),
                                      beatmapset_discussion_id=beatmapset_discussion_id,
                                      limit=limit, page=page, sort=sort, user=user, with_deleted=with_deleted)
        return {
            'beatmapsets': list(map(BeatmapsetCompact, resp['beatmapsets'])),
            'cursor': resp['cursor'],
            'posts': list(map(BeatmapsetDiscussionPost, resp['posts'])),
            'users': list(map(UserCompact, resp['users']))
        }

    def get_beatmapset_discussion_votes(self, beatmapset_discussion_id: Optional[int] = None,
                                        limit: Optional[int] = None, page: Optional[int] = None,
                                        receiver: Optional[int] = None, score: Optional[int] = None,
                                        sort: Optional[str] = None, user: Optional[int] = None,
                                        with_deleted: Optional[str] = None) -> dict:
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
        # TODO: Change is supposed to occur on the response given back from the server,
        #  make sure to change it when that happens.
        resp = self.http.make_request('get', Path.beatmapset_discussion_votes(),
                                      beatmapset_discussion_id=beatmapset_discussion_id,
                                      limit=limit, receiver=receiver, score=score, page=page,
                                      sort=sort, user=user, with_deleted=with_deleted)
        return {
            'cursor': resp['cursor'],
            'discussions': list(map(BeatmapsetDiscussion, resp['discussions'])),
            'users': list(map(UserCompact, resp['users'])),
            'votes': list(map(BeatmapsetDiscussionVote, resp['votes']))
        }

    def get_beatmapset_discussions(self, beatmap_id: Optional[int] = None, beatmapset_id: Optional[int] = None,
                                   beatmapset_status: Optional[str] = None, limit: Optional[int] = None,
                                   message_types: Optional[Sequence[str]] = None,
                                   only_unresolved: Optional[bool] = None, page: Optional[int] = None,
                                   sort: Optional[str] = None, user: Optional[int] = None,
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
        # TODO: Change is supposed to occur on the response given back from the server,
        #  make sure to change it when that happens.
        message_types = {"message_types[]": message_types}
        resp = self.http.make_request('get', Path.beatmapset_discussions(), beatmap_id=beatmap_id,
                                      beatmapset_id=beatmapset_id, beatmapset_status=beatmapset_status,
                                      limit=limit, only_unresolved=only_unresolved, page=page, sort=sort,
                                      user=user, with_deleted=with_deleted, **message_types)
        return {
            'beatmaps': list(map(Beatmap, resp['beatmaps'])),
            'cursor': resp['cursor'],
            'discussions': list(map(BeatmapsetDiscussion, resp['discussions'])),
            'included_discussions': list(map(BeatmapsetDiscussion, resp['included_discussions'])),
            'reviews_config.max_blocks': resp['reviews_config'],
            'users': list(map(UserCompact, resp['users']))
        }

    def get_changelog_build(self, stream: str, build: str) -> Build:
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
        return Build(self.http.make_request('get', Path.get_changelog_build(stream, build)))

    def get_changelog_listing(self, from_version: Optional[str] = None, max_id: Optional[int] = None,
                              stream: Optional[str] = None, to: Optional[str] = None,
                              message_formats: Optional[Sequence[str]] = None) -> \
            Dict[str, Union[Sequence[Build], Sequence[UpdateStream], Dict[str, Union[str, int, None]]]]:
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
        response = self.http.make_request('get', Path.get_changelog_listing(), max_id=max_id,
                                          stream=stream, to=to, message_formats=message_formats,
                                          **{"from": from_version})
        return {
            "build": list(map(Build, response['builds'])),
            "search": response['search'],
            "streams": list(map(UpdateStream, response['streams'])),
        }

    def lookup_changelog_build(self, changelog: str, key: Optional[str] = None,
                               message_formats: Optional[Sequence[str]] = None) -> Build:
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
        return Build(self.http.make_request('get', Path.lookup_changelog_build(changelog),
                                            key=key, message_formats=message_formats))

    def create_new_pm(self, target_id: int, message: str, is_action: bool) -> dict:
        """
        This endpoint allows you to create a new PM channel.

        Requires OAuth, scope chat.write, and a user (authorization code grant or delegate scope)

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
        resp = self.http.make_request('post', Path.create_new_pm(), data=data)
        return {
            'new_channel_id': resp['new_channel_id'],
            'presence': list(map(ChatChannel, resp['presence'])),
            'message': ChatMessage(resp['message'])
        }

    def get_updates(self, since: int, channel_id: Optional[int] = None, limit: Optional[int] = None) -> dict:
        """
        This endpoint returns new messages since the given message_id along with updated channel 'presence' data.

        Requires OAuth, scope lazer, a user (authorization code grant or delegate scope)

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
        resp = self.http.make_request('post', Path.get_updates(), since=since, channel_id=channel_id, limit=limit)
        return {
            'presence': list(map(ChatChannel, resp['presence'])),
            'messages': list(map(ChatMessage, resp['messages'])),
            'silences': list(map(UserSilence, resp['silences']))
        }

    def get_channel_messages(self, channel_id: int, limit: Optional[int] = None, since: Optional[int] = None,
                             until: Optional[int] = None) -> Sequence[ChatMessage]:
        """
        This endpoint returns the chat messages for a specific channel.

        Requires OAuth, scope lazer, and a user (authorization code grant or delegate scope)

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
        return list(map(ChatMessage, self.http.make_request('post', Path.get_channel_messages(channel_id),
                                                            limit=limit, since=since, until=until)))

    def send_message_to_channel(self, channel_id: int, message: str, is_action: bool) -> ChatMessage:
        """
        This endpoint sends a message to the specified channel.

        Requires OAuth, scope lazer, and a user (authorization code grant or delegate scope)

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
        return ChatMessage(self.http.make_request('post', Path.send_message_to_channel(channel_id), data=data))

    def join_channel(self, channel: int, user: int) -> ChatChannel:
        """
        This endpoint allows you to join a public channel.

        Requires OAuth, scope lazer, and a user (authorization code grant or delegate scope)

        **Parameters**

        channel: :class:`int`

        user: :class:`int`

        **Returns**

        :class:`ChatChannel`
        """
        return ChatChannel(self.http.make_request('put', Path.join_channel(channel, user)))

    def leave_channel(self, channel: int, user: int):
        """
        This endpoint allows you to leave a public channel.

        Requires OAuth, scope lazer, and a user (authorization code grant or delegate scope)

        **Parameters**

        channel: :class:`int`

        user: :class:`int`
        """
        self.http.make_request('delete', Path.leave_channel(channel, user))

    def mark_channel_as_read(self, channel: str, message: str, channel_id: int, message_id: int):
        """
        This endpoint marks the channel as having being read up to the given message_id.

        Requires OAuth, scope lazer, and a user (authorization code grant or delegate scope)

        **Parameters**

        channel: :class:`str`

        message: :class:`str`

        channel_id: :class:`int`
            The channel_id of the channel to mark as read

        message_id: :class:`int`
            The message_id of the message to mark as read up to
        """
        self.http.make_request('put', Path.mark_channel_as_read(channel, message), channel_id=channel_id,
                               message_id=message_id)

    def get_channel_list(self) -> Sequence[ChatChannel]:
        """
        This endpoint returns a list of all joinable public channels.

        Requires OAuth, scope lazer, and a user (authorization code grant or delegate scope)

        **Returns**

        Sequence[:class:`ChatChannel`]
        """
        return list(map(ChatChannel, self.http.make_request('get', Path.get_channel_list())))

    def create_channel(self, type: str, target_id: Optional[int] = None) -> ChatChannel:
        """
        This endpoint creates a new channel if doesn't exist and joins it.
        Currently only for rejoining existing PM channels which the user has left.

        Requires OAuth, scope lazer, and a user (authorization code grant or delegate scope)

        **Parameter**

        type: :class:`str`
            channel type (currently only supports "PM")

        target_id: Optional[:class:`int`]
            target user id for type PM

        **Returns**

        :class:`ChatChannel`
             contains recent_messages attribute. Note that if there's no existing PM channel,
             most of the fields will be blank. In that case, send a message (create_new_pm)
             instead to create the channel.
        """
        data = {'type': type, 'target_id': target_id}
        return ChatChannel(self.http.make_request('post', Path.create_channel(), data=data))

    def get_channel(self, channel: int) -> dict:
        """
        Gets details of a chat channel.

        Requires OAuth, scope lazer, and a user (authorization code grant or delegate scope)

        **Parameter**

        channel: :class:`int`

        **Returns**

        :class:`dict`
            {
            channel: :class:`ChatChannel`,

            users: :class:`UserCompact`

            }
        """
        resp = self.http.make_request('get', Path.get_channel(channel))
        return {
            'channel': ChatChannel(resp['channel']),
            'users': UserCompact(resp['users']),
        }

    def get_comments(self, commentable_type: Optional[str] = None, commentable_id: Optional[int] = None,
                     cursor: Optional[dict] = None, parent_id: Optional[int] = None,
                     sort: Optional[Union[str, CommentSort]] = None) -> CommentBundle:
        """
        Returns a list comments and their replies up to 2 levels deep.

        Does not require OAuth

        **Parameter**

        commentable_type: Optional[:class:`str`]
            The type of resource to get comments for.

        commentable_id: Optional[:class:`int`]
            The id of the resource to get comments for.

        cursor: Optional[:class:`dict`]
            Pagination option. See :class:`CommentSort` for detail.
            The format follows Cursor except it's not currently included in the response.

        parent_id: Optional[:class:`int`]
            Limit to comments which are reply to the specified id. Specify 0 to get top level comments.

        sort: Optional[Union[:class:`str`, :class:`CommentSort`]]
            Sort option as defined in :class:`CommentSort`.
            Defaults to new for guests and user-specified default when authenticated.

        **Returns**

        :class:`CommentBundle`
            pinned_comments is only included when commentable_type and commentable_id are specified.
        """
        sort = parse_enum_args(sort)
        return CommentBundle(self.http.make_request('get', Path.get_comments(), commentable_type=commentable_type,
                                                    commentable_id=commentable_id, **(cursor if cursor else {}),
                                                    parent_id=parent_id, sort=sort))

    def post_comment(self, commentable_id: Optional[int] = None, commentable_type: Optional[str] = None,
                     message: Optional[str] = None, parent_id: Optional[int] = None) -> CommentBundle:
        """
        Posts a new comment to a comment thread.

        Requires OAuth, scope lazer, and a user (authorization code grant or delegate scope)

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
        return CommentBundle(self.http.make_request('post', Path.post_new_comment(), params=params))

    def get_comment(self, comment: int) -> CommentBundle:
        """
        Gets a comment and its replies up to 2 levels deep.

        Does not require OAuth

        **Parameters**

        comment: :class:`int`
            Comment id

        **Returns**

        :class:`CommentBundle`
        """
        return CommentBundle(self.http.make_request('get', Path.get_comment(comment)))

    def edit_comment(self, comment: int, message: Optional[str] = None) -> CommentBundle:
        """
        Edit an existing comment.

        Requires OAuth, scope lazer, and a user (authorization code grant or delegate scope)

        **Parameters**

        comment: :class:`int`
            Comment id

        message: Optional[:class:`str`]
            New text of the comment

        **Returns**

        :class:`CommentBundle`
        """
        params = {'comment.message': message}
        return CommentBundle(self.http.make_request('patch', Path.edit_comment(comment), params=params))

    def delete_comment(self, comment: int) -> CommentBundle:
        """
        Deletes the specified comment.

        Requires OAuth, scope lazer, and a user (authorization code grant or delegate scope)

        **Parameters**

        comment: :class:`int`
            Comment id

        **Returns**

        :class:`CommentBundle`
        """
        return CommentBundle(self.http.make_request('delete', Path.delete_comment(comment)))

    def add_comment_vote(self, comment: int) -> CommentBundle:
        """
        Upvotes a comment.

        Requires OAuth, scope lazer, and a user (authorization code grant or delegate scope)

        **Parameters**

        comment: :class:`int`
            Comment id

        **Returns**

        :class:`CommentBundle`
        """
        return CommentBundle(self.http.make_request('post', Path.add_comment_vote(comment)))

    def remove_comment_vote(self, comment: int) -> CommentBundle:
        """
        Un-upvotes a comment.

        Requires OAuth, scope lazer, and a user (authorization code grant or delegate scope)

        **Parameters**

        comment: :class:`int`
            Comment id

        **Returns**

        :class:`CommentBundle`
        """
        return CommentBundle(self.http.make_request('delete', Path.remove_comment_vote(comment)))

    def reply_topic(self, topic: int, body: str) -> ForumPost:
        """
        Create a post replying to the specified topic.

        Requires OAuth, scope forum.write, and a user (authorization code grant or delegate scope)

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
        return ForumPost(self.http.make_request('post', Path.reply_topic(topic), data=data))

    def create_topic(self, body: str, forum_id: int, title: str, with_poll: Optional[bool] = None,
                     hide_results: Optional[bool] = None, length_days: Optional[int] = None,
                     max_options: Optional[int] = None, poll_options: Optional[str] = None,
                     poll_title: Optional[str] = None, vote_change: Optional[bool] = None) -> dict:
        """
        Create a new topic.

        Requires OAuth, scope forum.write, and a user (authorization code grant or delegate scope)

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
            Number of days for voting period. 0 means the voting will never ends (default: 0).
            This parameter is required if hide_results option is enabled.

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
                'hide_results': hide_results, 'length_days': length_days,
                'max_options': max_options, 'poll_options': poll_options,
                'poll_title': poll_title, 'vote_change': vote_change
            }})
        resp = self.http.make_request('post', Path.create_topic(), data=data)
        return {
            'topic': ForumTopic(resp['topic']),
            'post': ForumPost(resp['post'])
        }

    def get_topic_and_posts(self, topic: int, cursor: Optional[dict] = None, sort: Optional[str] = None,
                            limit: Optional[int] = None, start: Optional[int] = None,
                            end: Optional[int] = None) -> dict:
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
            First post id to be returned with sort set to id_asc.
            This parameter is ignored if cursor is specified.

        end: Optional[:class:`int`]
            First post id to be returned with sort set to id_desc.
            This parameter is ignored if cursor is specified.

        **Returns**

        :class:`dict`
            {
            cursor: :class:`dict`,

            search: :class:`dict`,

            posts: Sequence[:class:`ForumPost`],

            topic: :class:`ForumTopic`

            }
        """
        resp = self.http.make_request('get', Path.get_topic_and_posts(topic), **(cursor if cursor else {}),
                                      sort=sort, limit=limit, start=start, end=end)
        return {
            'cursor': resp['cursor'],
            'search': resp['search'],
            'posts': list(map(ForumPost, resp['posts'])),
            'topic': ForumTopic(resp['topic'])
        }

    def edit_topic(self, topic: int, topic_title: str) -> ForumTopic:
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
        return ForumTopic(self.http.make_request('patch', Path.edit_topic(topic), data=data))

    def edit_post(self, post: int, body: str) -> ForumPost:
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
        return ForumPost(self.http.make_request('patch', Path.edit_post(post), data=data))

    def search(self, mode: Optional[Union[str, WikiSearchMode]] = None, query: Optional[str] = None,
               page: Optional[int] = None) -> dict:
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
        mode = parse_enum_args(mode)
        resp = self.http.make_request('get', Path.search(), mode=mode, query=query, page=page)
        return {
            'user': {'results': resp['user']['data'], 'total': resp['user']['total']}
            if mode is None or mode == 'all' or mode == 'user' else None,
            'wiki_page': {'results': resp['wiki_page']['data'], 'total': resp['wiki_page']['total']}
            if mode is None or mode == 'all' or mode == 'wiki_page' else None
        }

    def get_user_highscore(self, room: int, playlist: int, user: int) -> MultiplayerScore:
        """
        Requires OAuth, scope lazer, and a user (authorization code grant or delegate scope)

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
        return MultiplayerScore(self.http.make_request('get', Path.get_user_high_score(room, playlist, user)))

    def get_scores(self, room: int, playlist: int, limit: Optional[int] = None,
                   sort: Optional[Union[str, MultiplayerScoresSort]] = None,
                   cursor: Optional[dict] = None) -> MultiplayerScores:
        """
        Requires OAuth, scope public, and a user (authorization code grant or delegate scope)

        **Parameters**

        room: :class:`int`
            Id of the room.

        playlist: :class:`int`
            Id of the playlist item.

        limit: Optional[:class:`int`]
            Number of scores to be returned.

        sort: Optional[Union[:class:`str`, :class:`MultiplayerScoresSort`]]


        cursor: Optional[:class:`dict`]

        **Returns**

        :class:`MultiplayerScores`
        """
        sort = parse_enum_args(sort)
        return MultiplayerScores(self.http.make_request('get', Path.get_scores(room, playlist),
                                                        limit=limit, sort=sort, **(cursor if cursor else {})))

    def get_score(self, room: int, playlist: int, score: int) -> MultiplayerScore:
        """
        Requires OAuth, scope lazer, and a user (authorization code grant or delegate scope)

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
        return MultiplayerScore(self.http.make_request('get', Path.get_score(room, playlist, score)))

    def get_news_listing(self, limit: Optional[int] = None, year: Optional[int] = None,
                         cursor: Optional[dict] = None) -> dict:
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
        response = self.http.make_request('get', Path.get_news_listing(), limit=limit, year=year, cursor=cursor)
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

    def get_news_post(self, news: str, key: Optional[str] = None) -> NewsPost:
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
        return NewsPost(self.http.make_request('get', Path.get_news_post(news), key=key))

    def get_notifications(self, max_id: Optional[int] = None) -> dict:
        """
        This endpoint returns a list of the user's unread notifications. Sorted descending by id with limit of 50.

        Requires OAuth, scope lazer, a user (authorization code grant or delegate scope)

        **Parameters**

        max_id: Optional[:class:`int`]
            Maximum id fetched. Can be used to load earlier notifications.
            Defaults to no limit (fetch latest notifications)

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
        resp = self.http.make_request('get', Path.get_notifications(), max_id=max_id)
        return {
            'has_more': resp['has_more'],
            'notifications': list(map(Notification, resp['notifications'])),
            'unread_count': resp['unread_count'],
            'notification_endpoint': resp['notification_endpoint'],
        }

    def mark_notifications_read(self, ids: Sequence[int]):
        """
        This endpoint allows you to mark notifications read.

        Requires OAuth, scope lazer, a user (authorization code grant or delegate scope)

        **Parameters**

        ids: Sequence[:class:`int`]
            ids of notifications to be marked as read.
        """
        data = {'ids[]': ids}
        self.http.make_request('post', Path.mark_notifications_as_read(), data=data)

    def revoke_current_token(self):
        """
        Requires OAuth
        """
        self.http.make_request('delete', self, Path.revoke_current_token())

    def get_ranking(self, mode: Union[str, GameModeStr], type: Union[str, RankingType],
                    country: Optional[str] = None, cursor: Optional[dict] = None,
                    filter: Optional[str] = None, spotlight: Optional[int] = None,
                    variant: Optional[str] = None) -> Rankings:
        """
        Gets the current ranking for the specified type and game mode.

        Requires OAuth and scope public

        mode: Union[:class:`str`, :class:`GameModeStr`]

        type: Union[:class:`str`, :class:`RankingType`]
            :ref:`RankingType`

        country: Optional[:class:`str`]
            Filter ranking by country code. Only available for type of performance.

        cursor: Optional[:class:`dict`]

        filter: Optional[:class:`str`]
            Either all (default) or friends.

        spotlight: Optional[:class:`int`]
            The id of the spotlight if type is charts.
            Ranking for latest spotlight will be returned if not specified.

        variant: Optional[:class:`str`]
            Filter ranking to specified mode variant.
            For mode of mania, it's either 4k or 7k. Only available for type of performance.

        **Returns**

        :class:`Rankings`
        """
        mode, type = parse_enum_args(mode, type)
        return Rankings(self.http.make_request('get', Path.get_ranking(mode, type), country=country,
                                               **(cursor if cursor else {}), filter=filter,
                                               spotlight=spotlight, variant=variant))

    def get_spotlights(self) -> Spotlights:
        """
        Gets the list of spotlights.

        Requires OAuth and scope public

        **Returns**

        :class:`Spotlights`
        """
        return Spotlights(self.http.make_request('get', Path.get_spotlights()))

    def get_own_data(self, mode: Union[str, GameModeStr] = "") -> User:
        """
        Similar to get_user but with authenticated user (token owner) as user id.

        Requires OAuth, scope identify, and a user (authorization code grant or delegate scope)

        **Parameters**

        mode: Optional[:class:`str`, :class:`GameModeStr`]
            GameMode. User default mode will be used if not specified.

        **Returns**

        See return for get_user
        """
        mode = parse_enum_args(mode)
        return User(self.http.make_request('get', Path.get_own_data(mode)))

    def get_user_kudosu(self, user: int, limit: Optional[int] = None, offset: Optional[int] = None):
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
        return list(map(KudosuHistory, self.http.make_request('get', Path.get_user_kudosu(user),
                                                              limit=limit, offset=offset)))

    def get_user_scores(self, user: int, type: str, include_fails: Optional[int] = None,
                        mode: Optional[Union[str, GameModeStr]] = None, limit: Optional[int] = None,
                        offset: Optional[int] = None) -> Sequence[LegacyScore]:
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

        Sequence[:class:`LegacyScore`]
            Includes attributes beatmap, beatmapset, weight: Only for type best, user
        """
        mode = parse_enum_args(mode)
        return [LegacyScore(score) for score in self.http.make_request('get', Path.get_user_scores(user, type),
                                                                 include_fails=include_fails, mode=mode,
                                                                 limit=limit, offset=offset)]

    def get_user_beatmaps(self, user: int, type: Union[str, UserBeatmapType], limit: Optional[int] = None,
                          offset: Optional[int] = None) -> Sequence[Union[BeatmapPlaycount, Beatmapset]]:
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
        type = parse_enum_args(type)
        if type == 'most_played':
            object_type = BeatmapPlaycount
        return list(map(object_type, self.http.make_request('get', Path.get_user_beatmaps(user, type),
                                                            limit=limit, offset=offset)))

    def get_user_recent_activity(self, user: int, limit: Optional[int] = None,
                                 offset: Optional[int] = None) -> Sequence[Event]:
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
        return list(map(Event, self.http.make_request('get', Path.get_user_recent_activity(user),
                                                      limit=limit, offset=offset)))

    def get_user(self, user: int, mode: Optional[Union[str, GameModeStr]] = '', key: Optional[str] = None) -> User:
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
        mode = parse_enum_args(mode)
        return User(self.http.make_request('get', Path.get_user(user, mode), key=key))

    def get_users(self, ids: Sequence[int]) -> Sequence[UserCompact]:
        """
        Returns list of users.

        Requires OAuth and scope public

        **Parameters**

        ids: Sequence[:class:`int`]
            User id to be returned. Specify once for each user id requested.
            Up to 50 users can be requested at once.

        **Returns**

        Sequence[:class:`UserCompact`]
            Includes attributes: country, cover, groups, statistics_rulesets.
        """
        res = self.http.make_request('get', Path.get_users(), **{"ids[]": ids})
        return list(map(UserCompact, res["users"]))

    def get_wiki_page(self, locale: str, path: str) -> WikiPage:
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
        return WikiPage(self.http.make_request('get', Path.get_wiki_page(locale, path)))

    def get_beatmapset_events(self, page: Optional[int] = None, limit: Optional[int] = None,
                              sort: Optional[Union[str, BeatmapsetEventSort]] = None,
                              type: Optional[Union[str, BeatmapsetEventType]] = None,
                              min_date: Optional[Union[str, datetime]] = None,
                              max_date: Optional[Union[str, datetime]] = None) -> \
            Dict[str, Union[Sequence[BeatmapsetEvent], Dict, Sequence[UserCompact]]]:
        """
        Returns a list of beatmapset events.

        Requires OAuth and scope public.

        **Parameters**

        page: Optional[:class:`int`]

        limit: Optional[:class:`int`]

        sort: Optional[Union[:class:`str`, :class:`BeatmapsetEventSort`]]
            Specified a sort order.

        type: Optional[Union[:class:`str`, :class:`BeatmapsetEventType`]]
            Specifies for only a certain type of event to be returned.

        **Returns**

        Dict[str, Union[Sequence[BeatmapsetEvent], Dict, Sequence[UserCompact]]]

        {

            'events': Sequence[BeatmapsetEvent],

            'reviews_config': Dict,

            'users': Sequence[UserCompact]

        }
        """
        sort, type = parse_enum_args(sort, type)
        if isinstance(min_date, datetime):
            min_date = min_date.isoformat()
        if isinstance(max_date, datetime):
            max_date = max_date.isoformat()
        resp = self.http.make_request('get', Path.get_beatmapset_events(), page=page, limit=limit, sort=sort,
                                      type=type, min_date=min_date, max_date=max_date)
        return {
            "events": [BeatmapsetEvent(event) for event in resp['events']],
            "reviews_config": resp['reviewsConfig'],
            "users": [UserCompact(user) for user in resp['users']],
        }

    def get_matches(self, limit=None, sort=None) -> Dict[str, Union[Sequence[Match], Dict]]:
        """
        Returns a list of matches.

        Requires OAuth and scope public.

        **Parameters**

        limit: Optional[:class:`int`]

        sort: Optional[Union[:class:`str`, :class:`MatchSort`]]

        **Returns**

        Dict[:class:`str`, Union[Dict, Sequence[:class:`Match`]]]
        """
        sort = parse_enum_args(sort)
        resp = self.http.make_request('get', Path.get_matches(), limit=limit, sort=sort)
        return {
            "matches": list(map(Match, resp['matches'])),
            "cursor": resp['cursor'],
            "params": resp['params'],
        }

    def get_match(self, match_id: int) -> Match:
        """
        Returns a match by id.

        Requires OAuth and scope public.

        **Parameters**

        match_id: :class:`int`
            The match id.

        **Returns**

        :class:`Match`
        """
        return MatchExtended(self.http.make_request('get', Path.get_match(match_id)))

    def get_rooms(self, mode: Union[str, GameModeStr] = '', sort: Union[str, RoomSort] = None) -> Sequence[Room]:
        """
        Returns a list of rooms.

        Requires OAuth, scope public, and a user (authorization code grant or delegate scope).

        **Parameters**

        mode: Optional[Union[:class:`str`, :class:`GameModeStr`]]
            Game mode to filter rooms by.

        sort: Optional[Union[:class:`str`, :class:`RoomSort`]]
            Sort rooms by.
        """
        mode = parse_enum_args(mode)
        return list(map(Room, self.http.make_request('get', Path.get_rooms(mode), sort=sort)))

    def get_seasonal_backgrounds(self) -> SeasonalBackgrounds:
        """
        Get the season backgrounds.

        Doesn't require OAuth

        **Returns**

        :class:`SeasonalBackgrounds`
        """
        return SeasonalBackgrounds(self.http.make_request('get', Path.get_seasonal_backgrounds()))

    def get_room(self, room_id: int) -> Room:
        """
        Returns a room by id.

        Requires OAuth and scope public.

        **Parameters**

        room_id: :class:`int`
            The room id.

        **Returns**

        :class:`Room`
        """
        return Room(self.http.make_request('get', Path.get_room(room_id)))

    def get_score_by_id(self, mode, score_id) -> LegacyScore:
        """
        Returns a score by id.

        Requires OAuth and scope public.

        **Parameters**

        mode: Union[:class:`str`, :class:`GameModeStr`]

        score_id: :class:`int`

        **Returns**

        :class:`LegacyScore`
        """
        mode = parse_enum_args(mode)
        return LegacyScore(self.http.make_request('get', Path.get_score_by_id(mode, score_id)))

    def search_beatmapsets(self, filters=None, page=None):
        """
        Search for beatmapsets.

        Requires OAuth and scope public.

        **Attributes**

        filters: Optional[:class:`BeatmapsetSearchFilter`]

        page: Optional[:class:`int`]
        """
        if filters is None:
            filters = {}
        if isinstance(filters, BeatmapsetSearchFilter):
            filters = filters.filters
        resp = self.http.make_request('get', Path('beatmapsets/search', 'public'), page=page, **filters)
        return {
            'beatmapsets': [Beatmapset(beatmapset) for beatmapset in resp['beatmapsets']],
            'cursor': resp['cursor'],
            'search': resp['search'],
            'recommended_difficulty': resp['recommended_difficulty'],
            'error': resp['error'],
            'total': resp['total'],
        }

    def get_room_leaderboard(self, room_id: int) -> \
            Dict[str, Union[Sequence[UserScoreAggregate], Union[UserScoreAggregate, None]]]:
        """
        Return a room's leaderboard. The :class:`UserScoreAggregate` objects returned under the "leaderboard"
        key contain the "user" attribute. The :class:`UserScoreAggregate` object under the "user_score" key
        contains the "user" and "position" attributes.

        Requires OAuth, scope public, and a user (authorization code grant or delegate scope).

        **Parameters**

        room_id: :class:`int`

        **Returns**

        Dict[:class:`str`, Union[Sequence[:class:`UserScoreAggregate`],
        Union[:class:`UserScoreAggregate`, :class:`NoneType`]]]

        {

            'leaderboard': Sequence[:class:`UserScoreAggregate`],

            'user_score': Union[:class:`UserScoreAggregate`, :class:`NoneType`]

        }
        """
        resp = self.http.make_request('get', Path.get_room_leaderboard(room_id))
        return {
            'leaderboard': list(map(UserScoreAggregate, resp['leaderboard'])),
            'user_score': UserScoreAggregate(resp['user_score']) if resp['user_score'] is not None else None,
        }

    def get_replay_data(self, mode, score_id):
        """
        Returns replay data for a score.

        Requires OAuth, scope public, and a user (authorization code grant or delegate scope).

        **Parameters**

        mode: Union[:class:`str`, :class:`GameModeStr`]

        score_id: :class:`int`

        **Returns**

        :class:`osrparse.Replay`
        """
        mode = parse_enum_args(mode)
        return Replay.from_string(self.http.make_request('get', Path.get_replay_data(mode, score_id), is_download=True))

    def get_friends(self):
        """
        Returns a list of friends.

        Requires OAuth, scope friends.read, and a user (authorization code grant or delegate scope).

        **Returns**

        Sequence[:class:`User`]
        """
        return list(map(UserCompact, self.http.make_request('get', Path.get_friends())))
