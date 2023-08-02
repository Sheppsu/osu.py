from .http import HTTPHandler
from .objects import *
from .path import Path
from .enums import *
from .auth import AuthHandler, LazerAuthHandler
from .util import (
    parse_mods_arg,
    parse_enum_args,
    BeatmapsetSearchFilter,
    create_multipart_formdata,
    PlaylistItemUtil,
    IdentitiesUtil,
    NotificationsUtil,
    JsonUtil,
    get_optional_list,
)
from .results import *

from typing import Union, Optional, Sequence, Dict, List
from datetime import datetime
from osrparse import Replay
from dateutil import parser
import json


class Client:
    """
    Main object for interacting with osu!api, which uses synchronous requests.
    If you're looking for asynchronous requests, use :class:`AsynchronousClient`.

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

    use_lazer: Optional[:class:`bool`]
        Default is False. This changes which base api endpoint the client will use.

        Uses lazer.ppy.sh when True and osu.ppy.sh when False.

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

    def __init__(
        self,
        auth: Union[AuthHandler, LazerAuthHandler] = None,
        request_wait_time: Optional[float] = 1.0,
        limit_per_minute: Optional[float] = 60.0,
        use_lazer: Optional[bool] = False,
    ):
        self.auth = auth
        self.http = HTTPHandler(self, request_wait_time, limit_per_minute, use_lazer)

    @classmethod
    def from_client_credentials(
        cls,
        client_id: int,
        client_secret: str,
        redirect_url: Optional[str],
        scope: Optional[Scope] = Scope.default(),
        code: Optional[str] = None,
        request_wait_time: Optional[float] = 1.0,
        limit_per_minute: Optional[float] = 60.0,
    ) -> "Client":
        """
        Returns a :class:`Client` object from client id, client secret, redirect uri, and scope.

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

        **Returns**

        :class:`Client`
        """
        auth = AuthHandler(client_id, client_secret, redirect_url, scope)
        auth.get_auth_token(code)
        return cls(auth, request_wait_time, limit_per_minute)

    @classmethod
    def from_osu_credentials(
        cls,
        username: str,
        password: str,
        request_wait_time: Optional[float] = 1.0,
        limit_per_minute: Optional[float] = 60.0,
    ) -> "Client":
        """
        Returns a :class:`Client` object which will make authorize and make requests to
        lazer.ppy.sh

        username: :class:`str`
            osu! username login

        password: :class:`str`
            osu! password login

        request_wait_time: Optional[:class:`float`]
            Read under Client init parameters.

        limit_per_minute: Optional[:class:`float`]
            Read under Client init parameters.
        """
        auth = LazerAuthHandler(username, password)
        auth.get_auth_token()
        return cls(auth, request_wait_time, limit_per_minute, True)

    def lookup_beatmap(
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
        return Beatmap(self.http.make_request(Path.beatmap_lookup(), checksum=checksum, filename=filename, id=id))

    def get_user_beatmap_score(
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
        return BeatmapUserScore(self.http.make_request(Path.user_beatmap_score(beatmap, user), mode=mode, mods=mods))

    def get_user_beatmap_scores(
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
        resp = self.http.make_request(Path.user_beatmap_scores(beatmap, user), mode=mode)
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
                lambda mod: (Mod[mod.name].value if not isinstance(mod, Mod) else mod.value)
                if type(mod) != str
                else mod,
                mods,
            )
        )

    def get_beatmap_scores(
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
            self.http.make_request(
                Path.beatmap_scores(beatmap),
                mode=mode,
                **{"mods[]": mods},
                type=ranking_type,
            )
        )

    def get_lazer_beatmap_scores(
        self,
        beatmap: int,
        mode: Optional[Union[str, GameModeStr]] = None,
        mods: Optional[str] = None,
        type: Optional[str] = None,
    ) -> BeatmapScores:
        """
        Returns the top scores for a beatmap on the lazer client.

        Requires OAuth and scope public

        **Parameters**

        beatmap: :class:`int`
            ID of the beatmap

        mode: Optional[Union[:class:`str`, :class:`GameModeStr`]]
            The game mode to get scores for

        mods: Optional[:class:`str`]
            Must pass one of:
            a :class:`Mods` object,
            a list of string mod abbreviations,
            a list of :class:`Mods` objects,
            a list of :classL`Mod` objects

        type: Optional[:class:`str`]
            Beatmap score ranking type. Currently doesn't do anything.

        **Returns**

        :class:`BeatmapScores`
            :class:`SoloScore` object inside includes "user" and the included user includes "country" and "cover".
        """
        mode = parse_enum_args(mode)
        mods = self._parse_mods_list(mods)
        return BeatmapScores(
            self.http.make_request(Path.lazer_beatmap_scores(beatmap), mode=mode, mods=mods, type=type)
        )

    def get_beatmap(self, beatmap: int) -> Beatmap:
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
        return Beatmap(self.http.make_request(Path.beatmap(beatmap)))

    def get_beatmaps(self, ids: Optional[Sequence[int]] = None) -> List[Beatmap]:
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
        results = self.http.make_request(Path.beatmaps(), **{"ids[]": list(ids)})
        return list(map(Beatmap, results["beatmaps"])) if results else []

    def get_beatmap_attributes(
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
            self.http.make_request(
                Path.get_beatmap_attributes(beatmap),
                mods=parse_mods_arg(mods),
                ruleset=ruleset,
                ruleset_id=ruleset_id,
            )
        )

    def get_beatmapset(self, beatmapset_id: int) -> Beatmapset:
        """
        Get beatmapset by id.

        Requires OAuth and scope public

        **Parameters**

        beatmapset_id: :class:`int`

        **Returns**

        :class:`Beatmapset`
        """
        return Beatmapset(self.http.make_request(Path.get_beatmapset(beatmapset_id)))

    def get_beatmapset_discussion_posts(
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
        resp = self.http.make_request(
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

    def get_beatmapset_discussion_votes(
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
        resp = self.http.make_request(
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

    def get_beatmapset_discussions(
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
        resp = self.http.make_request(
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

    def get_changelog_build(self, stream: str, build: str) -> Build:
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
        return Build(self.http.make_request(Path.get_changelog_build(stream, build)))

    def get_changelog_listing(
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
        response = self.http.make_request(
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

    def lookup_changelog_build(
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
            self.http.make_request(
                Path.lookup_changelog_build(changelog), key=key, **{"message_formats[]": message_formats}
            )
        )

    def chat_acknowledge(
        self, history_since: Optional[int] = None, since: Optional[int] = None
    ) -> Sequence[UserSilence]:
        """
        Send a chat ack.

        Requires OAuth, scope lazer, and a user (authorization code grant, delegate scope, or password auth)

        **Parameters**

        history_since: Optional[:class:`int`]
            :class:`UserSilence` s after the specified id to return.
            This field is preferred and takes precedence over since.

        since: Optional[:class:`int`]
            :class:`UserSilence` s after the specified :class:`ChatMessage`.message_id to return.

        **Returns**

        List[:class:`UserSilence`]
        """
        resp = self.http.make_request(Path.chat_ack(), history_since=history_since, since=since)
        return list(map(UserSilence, resp["silences"]))

    def create_new_pm(
        self, target_id: int, message: str, is_action: bool, uuid: Optional[str] = None
    ) -> CreateNewPmResult:
        """
        This endpoint allows you to create a new PM channel.

        Requires OAuth, scope chat.write, and a user (authorization code grant, delegate scope, or password auth)

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
        resp = self.http.make_request(Path.create_new_pm(), files=create_multipart_formdata(data))
        return CreateNewPmResult(
            ChatChannel(resp["channel"]),
            ChatMessage(resp["message"]),
            resp["new_channel_id"],
        )

    def get_updates(
        self,
        since: int = 0,
        includes: Optional[Sequence[str]] = None,
        history_since: Optional[int] = None,
    ) -> GetUpdatesResult:
        """
        This endpoint returns new messages since the given message_id along with updated channel 'presence' data.

        Requires OAuth, scope lazer, a user (authorization code grant, delegate scope, or password auth)

        **Parameters**

        since: :class:`int`
            Defaults to 0. :class:`UserSilence`s after the specified `ChatMessage.message_id` to return.

        includes: Optional[Sequence[:class:`str`]]
            List of fields from `presence`, `silences` to include in the response. Uses `presences` if not specified.

        history_since: Optional[:class:`int`]
            :class:`UserSilence`s after the specified id to return.
            This field is preferred and takes precedence over `since`.

        **Returns**

        :class:`GetUpdatesResult`
        """
        if includes is None:
            includes = ["presence"]
        resp = self.http.make_request(
            Path.get_updates(),
            since=since,
            history_since=history_since,
            **{"includes[]": includes},
        )
        if resp is None:
            resp = {}
        return GetUpdatesResult(
            get_optional_list(resp, "presence", ChatChannel),
            get_optional_list(resp, "silences", UserSilence),
        )

    def get_channel_messages(
        self,
        channel_id: int,
        limit: Optional[int] = None,
        since: Optional[int] = None,
        until: Optional[int] = None,
    ) -> List[ChatMessage]:
        """
        This endpoint returns the chat messages for a specific channel.
        You may need to first join the channel with :func:`osu.Client.join_channel`.

        Requires OAuth, scope lazer, and a user (authorization code grant, delegate scope, or password auth)

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

        List[:class:`ChatMessage`]
        """
        return list(
            map(
                ChatMessage,
                self.http.make_request(
                    Path.get_channel_messages(channel_id),
                    limit=limit,
                    since=since,
                    until=until,
                ),
            )
        )

    def send_message_to_channel(self, channel_id: int, message: str, is_action: bool) -> ChatMessage:
        """
        This endpoint sends a message to the specified channel.

        Requires OAuth, scope lazer, and a user (authorization code grant, delegate scope, or password auth)

        **Parameters**

        channel: :class:`int`
            The channel_id of the channel to send message to

        message: :class:`str`
            message to send

        is_action: :class:`bool`
            whether the message is an action

        **Returns**

        :class:`ChatMessage`
        """
        data = {"is_action": str(is_action).lower(), "message": message}
        data = create_multipart_formdata(data)
        return ChatMessage(self.http.make_request(Path.send_message_to_channel(channel_id), files=data))

    def join_channel(self, channel: int, user: int) -> ChatChannel:
        """
        This endpoint allows you (or someone else) to join a public channel.

        Requires OAuth, scope lazer, and a user (authorization code grant, delegate scope, or password auth)

        **Parameters**

        channel: :class:`int`
            channel id of channel to join

        user: :class:`int`
            user id of user joining

        **Returns**

        :class:`ChatChannel`
        """
        return ChatChannel(self.http.make_request(Path.join_channel(channel, user)))

    def leave_channel(self, channel: int, user: int) -> None:
        """
        This endpoint allows you (or someone else) to leave a public channel.

        Requires OAuth, scope lazer, and a user (authorization code grant, delegate scope, or password auth)

        **Parameters**

        channel: :class:`int`
            channel id of channel to leave

        user: :class:`int`
            user id of user leaving
        """
        self.http.make_request(Path.leave_channel(channel, user))

    def mark_channel_as_read(self, channel_id: int, message_id: int) -> None:
        """
        This endpoint marks the channel as having being read up to the given message_id.

        Requires OAuth, scope lazer, and a user (authorization code grant, delegate scope, or password auth)

        **Parameters**

        channel_id: :class:`int`
            The channel_id of the channel to mark as read

        message_id: :class:`int`
            The message_id of the message to mark as read up to
        """
        self.http.make_request(Path.mark_channel_as_read(channel_id, message_id))

    def get_channel_list(self) -> List[ChatChannel]:
        """
        This endpoint returns a list of all joinable public channels.

        Requires OAuth, scope lazer, and a user (authorization code grant, delegate scope, or password auth)

        **Returns**

        Sequence[:class:`ChatChannel`]
        """
        return list(map(ChatChannel, self.http.make_request(Path.get_channel_list())))

    def create_channel(
        self,
        channel_type: Union[ChatChannelType, str],
        target_id: Optional[int] = None,
        target_ids: Optional[Sequence[int]] = None,
        message: Optional[str] = None,
        channel: Optional[Dict[str, str]] = None,
    ) -> ChatChannel:
        """
        [This description may be outdated]

        This endpoint creates a new channel if doesn't exist and joins it.
        Currently only for rejoining existing PM channels which the user has left.

        Requires OAuth, scope lazer, and a user (authorization code grant, delegate scope, or password auth)

        **Parameter**

        channel_type: Union[:class:`ChatChannelType`, :class:`str`]
            channel type (currently only supports `PM` and `ANNOUNCE`)

        target_id: Optional[:class:`int`]
            target user id; required if type is PM; ignored, otherwise.

        target_ids: Optional[Sequence[:class:`int`]]
            target user ids; required if type is ANNOUNCE; ignored, otherwise.

        message: Optional[:class:`str`]
            message to send with the announcement; required if type is ANNOUNCE.

        channel: Optional[Dict[str, str]]
            channel details; required if type is ANNOUNCE.

            name: :class:`str`
                the channel name

            description: :class:`str`
                the channel description

        **Returns**

        :class:`ChatChannel`
             contains recent_messages attribute (which is deprecated).
        """
        channel_type = parse_enum_args(channel_type)
        if channel_type == "PM":
            data = {"type": "PM", "target_id": target_id}
        elif channel_type == "ANNOUNCE":
            data = {
                "type": channel_type,
                "message": message,
                "channel": json.dumps(channel),
                "target_ids": json.dumps(target_ids),
            }
        else:
            raise ValueError(
                f"{channel_type} is not a valid channel type that can be created. " f"Check for casing (uppercase)."
            )
        return ChatChannel(self.http.make_request(Path.create_channel(), files=create_multipart_formdata(data)))

    def get_channel(self, channel_id: int) -> GetChannelResult:
        """
        Gets details of a chat channel.

        Requires OAuth, scope lazer, and a user (authorization code grant, delegate scope, or password auth)

        **Parameter**

        channel_id: :class:`int`

        **Returns**

        :class:`GetChannelResult`
        """
        resp = self.http.make_request(Path.get_channel(channel_id))
        return GetChannelResult(ChatChannel(resp["channel"]), list(map(UserCompact, resp["users"])))

    def get_comments(
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
            self.http.make_request(
                Path.get_comments(),
                commentable_type=commentable_type,
                commentable_id=commentable_id,
                parent_id=parent_id,
                sort=sort,
                **(cursor if cursor else {}),
            )
        )

    def post_comment(
        self,
        commentable_type: Optional[Union[ObjectType, str]] = None,
        commentable_id: Optional[int] = None,
        message: Optional[str] = None,
        parent_id: Optional[int] = None,
    ) -> CommentBundle:
        """
        Posts a new comment to a comment thread.

        Requires OAuth, scope lazer, and a user (authorization code grant, delegate scope, or password auth)

        **Parameter**

        commentable_type: Optional[Union[:class:`ObjectType`, :class:`str`]
            The type of resource to get comments for. Must be of the following types:
            beatmapset, build, news_post

        commentable_id: Optional[:class:`int`]
            The id of the resource to get comments for. Id correlates with commentable_type.

        message: Optional[:class:`str`]
            Text of the comment

        parent_id: Optional[:class:`int`]
            The id of the comment to reply to, null if not a reply

        **Returns**

        :class:`CommentBundle`
        """
        data = {
            "comment[commentable_type]": parse_enum_args(commentable_type),
            "comment[commentable_id]": commentable_id,
            "comment[message]": message,
            "comment[parent_id]": parent_id,
        }
        return CommentBundle(self.http.make_request(Path.post_new_comment(), files=create_multipart_formdata(data)))

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
        return CommentBundle(self.http.make_request(Path.get_comment(comment)))

    def edit_comment(self, comment: int, message: Optional[str] = None) -> CommentBundle:
        """
        Edit an existing comment.

        Requires OAuth, scope lazer, and a user (authorization code grant, delegate scope, or password auth)

        **Parameters**

        comment: :class:`int`
            Comment id

        message: Optional[:class:`str`]
            New text of the comment

        **Returns**

        :class:`CommentBundle`
        """
        return CommentBundle(
            self.http.make_request(
                Path.edit_comment(comment), files=create_multipart_formdata({"comment[message]": message})
            )
        )

    def delete_comment(self, comment: int) -> CommentBundle:
        """
        Deletes the specified comment.

        Requires OAuth, scope lazer, and a user (authorization code grant, delegate scope, or password auth)

        **Parameters**

        comment: :class:`int`
            Comment id

        **Returns**

        :class:`CommentBundle`
        """
        return CommentBundle(self.http.make_request(Path.delete_comment(comment)))

    def add_comment_vote(self, comment: int) -> CommentBundle:
        """
        Upvotes a comment.

        Requires OAuth, scope lazer, and a user (authorization code grant, delegate scope, or password auth)

        **Parameters**

        comment: :class:`int`
            Comment id

        **Returns**

        :class:`CommentBundle`
        """
        return CommentBundle(self.http.make_request(Path.add_comment_vote(comment)))

    def remove_comment_vote(self, comment: int) -> CommentBundle:
        """
        Un-upvotes a comment.

        Requires OAuth, scope lazer, and a user (authorization code grant, delegate scope, or password auth)

        **Parameters**

        comment: :class:`int`
            Comment id

        **Returns**

        :class:`CommentBundle`
        """
        return CommentBundle(self.http.make_request(Path.remove_comment_vote(comment)))

    def reply_topic(self, topic: int, body: str) -> ForumPost:
        """
        Create a post replying to the specified topic.

        Requires OAuth, scope forum.write, and a user (authorization code grant, delegate scope, or password auth)

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
        return ForumPost(self.http.make_request(Path.reply_topic(topic), files=create_multipart_formdata(data)))

    def create_topic(
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

        Requires OAuth, scope forum.write, and a user (authorization code grant, delegate scope, or password auth)

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
        resp = self.http.make_request(Path.create_topic(), files=create_multipart_formdata(data))
        return CreateTopicResult(ForumTopic(resp["topic"]), ForumPost(resp["post"]))

    def get_topic_and_posts(
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
        resp = self.http.make_request(
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
        data = {"forum_topic[topic_title]": topic_title}
        return ForumTopic(self.http.make_request(Path.edit_topic(topic), files=create_multipart_formdata(data)))

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
        data = {"body": body}
        return ForumPost(self.http.make_request(Path.edit_post(post), files=create_multipart_formdata(data)))

    def search(
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
        resp = self.http.make_request(Path.search(), mode=mode, query=query, page=page)
        return SearchResult(
            get_optional_list(resp.get("user", {}), "data", UserCompact),
            get_optional_list(resp.get("wiki_page", {}), "data", WikiPage),
        )

    def get_user_highscore(self, room: int, playlist: int, user: int) -> MultiplayerScore:
        """
        Requires OAuth, scope lazer, and a user (authorization code grant, delegate scope, or password auth)

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
        return MultiplayerScore(self.http.make_request(Path.get_user_high_score(room, playlist, user)))

    def get_scores(
        self,
        room: int,
        playlist: int,
        limit: Optional[int] = None,
        sort: Optional[Union[str, MultiplayerScoresSort]] = None,
        cursor: Optional[str] = None,
    ) -> MultiplayerScores:
        """
        Requires OAuth, scope public, and a user (authorization code grant, delegate scope, or password auth)

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
            self.http.make_request(
                Path.get_scores(room, playlist),
                limit=limit,
                sort=sort,
                cursor_string=cursor,
            )
        )

    def get_score(self, room: int, playlist: int, score: int) -> MultiplayerScore:
        """
        Requires OAuth, scope lazer, and a user (authorization code grant, delegate scope, or password auth)

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
        return MultiplayerScore(self.http.make_request(Path.get_score(room, playlist, score)))

    def get_news_listing(
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
        resp = self.http.make_request(Path.get_news_listing(), limit=limit, year=year, cursor=cursor)
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

    def get_news_post(self, news: str, key: Optional[str] = None) -> NewsPost:
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
        return NewsPost(self.http.make_request(Path.get_news_post(news), key=key))

    def get_notifications(self, max_id: Optional[int] = None) -> GetNotificationsResult:
        """
        This endpoint returns a list of the user's unread notifications. Sorted descending by id with limit of 50.

        Requires OAuth, scope lazer, a user (authorization code grant, delegate scope, or password auth)

        **Parameters**

        max_id: Optional[:class:`int`]
            Maximum id fetched. Can be used to load earlier notifications.
            Defaults to no limit (fetch latest notifications)

        **Returns**

        :class:`GetNotificationsResult`
        """
        resp = self.http.make_request(Path.get_notifications(), max_id=max_id)
        return GetNotificationsResult(
            list(map(Notification, resp["notifications"])),
            [
                NotificationStackResult(
                    NotificationType(category)
                    if (category := stack["category"]).upper() in NotificationType.__members__
                    else ObjectType(category),
                    stack["cursor"],
                    ObjectType(stack["object_type"]),
                    stack["object_id"],
                    stack["total"],
                )
                for stack in resp["stacks"]
            ],
            parser.parse(resp["timestamp"]),
            [
                NotificationTypeResult(t["cursor"], get_optional(t, "name", ObjectType), t["total"])
                for t in resp["types"]
            ],
            resp.get("unread_count"),
            resp["notification_endpoint"],
        )

    def mark_notifications_read(
        self,
        identities: Optional[Sequence[Union[IdentitiesUtil, Dict[str, Union[str, int]]]]] = None,
        notifications: Optional[Sequence[Union[NotificationsUtil, Dict[str, str]]]] = None,
    ) -> None:
        """
        This endpoint allows you to mark notifications read. Should only supply one of the arguments.

        Requires OAuth, scope lazer, a user (authorization code grant, delegate scope, or password auth)

        **Parameters**

        identities: Optional[Sequence[Union[:class:`IdentitiesUtil`, Dict[:class:`str`, :class:`str`]]]]

        notifications: Optional[Sequence[Union[:class:`NotificationsUtil`, Dict[:class:`str`, :class:`str`]]]]
        """
        name = "identities" if notifications is None else "notifications"
        params = JsonUtil.list_to_labeled_dict(locals()[name], name)
        self.http.make_request(Path.mark_notifications_as_read(), **params)

    def revoke_current_token(self) -> None:
        """
        Revokes currently authenticated token.

        Requires OAuth
        """
        self.http.make_request(Path.revoke_current_token())

    def get_ranking(
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
            self.http.make_request(
                Path.get_ranking(mode, type),
                country=country,
                **(cursor if cursor else {}),
                filter=filter,
                spotlight=spotlight,
                variant=variant,
            )
        )

    def get_spotlights(self) -> Spotlights:
        """
        Gets the list of spotlights.

        Requires OAuth and scope public

        **Returns**

        :class:`Spotlights`
        """
        return Spotlights(self.http.make_request(Path.get_spotlights()))

    def get_own_data(self, mode: Union[str, GameModeStr] = "") -> User:
        """
        Similar to get_user but with authenticated user (token owner) as user id.

        Requires OAuth, scope identify, and a user (authorization code grant, delegate scope, or password auth)

        **Parameters**

        mode: Optional[:class:`str`, :class:`GameModeStr`]
            GameMode. User default mode will be used if not specified.

        **Returns**

        See return for get_user
        """
        mode = parse_enum_args(mode)
        return User(self.http.make_request(Path.get_own_data(mode)))

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
        return list(
            map(
                KudosuHistory,
                self.http.make_request(Path.get_user_kudosu(user), limit=limit, offset=offset),
            )
        )

    def get_user_scores(
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
            Score type. Must be one of `best`, `firsts`, `recent`

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
                self.http.make_request(
                    Path.get_user_scores(user, type),
                    include_fails=int(include_fails),
                    mode=mode,
                    limit=limit,
                    offset=offset,
                ),
            )
        )

    def get_user_beatmaps(
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
                self.http.make_request(Path.get_user_beatmaps(user, type), limit=limit, offset=offset),
            )
        )

    def get_user_recent_activity(
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
                self.http.make_request(Path.get_user_recent_activity(user), limit=limit, offset=offset),
            )
        )

    def get_user(
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
        return User(self.http.make_request(Path.get_user(user, mode), key=key))

    def get_users(self, ids: Sequence[int]) -> List[UserCompact]:
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
        res = self.http.make_request(Path.get_users(), **{"ids[]": ids})
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
        return WikiPage(self.http.make_request(Path.get_wiki_page(locale, path)))

    def get_beatmapset_events(
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
        resp = self.http.make_request(
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

    def get_matches(
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
        resp = self.http.make_request(Path.get_matches(), limit=limit, sort=sort, **{"cursor[match_id]": match_id})
        return GetMatchesResult(list(map(Match, resp["matches"])), resp["params"], resp["cursor"])

    def get_match(self, match_id: int) -> MatchExtended:
        """
        Returns a match by id.

        Requires OAuth and scope public.

        **Parameters**

        match_id: :class:`int`
            The match id.

        **Returns**

        :class:`Match`
        """
        return MatchExtended(self.http.make_request(Path.get_match(match_id)))

    def get_rooms(
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

        Requires OAuth, scope public, and a user (authorization code grant, delegate scope, or password auth).

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
                self.http.make_request(
                    Path.get_rooms(mode),
                    sort=sort,
                    limit=limit,
                    type_group=room_type,
                    category=category,
                    mode=filter_mode,
                ),
            )
        )

    def get_seasonal_backgrounds(self) -> SeasonalBackgrounds:
        """
        Get the season backgrounds.

        Doesn't require OAuth

        **Returns**

        :class:`SeasonalBackgrounds`
        """
        return SeasonalBackgrounds(self.http.make_request(Path.get_seasonal_backgrounds()))

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
        return Room(self.http.make_request(Path.get_room(room_id)))

    def get_score_by_id(self, mode, score_id) -> Union[LegacyScore, SoloScore]:
        """
        Returns a score by id.

        Requires OAuth and scope public.

        **Parameters**

        mode: Union[:class:`str`, :class:`GameModeStr`]

        score_id: :class:`int`

        **Returns**

        Union[:class:`SoloScore`, :class:`LegacyScore`]
        """
        mode = parse_enum_args(mode)
        return get_score_object(self.http.make_request(Path.get_score_by_id(mode, score_id)))

    def search_beatmapsets(self, filters=None, page=None) -> BeatmapsetSearchResult:
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
        resp = self.http.make_request(Path.beatmapset_search(), page=page, **filters)
        return BeatmapsetSearchResult(
            list(map(Beatmapset, resp["beatmapsets"])),
            resp["cursor"],
            resp["search"],
            resp["recommended_difficulty"],
            resp["error"],
            resp["total"],
        )

    def get_room_leaderboard(self, room_id: int) -> GetRoomLeaderboardResult:
        """
        Return a room's leaderboard. The :class:`UserScoreAggregate` objects returned under the "leaderboard"
        key contain the "user" attribute. The :class:`UserScoreAggregate` object under the "user_score" key
        contains the "user" and "position" attributes.

        Requires OAuth, scope public, and a user (authorization code grant, delegate scope, or password auth).

        **Parameters**

        room_id: :class:`int`

        **Returns**

        :class:`GetRoomLeaderboard`
        """
        resp = self.http.make_request(Path.get_room_leaderboard(room_id))
        return GetRoomLeaderboardResult(
            list(map(UserScoreAggregate, resp["leaderboard"])), get_optional(resp, "user_score", UserScoreAggregate)
        )

    def get_replay_data(self, mode, score_id):
        """
        Returns replay data for a score.

        Requires OAuth, scope public, and a user (authorization code grant, delegate scope, or password auth).

        **Parameters**

        mode: Union[:class:`str`, :class:`GameModeStr`]

        score_id: :class:`int`

        **Returns**

        :class:`osrparse.Replay`
        """
        mode = parse_enum_args(mode)
        return Replay.from_string(self.http.make_request(Path.get_replay_data(mode, score_id), is_download=True))

    def get_friends(self):
        """
        Returns a list of friends.

        Requires OAuth, scope friends.read, and a user (authorization code grant, delegate scope, or password auth).

        **Returns**

        List[:class:`User`]
        """
        return list(map(UserCompact, self.http.make_request(Path.get_friends())))

    def favourite_beatmapset(self, beatmapset_id: int, favourite: bool) -> int:
        """
        Add or remove a favourite beatmapset

        Requires OAuth, lazer scope, and a user (authorization code grant, delegate scope, or password auth).

        **Parameters**

        beatmapset_id: :class:`int`

        favourite: :class:`bool`
            whether to favourite (true) or unfavourite (false)

        **Returns**

        :class:`int`
            The number of favourites on the beatmapsets
        """
        resp = self.http.make_request(
            Path.favourite_beatmapset(beatmapset_id),
            data={"action": "favourite" if favourite else "unfavourite"},
        )
        return resp["favourite_count"]

    def get_open_chat_channels(self):
        """
        Get a list of chat channels that you have open. Includes recent DMs and public chat channels.

        Requires OAuth, lazer scope, and a user (authorization code grant, delegate scope, or password auth).

        **Returns**

        List[:class:`ChatChannel`]
        """
        return list(map(ChatChannel, self.http.make_request(Path.get_chat_presence())))

    def join_user_to_room(self, room: int, user: int, password: Optional[str] = None) -> None:
        """
        Join a user to a room.

        Requires OAuth, lazer scope, and a user (authorization code grant, delegate scope, or password auth).

        **Parameters**

        room: :class:`int`

        user: :class:`int`

        password: Optional[:class:`str`]
        """
        self.http.make_request(Path.join_to_room(room, user), password=password)

    def kick_user_from_room(self, room: int, user: int) -> None:
        """
        Kick a user from a room.

        Requires OAuth, lazer scope, and a user (authorization code grant, delegate scope, or password auth).

        **Parameters**

        room: :class:`int`

        user: :class:`int`
        """
        self.http.make_request(Path.kick_from_room(room, user))

    def report(
        self,
        comments: str,
        reason: str,
        reportable_id: int,
        reportable_type: Union[ObjectType, str],
    ) -> None:
        """
        Send a report.

        Requires OAuth, lazer scope, and a user (authorization code grant, delegate scope, or password auth).

        **Parameters**

        comments: :class:`str`

        reason: :class:`str`

        reportable_id: :class:`id`

        reportable_type: Union[:class:`str`, :class:`ObjectType`]
        """
        params = {
            "comments": comments,
            "reason": reason,
            "reportable_id": reportable_id,
            "reportable_type": parse_enum_args(reportable_type),
        }
        self.http.make_request(Path.send_report(), **params)

    def create_multiplayer_room(
        self,
        name: str,
        starting_map: Union[PlaylistItemUtil, dict],
        password: Optional[str] = None,
        queue_mode: Optional[Union[RealTimeQueueMode, str]] = RealTimeQueueMode.HOST_ONLY,
        auto_start_duration: Optional[int] = 0,
        room_type: Optional[Union[RoomType, str]] = RoomType.HEAD_TO_HEAD,
        auto_skip: Optional[bool] = False,
    ) -> Room:
        """
        Create a multiplayer (realtime) room.

        Requires OAuth, lazer scope, and a user (authorization code grant, delegate scope, or password auth).

        **Parameters**

        name: :class:`str`
            Name of the room

        starting_map: Union[:class:`PlaylistItemUtil`, dict]

        password: Optional[:class:`str`]
            Password to enter the room which is optional.

        queue_mode: Optional[Union[:class:`RealTimeQueueMode`, :class:`str`]]
            The mode for queuing maps.

        auto_start_duration: Optional[:class:`int`]

        room_type: Optional[Union[:class:`RoomType`, :class:`str`]]

        auto_skip: Optional[:class:`bool`]
            Whether to automatically skip intro or not.

        **Returns**

        :class:`Room`
        """
        if isinstance(starting_map, PlaylistItemUtil):
            starting_map = starting_map.json
        queue_mode, room_type = parse_enum_args(queue_mode, room_type)
        data = {
            "name": name,
            "password": password,
            "playlist": [starting_map],
            "queue_mode": queue_mode,
            "auto_start_duration": auto_start_duration,
            "category": "realtime",
            "type": room_type,
            "auto_skip": auto_skip,
        }
        return Room(self.http.make_request(Path.create_room(), data=json.dumps(data)))

    def create_playlist(
        self,
        name: str,
        playlist_items: Sequence[Union[PlaylistItemUtil, dict]],
        duration: Optional[int] = None,
        ends_at: Optional[Union[str, datetime]] = None,
        max_attempts: Optional[int] = None,
        queue_mode: Optional[Union[PlaylistQueueMode, str]] = PlaylistQueueMode.HOST_ONLY,
        auto_start_duration: Optional[int] = 0,
    ) -> Room:
        """
        Create a playlist

        Requires OAuth, lazer scope, and a user (authorization code grant, delegate scope, or password auth).

        **Parameters**

        name: :class:`str`
            Name of the playlist

        playlist_items: Sequence[Union[:class:`PlaylistItemUtil`, :class:`dict`]]
            List of beatmaps to put on the playlist

        duration: Optional[:class:`int`]
            Duration for the playlist to last in minutes.
            If not specified then an end time must be specified.
            The playlist must have a duration of at least 30 minutes.

        ends_at: Optional[Union[:class:`datetime.datetime`, :class:`str`]]
            Time for the playlist to end at. If not specified then a duration must be specified.
            Must amount to a duration of at least 30 minutes.

        max_attempts: Optional[:class:`int`]
            Null means infinite attempts.

        queue_mode: Optional[Union[:class:`PlaylistQueueMode`, :class:`str`]]
            PlaylistQueueMode.HOST_ONLY is the only option

        auto_start_duration: Optional[:class:`int`]

        **Returns**

        :class:`Room`
        """
        if duration is None and ends_at is None:
            raise ValueError("Either duration or ends_at must be not null.")
        if ends_at is not None and isinstance(ends_at, datetime):
            ends_at = ends_at.isoformat()
        playlist_items = [item.json if isinstance(item, PlaylistItemUtil) else item for item in playlist_items]
        data = {
            "name": name,
            "max_attempts": max_attempts,
            "duration": duration,
            "ends_at": ends_at,
            "queue_mode": parse_enum_args(queue_mode),
            "auto_start_duration": auto_start_duration,
            "category": "playlists",
            "playlist": playlist_items,
        }
        return Room(self.http.make_request(Path.create_room(), data=json.dumps(data)))

    def check_download_quota(self) -> int:
        """
        Get the amount of quota you've used.

        Requires OAuth, lazer scope, and a user (authorization code grant, delegate scope, or password auth).

        **Returns**

        :class:`int`
        """
        resp = self.http.make_request(Path.download_quota_check())
        return resp["quota_used"]
