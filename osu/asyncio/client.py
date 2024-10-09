from .http import AsynchronousHTTPHandler
from ..objects import *
from ..path import Path
from ..enums import *
from ..auth import BaseAuthHandler, AsynchronousAuthHandler
from ..util import (
    parse_mods_arg,
    parse_enum_args,
    BeatmapsetSearchFilter,
    create_multipart_formdata,
    get_optional_list,
)
from ..results import *

from typing import Union, Optional, Sequence, Dict, List, Awaitable
from datetime import datetime

try:
    import osrparse

    has_osrparse = True
except ImportError:
    has_osrparse = False


class AsynchronousClient:
    """
    Main object for interacting with osu!api, which uses asynchronous requests.
    If you're looking for synchronous requests, use :class:`Client`.

    All the functions of this class are documented under :class:`Client` and function the exact same,
    with the exception of :func:`AsynchronousClient.from_credentials`


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

    __slots__ = ("http",)

    def __init__(
        self, auth: Optional[BaseAuthHandler] = None, request_wait_time: float = 1.0, limit_per_minute: int = 60
    ):
        self.http = AsynchronousHTTPHandler(auth, request_wait_time, limit_per_minute)

    @property
    def auth(self):
        return self.http.auth

    @classmethod
    async def from_client_credentials(
        cls,
        client_id: int,
        client_secret: str,
        redirect_url: Optional[str],
        scope: Optional[Scope] = Scope.default(),
        code: Optional[str] = None,
        request_wait_time: float = 1.0,
        limit_per_minute: int = 60,
    ) -> "AsynchronousClient":
        """
        **DEPRECATED AS OF v2.2.0**

        Use `from_credentials`
        """
        auth = AsynchronousAuthHandler(client_id, client_secret, redirect_url, scope)
        await auth.get_auth_token(code)
        return cls(auth, request_wait_time, limit_per_minute)

    @classmethod
    def from_credentials(
        cls,
        client_id: int,
        client_secret: str,
        redirect_url: Optional[str],
        scope: Optional[Scope] = Scope.default(),
        code: Optional[str] = None,
        request_wait_time: float = 1.0,
        limit_per_minute: int = 60,
        lazily_authenticate: bool = True,
    ) -> Union["AsynchronousClient", Awaitable]:
        """
        Creates client from client id, client secret, redirect uri, and scope.

        **Parameters**

        client_id: :class:`int`
            API Client id

        client_secret: :class:`int`
            API Client secret

        redirect_uri: Optional[:class:`str`]
            API redirect uri

        scope: Optional[:class:`Scope`]
            Scopes to use. Default is Scope.default() which is just the public scope.

        code: Optional[:class:`str`]
            If provided, is used to authorize. Read more about this under :class:`AuthHandler.get_auth_token`

        request_wait_time: Optional[:class:`float`]
            Default is 1.

            This defines the amount of time that the client should wait before making another request.
            It can make it easier to stay within the rate limits without using all your requests up quickly
            and then waiting forever to make another. It's most applicable in bot-type apps.

        limit_per_minute: Optional[:class:`float`]
            Default is 60 because that's the limit peppy requests that we stay under.

            This sets a cap on the number of requests the client is allowed to make within 1 minute of time.

        lazily_authenticate: :class:`bool`
            If true (default), the :class:`AuthHandler` won't authenticate with the api until
            a request is made which requires it. If false, an `Awaitable` is returned.

        **Returns**

        Union[:class:`AsynchronousClient`, Awaitable]
        """
        auth = AsynchronousAuthHandler(client_id, client_secret, redirect_url, scope)
        if not lazily_authenticate:

            async def create():
                await auth.get_auth_token(code)
                return cls(auth, request_wait_time, limit_per_minute)

            return create()

        return cls(auth, request_wait_time, limit_per_minute)

    def set_api_version(self, version: str) -> None:
        """
        Sets x-api-version header to use when sending requests to the api.
        You shouldn't have to change it from the default, but if you need to
        then the function is available.

        **Parameters**

        version: :class:`str`
            x-api-version header value in the format yyyymmdd
        """
        self.http.api_version = version

    async def lookup_beatmap(
        self,
        checksum: Optional[str] = None,
        filename: Optional[str] = None,
        id: Optional[int] = None,
    ) -> Beatmap:
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
        return Beatmap(await self.http.make_request(Path.beatmap_lookup(), checksum=checksum, filename=filename, id=id))

    async def get_user_beatmap_score(
        self,
        beatmap: int,
        user: int,
        mode: Optional[Union[str, GameModeStr]] = None,
        mods: Optional[Sequence[str]] = None,
    ) -> BeatmapUserScore:
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
        return BeatmapUserScore(
            await self.http.make_request(Path.user_beatmap_score(beatmap, user), mode=mode, mods=mods)
        )

    async def get_user_beatmap_scores(
        self, beatmap: int, user: int, mode: Optional[Union[str, GameModeStr]] = None
    ) -> List[Union[LegacyScore, SoloScore]]:
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

        List[Union[:class:`LegacyScore`, :class:`SoloScore`]]
        """
        mode = parse_enum_args(mode)
        resp = await self.http.make_request(Path.user_beatmap_scores(beatmap, user), mode=mode)
        return list(
            map(
                get_score_object,
                resp["scores"],
            )
        )

    def _parse_mods_list(self, mods) -> Optional[List[str]]:
        if mods is None:
            return
        return list(
            map(
                lambda mod: (
                    (Mod[mod.name].value if not isinstance(mod, Mod) else mod.value) if type(mod) != str else mod
                ),
                mods,
            )
        )

    async def get_beatmap_scores(
        self,
        beatmap: int,
        mode: Optional[Union[str, GameModeStr]] = None,
        mods: Optional[Union[Mods, Sequence[Union[Mods, Mod, str]]]] = None,
        ranking_type: Optional[str] = None,
    ) -> BeatmapScores:
        """
        Returns the top scores for a beatmap

        Requires OAuth and scope public

        **Parameters**

        beatmap: :class:`int`
            Id of the beatmap

        mode: Optional[Union[:class:`str`, :class:`GameModeStr`]]
            The game mode to get scores for

        mods: Optional[Union[:class:`Mods`, Sequence[Union[:class:`Mods`, :class:`Mod`, :class:`str`]]]]
            Must pass one of:
            a :class:`Mods` object,
            a list of string mod abbreviations,
            a list of :class:`Mods` objects,
            a list of :classL`Mod` objects

        ranking_type: Optional[:class:`str`]
            Beatmap score ranking type. Currently doesn't do anything.

        **Returns**

        :class:`BeatmapScores`
            :class:`LegacyScore` object inside includes "user" and the included user includes "country" and "cover".
        """
        mode = parse_enum_args(mode)
        mods = self._parse_mods_list(mods)
        return BeatmapScores(
            await self.http.make_request(
                Path.beatmap_scores(beatmap),
                mode=mode,
                **{"mods[]": mods},
                type=ranking_type,
            )
        )

    async def get_beatmap(self, beatmap: int) -> Beatmap:
        """
        Gets beatmap data for the specified beatmap ID.

        Requires OAuth and scope public

        **Parameters**

        beatmap: :class:`int`
            The ID of the beatmap

        **Returns**

        :class:`Beatmap`
            Includes attributes `beatmapset`, `beatmapset.ratings`, `failtimes`, `max_combo`.
        """
        return Beatmap(await self.http.make_request(Path.beatmap(beatmap)))

    async def get_beatmaps(self, ids: Optional[Sequence[int]] = None) -> List[Beatmap]:
        """
        Returns list of beatmaps.

        Requires OAuth and scope public

        **Parameters**

        ids: Optional[List[:class:`int`]]
            Beatmap id to be returned. Specify once for each beatmap id requested.
            Up to 50 beatmaps can be requested at once.

        **Returns**

        List[:class:`Beatmap`]
            Includes attributes `beatmapset`, `beatmapset.ratings`, `failtimes`, `max_combo`.
        """
        results = await self.http.make_request(Path.beatmaps(), **{"ids[]": list(ids)})
        return list(map(Beatmap, results["beatmaps"])) if results else []

    async def get_beatmap_attributes(
        self,
        beatmap: int,
        mods: Optional[Union[int, Mods, Sequence[Union[str, Mods, int]]]] = None,
        ruleset: Optional[Union[str, GameModeStr]] = None,
        ruleset_id: Optional[Union[int, GameModeInt]] = None,
    ) -> BeatmapDifficultyAttributes:
        """
        Returns difficulty attributes of beatmap with specific mode and mods combination.

        Requires OAuth and scope public

        **Parameters**

        beatmap: :class:`int`
            Beatmap id.

        mods: Optional[Union[:class:`int`, Sequence[Union[:class:`str`, :class:`Mods`, :class:`int`]], :class:`Mods`]]
            Mod combination. Can be either a bitset of mods, a Mods enum, or array of any. Defaults to no mods.
            Some mods may cause the api to throw an HTTP 422 error depending on the map's gamemode.

        ruleset: Optional[Union[:class:`GameModeStr`, :class:`str`]]
            Ruleset of the difficulty attributes. Only valid if it's the beatmap ruleset or the beatmap can be
            converted to the specified ruleset. Defaults to ruleset of the specified beatmap.

        ruleset_id: Optional[Union[:class:`GameModeInt`, :class:`int`]]
            The same as `ruleset` but in integer form.

        **Returns**

        :class:`BeatmapDifficultyAttributes`
        """
        ruleset, ruleset_id = parse_enum_args(ruleset, ruleset_id)
        return BeatmapDifficultyAttributes(
            await self.http.make_request(
                Path.get_beatmap_attributes(beatmap),
                mods=parse_mods_arg(mods),
                ruleset=ruleset,
                ruleset_id=ruleset_id,
            )
        )

    async def get_beatmapset(self, beatmapset_id: int) -> Beatmapset:
        """
        Get beatmapset by id.

        Requires OAuth and scope public

        **Parameters**

        beatmapset_id: :class:`int`

        **Returns**

        :class:`Beatmapset`
        """
        return Beatmapset(await self.http.make_request(Path.get_beatmapset(beatmapset_id)))

    async def get_beatmapset_discussion_posts(
        self,
        beatmapset_discussion_id: Optional[int] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        sort: Optional[str] = None,
        types: Optional[Sequence[str]] = None,
        user: Optional[int] = None,
        with_deleted: Optional[str] = None,
        cursor: Optional[Dict[str, int]] = None,
    ) -> BeatmapsetDiscussionPostsResult:
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
            `id_desc` for newest first; `id_asc` for oldest first. Defaults to `id_desc`

        type: Optional[Sequence[:class:`str`]]
            `first`, `reply`, `system` are the valid values. Defaults to `reply`.

        user: Optional[:class:`int`]
            The id of the user

        with_deleted: Optional[:class:`str`]
            This param has no effect as api calls do not currently receive group permissions.

        cursor: Optional[Dict[:class:`str`, :class:`int`]]
            A cursor object received from a previous call to get_beatmapset_discussion_posts
            (:class:`BeatmapsetDiscussionPostsResult`.cursor)

        **Returns**

        :class:`BeatmapsetDiscussionsPostsResult`
        """
        if cursor is None:
            cursor = {}
        if "page" in cursor:
            page = cursor["page"]
        if "limit" in cursor:
            limit = cursor["limit"]
        resp = await self.http.make_request(
            Path.beatmapset_discussion_posts(),
            beatmapset_discussion_id=beatmapset_discussion_id,
            limit=limit,
            page=page,
            sort=sort,
            user=user,
            with_deleted=with_deleted,
            **{"types[]": types},
        )
        return BeatmapsetDiscussionPostsResult(
            list(map(BeatmapsetCompact, resp["beatmapsets"])),
            list(map(BeatmapsetDiscussionPost, resp["posts"])),
            list(map(UserCompact, resp["users"])),
            resp["cursor_string"],
        )

    async def get_beatmapset_discussion_votes(
        self,
        beatmapset_discussion_id: Optional[int] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        receiver: Optional[int] = None,
        score: Optional[int] = None,
        sort: Optional[str] = None,
        user: Optional[int] = None,
        with_deleted: Optional[str] = None,
        cursor: Optional[Dict[str, int]] = None,
    ) -> BeatmapsetDiscussionVotesResult:
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
            `id_desc` for newest first; `id_asc` for oldest first. Defaults to `id_desc`

        user: Optional[:class:`int`]
            The id of the User giving the votes.

        with_deleted: Optional[:class:`str`]
            This param has no effect as api calls do not currently receive group permissions

        cursor: Optional[Dict[:class:`str`, :class:`int`]]
            A cursor object received from a previous call to get_beatmapset_discussion_votes
            (:class:`BeatmapsetDiscussionVotesResult`.cursor)

        **Returns**

        :class:`BeatmapsetDiscussionVotesResult`
        """
        if cursor is None:
            cursor = {}
        if "page" in cursor:
            page = cursor["page"]
        if "limit" in cursor:
            limit = cursor["limit"]
        resp = await self.http.make_request(
            Path.beatmapset_discussion_votes(),
            beatmapset_discussion_id=beatmapset_discussion_id,
            limit=limit,
            receiver=receiver,
            score=score,
            page=page,
            sort=sort,
            user=user,
            with_deleted=with_deleted,
        )
        return BeatmapsetDiscussionVotesResult(
            list(map(BeatmapsetDiscussion, resp["discussions"])),
            list(map(BeatmapsetDiscussionVote, resp["votes"])),
            list(map(UserCompact, resp["users"])),
            resp["cursor"],
        )

    async def get_beatmapset_discussions(
        self,
        beatmap_id: Optional[int] = None,
        beatmapset_id: Optional[int] = None,
        beatmapset_status: Optional[str] = None,
        limit: Optional[int] = None,
        message_types: Optional[Sequence[Union[str, MessageType]]] = None,
        only_unresolved: Optional[bool] = None,
        page: Optional[int] = None,
        sort: Optional[str] = None,
        user: Optional[int] = None,
        with_deleted: Optional[str] = None,
        cursor: Optional[Dict[str, int]] = None,
    ) -> BeatmapsetDiscussionsResult:
        """
        Returns a list of beatmapset discussions

        Requires OAuth and scope public

        **Parameters**

        beatmap_id: Optional[:class:`int`]
            id of the beatmap

        beatmapset_id: Optional[:class:`int`]
            id of the beatmapset

        beatmapset_status: Optional[:class:`str`]
            One of `all`, `ranked`, `qualified`, `disqualified`, `never_qualified`. Defaults to `all`.

        limit: Optional[:class:`int`]
            Maximum number of results.

        message_types: Optional[Sequence[Union[:class:`str`, :class:`MessageType`]]]
            None defaults to all types.

        only_unresolved: Optional[:class:`bool`]
            true to show only unresolved issues; false, otherwise. Defaults to false.

        page: Optional[:class:`int`]
            Search result page.

        sort: Optional[:class:`str`]
            `id_desc` for newest first; `id_asc` for oldest first. Defaults to `id_desc`.

        user: Optional[:class:`int`]
            The id of the User.

        with_deleted: Optional[:class:`str`]
            This param has no effect as api calls do not currently receive group permissions.

        cursor: Optional[Dict[:class:`str`, :class:`int`]]
            A cursor object received from a previous call to get_beatmapset_discussions
            (:class:`BeatmapsetDiscussionsResult`.cursor)

        **Returns**

        :class:`BeatmapsetDiscussionsResult`
        """
        if cursor is None:
            cursor = {}
        if "page" in cursor:
            page = cursor["page"]
        if "limit" in cursor:
            limit = cursor["limit"]
        params = {}
        if message_types is not None:
            message_types = list(map(lambda t: t.value if isinstance(t, MessageType) else t, message_types))
            params = {"message_types[]": message_types}
        resp = await self.http.make_request(
            Path.beatmapset_discussions(),
            beatmap_id=beatmap_id,
            beatmapset_id=beatmapset_id,
            beatmapset_status=beatmapset_status,
            limit=limit,
            only_unresolved=only_unresolved,
            page=page,
            sort=sort,
            user=user,
            with_deleted=with_deleted,
            **params,
        )
        return BeatmapsetDiscussionsResult(
            list(map(Beatmap, resp["beatmaps"])),
            list(map(BeatmapsetDiscussion, resp["discussions"])),
            list(map(BeatmapsetDiscussion, resp["included_discussions"])),
            list(map(UserCompact, resp["users"])),
            ReviewsConfig(resp["reviews_config"]),
            resp["cursor"],
        )

    async def get_changelog_build(self, stream: str, build: str) -> Build:
        """
        Returns details of the specified build.

        **Parameters**

        stream: :class:`str`
            Update stream name.

        build: :class:`str`
            Build version.

        **Returns**

        A :class:`Build` with `changelog_entries`, `changelog_entries.github_user`, and `versions` included.
        """
        return Build(await self.http.make_request(Path.get_changelog_build(stream, build)))

    async def get_changelog_listing(
        self,
        start: Optional[str] = None,
        max_id: Optional[int] = None,
        stream: Optional[str] = None,
        end: Optional[str] = None,
        message_formats: Optional[Sequence[str]] = None,
    ) -> ChangelogListingResult:
        """
        Returns a listing of update streams, builds, and changelog entries.

        **Parameters**

        start: Optional[:class:`str`]
            Minimum build version.

        max_id: Optional[:class:`int`]
            Maximum build ID.

        stream: Optional[:class:`str`]
            Stream name to return builds from.

        end: Optional[:class:`str`]
            Maximum build version.

        message_formats: Optional[Sequence[:class:`str`]]
            `html`, `markdown`. Default to both.

        **Returns**

        :class:`ChangelogListingResult`
        """
        response = await self.http.make_request(
            Path.get_changelog_listing(),
            max_id=max_id,
            stream=stream,
            to=end,
            **{"from": start, "message_formats[]": message_formats},
        )
        return ChangelogListingResult(
            list(map(Build, response["builds"])),
            list(map(UpdateStream, response["streams"])),
            ChangelogListingSearch(
                response["search"]["from"],
                response["search"]["to"],
                response["search"]["limit"],
                response["search"]["max_id"],
                response["search"]["stream"],
            ),
        )

    async def lookup_changelog_build(
        self,
        changelog: str,
        key: Optional[str] = None,
        message_formats: Optional[Sequence[str]] = None,
    ) -> Build:
        """
        Returns details of the specified build.

        **Parameters**

        changelog: :class:`str`
            Build version, update stream name, or build ID.

        key: Optional[:class:`str`]
            Leave blank to query by build version or stream name, or `id` to query by build ID.

        message_formats: Optional[Sequence[:class:`str`]]
            `html`, `markdown`. Default to both.

        **Returns**

        A :class:`Build` with changelog_entries, changelog_entries.github_user, and versions included.
        """
        return Build(
            await self.http.make_request(
                Path.lookup_changelog_build(changelog), key=key, **{"message_formats[]": message_formats}
            )
        )

    async def create_new_pm(
        self, target_id: int, message: str, is_action: bool, uuid: Optional[str] = None
    ) -> CreateNewPmResult:
        """
        This endpoint allows you to create a new PM channel.

        Requires OAuth, scope chat.write, and a user (authorization code grant, delegate scope)

        **Parameters**

        target_id: :class:`int`
            user_id of user to start PM with

        message: :class:`str`
            message to send

        is_action: :class:`bool`
            whether the message is an action

        uuid: Optional[:class:`str`]
            client-side message identifier which will be sent back in response and websocket json.

        **Returns**

        :class:`CreateNewPmResult`
        """
        data = {"target_id": target_id, "message": message, "is_action": is_action}
        if uuid is not None:
            data["uuid"] = uuid
        resp = await self.http.make_request(Path.create_new_pm(), files=create_multipart_formdata(data))
        return CreateNewPmResult(
            ChatChannel(resp["channel"]),
            ChatMessage(resp["message"]),
            resp["new_channel_id"],
        )

    async def get_comments(
        self,
        commentable_type: Optional[Union[ObjectType, str]] = None,
        commentable_id: Optional[int] = None,
        cursor: Optional[dict] = None,
        parent_id: Optional[int] = None,
        sort: Optional[Union[str, CommentSort]] = None,
    ) -> CommentBundle:
        """
        Returns a list comments and their replies up to 2 levels deep.

        Does not require OAuth

        **Parameter**

        commentable_type: Optional[Union[:class:`ObjectType`, :class:`str`]
            The type of resource to get comments for. Must be of the following types:
            beatmapset, build, news_post

        commentable_id: Optional[:class:`int`]
            The id of the resource to get comments for. Id correlates with commentable_type.

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
        commentable_type, sort = parse_enum_args(commentable_type, sort)
        if commentable_type is not None and commentable_type not in (
            "beatmapset",
            "build",
            "news_post",
        ):
            raise ValueError("commentable_type, if not null, must be of the following: beatmapset, build, new_post")
        return CommentBundle(
            await self.http.make_request(
                Path.get_comments(),
                commentable_type=commentable_type,
                commentable_id=commentable_id,
                parent_id=parent_id,
                sort=sort,
                **(cursor if cursor else {}),
            )
        )

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
        return CommentBundle(await self.http.make_request(Path.get_comment(comment)))

    async def reply_topic(self, topic: int, body: str) -> ForumPost:
        """
        Create a post replying to the specified topic.

        Requires OAuth, scope forum.write, and a user (authorization code grant, delegate scope)

        **Parameters**

        topic: :class:`int`
            Id of the topic to be replied to.

        body: :class:`str`
            Content of the reply post.

        **Returns**

        :class:`ForumPost`
            body attributes included
        """
        data = {"body": body}
        return ForumPost(await self.http.make_request(Path.reply_topic(topic), files=create_multipart_formdata(data)))

    async def create_topic(
        self,
        body: str,
        forum_id: int,
        title: str,
        with_poll: Optional[bool] = None,
        hide_results: Optional[bool] = None,
        length_days: Optional[int] = None,
        max_options: Optional[int] = None,
        poll_options: Optional[str] = None,
        poll_title: Optional[str] = None,
        vote_change: Optional[bool] = None,
    ) -> CreateTopicResult:
        """
        Create a new topic.

        Requires OAuth, scope forum.write, and a user (authorization code grant, delegate scope)

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

        :class:`CreateTopicResult`
        """
        data = {
            "body": body,
            "forum_id": forum_id,
            "title": title,
            "with_poll": with_poll,
        }
        if with_poll:
            if poll_options is None or poll_title is None:
                raise TypeError("poll_options and poll_title are required since the topic has a poll.")
            data.update(
                {
                    "forum_topic_poll[hide_results]": hide_results,
                    "forum_topic_poll[length_days]": length_days,
                    "forum_topic_poll[max_options]": max_options,
                    "forum_topic_poll[poll_options]": poll_options,
                    "forum_topic_poll[poll_title]": poll_title,
                    "forum_topic_poll[vote_change]": vote_change,
                }
            )
        resp = await self.http.make_request(Path.create_topic(), files=create_multipart_formdata(data))
        return CreateTopicResult(ForumTopic(resp["topic"]), ForumPost(resp["post"]))

    async def get_topic_and_posts(
        self,
        topic: int,
        cursor: Optional[str] = None,
        sort: Optional[str] = None,
        limit: Optional[int] = None,
        start: Optional[int] = None,
        end: Optional[int] = None,
    ) -> GetTopicAndPostsResult:
        """
        Get topic and its posts.

        Requires OAuth and scope public

        **Parameters**

        topic: :class:`int`
            Id of the topic.

        cursor: Optional[:class:`str`]
            Parameter for pagination.

        sort: Optional[:class:`str`]
            Post sorting option. Valid values are id_asc (default) and id_desc.

        limit: Optional[:class:`int`]
            Maximum number of posts to be returned (20 default, 50 at most).

        start: Optional[:class:`int`]
            First post id to be returned with sort set to id_asc.
            This parameter is ignored if cursor_string is specified.

        end: Optional[:class:`int`]
            First post id to be returned with sort set to id_desc.
            This parameter is ignored if cursor_string is specified.

        **Returns**

        :class:`GetTopicAndPostsResult`
        """
        resp = await self.http.make_request(
            Path.get_topic_and_posts(topic),
            **(cursor if cursor else {}),
            sort=sort,
            limit=limit,
            start=start,
            end=end,
        )
        return GetTopicAndPostsResult(
            resp["cursor_string"],
            resp["search"],
            ForumTopic(resp["topic"]),
            list(map(ForumPost, resp["posts"])),
        )

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
        data = {"forum_topic[topic_title]": topic_title}
        return ForumTopic(await self.http.make_request(Path.edit_topic(topic), files=create_multipart_formdata(data)))

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
        data = {"body": body}
        return ForumPost(await self.http.make_request(Path.edit_post(post), files=create_multipart_formdata(data)))

    async def search(
        self,
        mode: Optional[Union[str, WikiSearchMode]] = None,
        query: Optional[str] = None,
        page: Optional[int] = None,
    ) -> SearchResult:
        """
        Searches users and wiki pages.

        Requires OAuth and scope public

        **Parameters**

        mode: Optional[Union[:class:`str`, :class:`WikiSearchMode`]]
            Either all, user, or wiki_page. Default is all.

        query: Optional[:class:`str`]
            Search keyword.

        page: Optional[:class:`int`]
            Search result page. Ignored for mode all.

        **Returns**

        :class:`SearchResult`
        """
        mode = parse_enum_args(mode)
        resp = await self.http.make_request(Path.search(), mode=mode, query=query, page=page)
        return SearchResult(
            get_optional_list(resp.get("user", {}), "data", UserCompact),
            get_optional_list(resp.get("wiki_page", {}), "data", WikiPage),
        )

    async def get_scores(
        self,
        room: int,
        playlist: int,
        limit: Optional[int] = None,
        sort: Optional[Union[str, MultiplayerScoresSort]] = None,
        cursor: Optional[str] = None,
    ) -> MultiplayerScores:
        """
        Requires OAuth, scope public, and a user (authorization code grant, delegate scope)

        **Parameters**

        room: :class:`int`
            Id of the room.

        playlist: :class:`int`
            Id of the playlist item.

        limit: Optional[:class:`int`]
            Number of scores to be returned.

        sort: Optional[Union[:class:`str`, :class:`MultiplayerScoresSort`]]

        cursor: Optional[:class:`str`]
            :class:`MultiplayerScores`.cursor value from a previous call to get next page.

        **Returns**

        :class:`MultiplayerScores`
        """
        sort = parse_enum_args(sort)
        return MultiplayerScores(
            await self.http.make_request(
                Path.get_scores(room, playlist),
                limit=limit,
                sort=sort,
                cursor_string=cursor,
            )
        )

    async def get_news_listing(
        self,
        limit: Optional[int] = None,
        year: Optional[int] = None,
        cursor: Optional[dict] = None,
    ) -> GetNewsListingResult:
        """
        Returns a list of news posts and related metadata.

        **Parameters**

        limit: Optional[:class:`int`]
            Maximum number of posts (12 default, 1 minimum, 21 maximum).

        year: Optional[:class:`int`]
            Year to return posts from.

        cursor: Optional[:class:`str`]
            Cursor for pagination.

        **Returns**

        :class:`GetNewsListingResult`
        """
        resp = await self.http.make_request(Path.get_news_listing(), limit=limit, year=year, cursor=cursor)
        return GetNewsListingResult(
            resp["cursor_string"],
            list(map(NewsPost, resp["news_posts"])),
            NewsSidebar(
                resp["news_sidebar"]["current_year"],
                list(map(NewsPost, resp["news_sidebar"]["news_posts"])),
                resp["news_sidebar"]["years"],
            ),
            SearchInfo(resp["search"]["sort"], resp["search"]["limit"], None, None),
        )

    async def get_news_post(self, news: str, key: Optional[str] = None) -> NewsPost:
        """
        Returns details of the specified news post.

        **Parameters**

        news: class:`str`
            News post slug or ID.

        key: Optional[:class:`str`]
            Unset to query by slug, or `id` to query by ID.

        **Returns**

        Returns a :class:`NewsPost` with content and navigation included.
        """
        return NewsPost(await self.http.make_request(Path.get_news_post(news), key=key))

    async def revoke_current_token(self) -> None:
        """
        Revokes currently authenticated token.

        Requires OAuth
        """
        await self.http.make_request(Path.revoke_current_token())

    async def get_ranking(
        self,
        mode: Union[str, GameModeStr],
        type: Union[str, RankingType],
        country: Optional[str] = None,
        cursor: Optional[dict] = None,
        filter: Optional[str] = None,
        spotlight: Optional[int] = None,
        variant: Optional[str] = None,
    ) -> Rankings:
        """
        Gets the current ranking for the specified type and game mode.

        Requires OAuth and scope public

        mode: Union[:class:`str`, :class:`GameModeStr`]

        type: Union[:class:`str`, :class:`RankingType`]
            :class:`RankingType`

        country: Optional[:class:`str`]
            Filter ranking by country code. Only available for `type` of `performance`.

        cursor: Optional[:class:`dict`]

        filter: Optional[:class:`str`]
            Either `all` (default) or `friends`.

        spotlight: Optional[:class:`int`]
            The id of the spotlight if `type` is `charts`.
            Ranking for latest spotlight will be returned if not specified.

        variant: Optional[:class:`str`]
            Filter ranking to specified mode variant.
            For `mode` of `mania`, it's either `4k` or `7k`. Only available for `type` of `performance`.

        **Returns**

        :class:`Rankings`
        """
        mode, type = parse_enum_args(mode, type)
        return Rankings(
            await self.http.make_request(
                Path.get_ranking(mode, type),
                country=country,
                **(cursor if cursor else {}),
                filter=filter,
                spotlight=spotlight,
                variant=variant,
            )
        )

    async def get_spotlights(self) -> Spotlights:
        """
        Gets the list of spotlights.

        Requires OAuth and scope public

        **Returns**

        :class:`Spotlights`
        """
        return Spotlights(await self.http.make_request(Path.get_spotlights()))

    async def get_own_data(self, mode: Union[str, GameModeStr] = "") -> User:
        """
        Similar to get_user but with authenticated user (token owner) as user id.

        Requires OAuth, scope identify, and a user (authorization code grant, delegate scope)

        **Parameters**

        mode: Optional[:class:`str`, :class:`GameModeStr`]
            GameMode. User default mode will be used if not specified.

        **Returns**

        See return for get_user
        """
        mode = parse_enum_args(mode)
        return User(await self.http.make_request(Path.get_own_data(mode)))

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
        return list(
            map(
                KudosuHistory,
                await self.http.make_request(Path.get_user_kudosu(user), limit=limit, offset=offset),
            )
        )

    async def get_user_scores(
        self,
        user: int,
        type: Union[UserScoreType, str],
        include_fails: Optional[bool] = False,
        mode: Optional[Union[str, GameModeStr]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[Union[LegacyScore, SoloScore]]:
        """
        This endpoint returns the scores of specified user.

        Requires OAuth and scope public

        **Parameters**

        user: :class:`int`
            Id of the user.

        type: Union[:class:`UserScoreType` :class:`str`]
            Score type. Must be one of `best`, `firsts`, `recent`, `pinned`

        include_fails: Optional[:class:`bool`]
            Only for recent scores, include scores of failed plays. Defaults to False.

        mode: Optional[Union[:class:`GameModeStr`, :class:`str`]]
            game mode of the scores to be returned. Defaults to the specified user's mode.

        limit: Optional[:class:`int`]
            Maximum number of results.

        offset: Optional[:class:`int`]
            Result offset for pagination.

        **Returns**

        Sequence[Union[:class:`LegacyScore`, :class:`SoloScore`]]
            Includes attributes `beatmap`, `beatmapset`. Additionally includes `weight` if `type` is `best`.
        """
        mode, type = parse_enum_args(mode, type)
        return list(
            map(
                get_score_object,
                await self.http.make_request(
                    Path.get_user_scores(user, type),
                    include_fails=int(include_fails),
                    mode=mode,
                    limit=limit,
                    offset=offset,
                ),
            )
        )

    async def get_user_beatmaps(
        self,
        user: int,
        type: Union[str, UserBeatmapType],
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[Union[BeatmapPlaycount, Beatmapset]]:
        """
        Returns the beatmaps of specified user.

        Requires OAuth and scope public

        **Parameters**

        user: :class:`int`
            Id of the user.

        type: Union[:class:`str`, :class:`UserBeatmapType`]
            Beatmap type. Can be one of `favourite`, `graveyard`, `loved`, `most_played`, `pending`, `ranked`.

        limit: Optional[:class:`int`]
            Maximum number of results.

        offset: Optional[:class:`int`]
            Result offset for pagination.

        **Returns**

        List[Union[:class:`BeatmapPlaycount`, :class:`Beatmapset`]]
            :class:`BeatmapPlaycount` for `type` `most_played` and :class:`Beatmapset` for any other type.
        """
        type = parse_enum_args(type)
        return list(
            map(
                BeatmapPlaycount if type == "most_played" else Beatmapset,
                await self.http.make_request(Path.get_user_beatmaps(user, type), limit=limit, offset=offset),
            )
        )

    async def get_user_recent_activity(
        self, user: int, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> List[EVENT_TYPE]:
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

        List[:class:`Event`]
            list of :class:`Event` objects
        """
        return list(
            map(
                get_event_object,
                await self.http.make_request(Path.get_user_recent_activity(user), limit=limit, offset=offset),
            )
        )

    async def get_user(
        self,
        user: int,
        mode: Optional[Union[str, GameModeStr]] = "",
        key: Optional[str] = None,
    ) -> User:
        """
        This endpoint returns the detail of specified user.

        NOTE: It's highly recommended to pass key parameter
        to avoid getting unexpected result (mainly when
        looking up user with numeric username or nonexistent user id).

        Requires OAuth and scope public

        **Parameters**

        user: Union[:class:`int`, :class:`str`]
            Id or username of the user. Id lookup is prioritised unless key parameter is specified.
            Previous usernames are also checked in some cases.

        mode: Optional[Union[:class:`str`, :class:`GameModeStr`]
            User default mode will be used if not specified.

        key: Optional[:class:`str`]
            **DEPRECATED**
            It's recommended to prefix usernames with @ instead of setting key

            Type of user passed in url parameter. Can be either `id` or `username`
            to limit lookup by their respective type. Passing empty or invalid
            value will result in id lookup followed by username lookup if not found.

        **Returns**

        :class:`User`
            Includes attributes `account_history`, `active_tournament_banner`, `badges`,
            `beatmap_playcounts_count`, `favourite_beatmapset_count`, `follower_count`,
            `graveyard_beatmapset_count`, `groups`, `loved_beatmapset_count`, `mapping_follower_count`,
            `monthly_playcounts`, `page`, `pending_beatmapset_count`, `previous_usernames`,
            `rank_highest`, `rank_history`, `ranked_beatmapset_count`, `replays_watched_counts`,
            `scores_best_count`, `scores_first_count`, `scores_recent_count`, `statistics`,
            `statistics.country_rank`, `statistics.rank`, `statistics.variants`, `support_level`,
            `user_achievements`.
        """
        mode = parse_enum_args(mode)
        user = f"@{user}" if key is not None and key.lower() == "username" else user
        return User(await self.http.make_request(Path.get_user(user, mode)))

    async def get_users(self, ids: Sequence[int]) -> List[UserCompact]:
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
        res = await self.http.make_request(Path.get_users(), **{"ids[]": ids})
        return list(map(UserCompact, res["users"]))

    async def lookup_users(self, users: list[int, str]):
        """
        Lookup users by a mix of user ids and usernames.
        Can lookup maximum 50 at a time.

        ids: Sequence[Union[:class:`int`, :class:`str`]]
            Can be a list of user ids and usernames.
            Usernames should be prefixed with "@" to make sure they're interpreted as usernames by the api.

        **Returns**

        Sequence[:class:`UserCompact`]
        """
        res = await self.http.make_request(Path.lookup_users(), **{"ids[]": users})
        return list(map(UserCompact, res["users"]))

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
        return WikiPage(await self.http.make_request(Path.get_wiki_page(locale, path)))

    async def get_beatmapset_events(
        self,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, BeatmapsetEventSort]] = None,
        type: Optional[Union[str, BeatmapsetEventType]] = None,
        min_date: Optional[Union[str, datetime]] = None,
        max_date: Optional[Union[str, datetime]] = None,
    ) -> GetBeatmapsetEventsResult:
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

        :class:`GetBeatmapsetEventsResult`
        """
        sort, type = parse_enum_args(sort, type)
        if isinstance(min_date, datetime):
            min_date = min_date.isoformat()
        if isinstance(max_date, datetime):
            max_date = max_date.isoformat()
        resp = await self.http.make_request(
            Path.get_beatmapset_events(),
            page=page,
            limit=limit,
            sort=sort,
            type=type,
            min_date=min_date,
            max_date=max_date,
        )
        return GetBeatmapsetEventsResult(
            list(map(BeatmapsetEvent, resp["events"])),
            Review(resp["reviewsConfig"]),
            list(map(UserCompact, resp["users"])),
        )

    async def get_matches(
        self, limit: Optional[int] = None, sort: Optional[Union[str, MatchSort]] = None, cursor: Optional[Dict] = None
    ) -> GetMatchesResult:
        """
        Returns a list of matches.

        Requires OAuth and scope public.

        **Parameters**

        limit: Optional[:class:`int`]

        sort: Optional[Union[:class:`str`, :class:`MatchSort`]]

        cursor: Optional[Dict]
            Dictionary containing one key: `match_id`.
            Can be obtained from a previous call to this function or manually created.

        **Returns**

        :class:`GetMatchesResult`
        """
        match_id = cursor.get("match_id") if cursor is not None else None
        sort = parse_enum_args(sort)
        resp = await self.http.make_request(
            Path.get_matches(), limit=limit, sort=sort, **{"cursor[match_id]": match_id}
        )
        return GetMatchesResult(list(map(Match, resp["matches"])), resp["params"], resp["cursor"])

    async def get_match(self, match_id: int) -> MatchExtended:
        """
        Returns a match by id.

        Requires OAuth and scope public.

        **Parameters**

        match_id: :class:`int`
            The match id.

        **Returns**

        :class:`Match`
        """
        return MatchExtended(await self.http.make_request(Path.get_match(match_id)))

    async def get_rooms(
        self,
        mode: Union[str, GameModeStr] = "",
        sort: Optional[Union[str, RoomSort]] = None,
        limit: Optional[int] = None,
        room_type: Optional[Union[RoomType, str]] = None,
        category: Optional[Union[RoomCategory, str]] = None,
        filter_mode: Optional[Union[RoomFilterMode, str]] = None,
    ) -> List[Room]:
        """
        Returns a list of rooms.

        Requires OAuth, scope public, and a user (authorization code grant, delegate scope).

        **Parameters**

        mode: Optional[Union[:class:`str`, :class:`GameModeStr`]]
            Game mode to filter rooms by.

        sort: Optional[Union[:class:`str`, :class:`RoomSort`]]
            Sort rooms by.

        limit: Optional[:class:`int`]
            max number of rooms to return

        room_type: Optional[Union[:class:`RoomType`, :class:`str`]]
            type of room to look for

        category: Optional[Union[:class:`RoomCategory`, :class:`str`]]
            type of category of room to look for

        filter_mode: Optional[Union[:class:`RoomFilterMode`, :class:`str`]]
        """
        mode, sort, room_type, category, filter_mode = parse_enum_args(mode, sort, room_type, category, filter_mode)
        return list(
            map(
                Room,
                await self.http.make_request(
                    Path.get_rooms(mode),
                    sort=sort,
                    limit=limit,
                    type_group=room_type,
                    category=category,
                    mode=filter_mode,
                ),
            )
        )

    async def get_seasonal_backgrounds(self) -> SeasonalBackgrounds:
        """
        Get the season backgrounds.

        Doesn't require OAuth

        **Returns**

        :class:`SeasonalBackgrounds`
        """
        return SeasonalBackgrounds(await self.http.make_request(Path.get_seasonal_backgrounds()))

    async def get_room(self, room_id: int) -> Room:
        """
        Returns a room by id.

        Requires OAuth and scope public.

        **Parameters**

        room_id: :class:`int`
            The room id.

        **Returns**

        :class:`Room`
        """
        return Room(await self.http.make_request(Path.get_room(room_id)))

    async def get_score_by_id(self, mode: Union[str, GameModeStr], score_id) -> Union[LegacyScore, SoloScore]:
        """
        Returns a score by id.

        Requires OAuth and scope public.

        **Parameters**

        mode: Union[:class:`str`, :class:`GameModeStr`]

        score_id: :class:`int`

        **Returns**

        Union[:class:`SoloScore`, :class:`LegacyScore`]
            Should be a SoloScore, unless for some strange reason it's not
        """
        mode = parse_enum_args(mode)
        return get_score_object(await self.http.make_request(Path.get_score_by_id(mode, score_id)))

    async def get_score_by_id_only(self, score_id: int) -> Union[LegacyScore, SoloScore]:
        """
        Returns a score by id, not requiring a mode.

        Requires OAuth and scope public.

        **Parameters**

        score_id: :class:`int`

        **Returns**

        Union[:class:`SoloScore`, :class:`LegacyScore`]
            Should be a SoloScore, unless for some strange reason it's not
        """
        return get_score_object(await self.http.make_request(Path.get_score_by_id_only(score_id)))

    async def search_beatmapsets(
        self, filters: Optional[BeatmapsetSearchFilter] = None, page: Optional[int] = None
    ) -> BeatmapsetSearchResult:
        """
        Search for beatmapsets.

        Requires OAuth and scope public.

        **Attributes**

        filters: Optional[:class:`BeatmapsetSearchFilter`]

        page: Optional[:class:`int`]

        **Returns**

        :class:`BeatmapsetSearchResult`
        """
        if filters is None:
            filters = {}
        if isinstance(filters, BeatmapsetSearchFilter):
            filters = filters.filters
        resp = await self.http.make_request(Path.beatmapset_search(), page=page, **filters)
        return BeatmapsetSearchResult(
            list(map(Beatmapset, resp["beatmapsets"])),
            resp["cursor"],
            resp["search"],
            resp["recommended_difficulty"],
            resp["error"],
            resp["total"],
        )

    async def get_room_leaderboard(self, room_id: int) -> GetRoomLeaderboardResult:
        """
        Return a room's leaderboard. The :class:`UserScoreAggregate` objects returned under the "leaderboard"
        key contain the "user" attribute. The :class:`UserScoreAggregate` object under the "user_score" key
        contains the "user" and "position" attributes.

        Requires OAuth, scope public, and a user (authorization code grant, delegate scope).

        **Parameters**

        room_id: :class:`int`

        **Returns**

        :class:`GetRoomLeaderboard`
        """
        resp = await self.http.make_request(Path.get_room_leaderboard(room_id))
        return GetRoomLeaderboardResult(
            list(map(UserScoreAggregate, resp["leaderboard"])), get_optional(resp, "user_score", UserScoreAggregate)
        )

    async def get_replay_data(
        self, mode: Optional[Union[GameModeStr, str]], score_id: int, use_osrparse: bool = True
    ) -> Union["osrparse.Replay", bytes]:
        """
        Returns replay data for a score.

        Requires OAuth, scope public, and a user (authorization code grant, delegate scope).

        Requires osu.py is installed with the 'replay' feature

        **Parameters**

        mode: Optional[Union[:class:`str`, :class:`GameModeStr`]]

        score_id: :class:`int`

        use_osrparse: :class:`bool`
            If true, returns an :class:`osrparse.Replay` object. Defaults to true.

        **Returns**

        Union[:class:`osrparse.Replay`, :class:`bytes`]
        """
        if mode is None:
            return await self.get_replay_data_by_id_only(score_id, use_osrparse=use_osrparse)

        if not has_osrparse and use_osrparse:
            raise RuntimeError(
                "osrparse is required to call get_replay_data. "
                "Install osu.py with the 'replay' feature to use this function."
            )

        mode = parse_enum_args(mode)
        gen = self.http.get_req_gen(Path.get_replay_data(mode, score_id))
        async for resp in gen:  # at most one resp, but shouldn't be zero here
            data = await resp.read()
            return osrparse.Replay.from_string(data) if use_osrparse else data

    async def get_replay_data_by_id_only(
        self, score_id: int, use_osrparse: bool = True
    ) -> Union["osrparse.Replay", bytes]:
        """
        Returns replay data for a score. Use :func:`AsynchronousClient.get_replay_data` for score ids that require
        specifying the game mode too.

        Requires OAuth, scope public, and a user (authorization code grant, delegate scope).

        Requires osu.py is installed with the 'replay' feature if use_osrparse is true.

        **Parameters**

        score_id: :class:`int`

        use_osrparse: :class:`bool`
            If true, returns an :class:`osrparse.Replay` object. Defaults to true.

        **Returns**

        Union[:class:`osrparse.Replay`, :class:`bytes`]
        """
        if not has_osrparse and use_osrparse:
            raise RuntimeError(
                "osrparse is required to call get_replay_data. "
                "Install osu.py with the 'replay' feature to use this function."
            )

        gen = self.http.get_req_gen(Path.get_replay_data_by_id_only(score_id))
        async for resp in gen:  # at most one resp, but shouldn't be zero here
            data = await resp.read()
            return osrparse.Replay.from_string(data) if use_osrparse else data

    async def get_friends(self) -> List[UserCompact]:
        """
        Returns a list of friends.

        Requires OAuth, scope friends.read, and a user (authorization code grant, delegate scope).

        **Returns**

        List[:class:`UserCompact`]
        """
        return list(map(UserCompact, await self.http.make_request(Path.get_friends())))
