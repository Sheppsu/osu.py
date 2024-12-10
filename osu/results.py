from dataclasses import dataclass
from typing import Dict, Optional, List, TypeVar, Type, TYPE_CHECKING

from .objects import (
    Beatmap,
    Beatmapset,
    BeatmapsetCompact,
    BeatmapsetDiscussion,
    BeatmapsetDiscussionPost,
    BeatmapsetDiscussionVote,
    BeatmapsetEvent,
    Build,
    ChatChannel,
    ChatMessage,
    ForumPost,
    ForumTopic,
    Match,
    NewsPost,
    Review,
    SoloScore,
    UpdateStream,
    UserCompact,
    UserScoreAggregate,
    WikiPage,
)

_T = TypeVar("_T")


def result_dataclass(cls: Type[_T]) -> Type[_T]:
    """basic wrapper that adds slots"""
    from dataclasses import dataclass as _dataclass, fields

    cls = _dataclass(frozen=True)(cls)

    cls_dict = dict(cls.__dict__)
    field_names = tuple(field.name for field in fields(cls))
    cls_dict["__slots__"] = field_names
    for field_name in field_names:
        cls_dict.pop(field_name, None)
    cls_dict.pop("__dict__", None)

    return type(cls)(cls.__name__, cls.__bases__, cls_dict)


# "trick" type checkers into seeing the classes as dataclasses
# the type checkers can't tell that they are otherwise
if not TYPE_CHECKING:
    dataclass = result_dataclass
    del result_dataclass

__all__ = (
    "BeatmapsetSearchResult",
    "BeatmapsetDiscussionPostsResult",
    "BeatmapsetDiscussionVotesResult",
    "ReviewsConfig",
    "BeatmapsetDiscussionsResult",
    "ChangelogListingSearch",
    "ChangelogListingResult",
    "CreateNewPmResult",
    "CreateTopicResult",
    "GetTopicAndPostsResult",
    "SearchResult",
    "SearchInfo",
    "GetNewsListingResult",
    "NewsSidebar",
    "GetBeatmapsetEventsResult",
    "GetMatchesResult",
    "GetRoomLeaderboardResult",
    "GetChannelResult",
    "GetAllScoresResult",
)


class ResultBase:
    __slots__ = ()

    # For backwards compatibility
    def __getitem__(self, item):
        if isinstance(item, str):
            return getattr(self, item)
        elif isinstance(item, int):
            return self.__slots__[item], getattr(self, self.__slots__[item], None)
        raise AttributeError(f"Could not fetch attribute of {self.__class__.__name__} " f"from item value {item!r}")


@dataclass
class SearchInfo(ResultBase):
    """
    A class for search info in several result objects.

    **Attributes**

    sort: :class:`str`

    limit: :class:`int`

    start: Optional[:class:`str`]

    end: Optional[:class:`str`]
    """

    sort: str
    limit: int
    start: Optional[int]
    end: Optional[int]


@dataclass
class BeatmapsetDiscussionPostsResult(ResultBase):
    """
    Result of :func:`osu.Client.get_beatmapset_discussion_posts`

    **Attributes**

    beatmapsets: List[:class:`BeatmapsetCompact`]

    posts: List[:class:`BeatmapsetDiscussionPost`]

    users: List[:class:`UserCompact`]

    cursor: Dict[:class:`str`, :class:`int`]
    """

    beatmapsets: List[BeatmapsetCompact]
    posts: List[BeatmapsetDiscussionPost]
    users: List[UserCompact]
    cursor: str


@dataclass
class BeatmapsetDiscussionVotesResult(ResultBase):
    """
    Result of :func:`osu.Client.get_beatmapset_discussion_votes`

    **Attributes**

    discussions: List[:class:`BeatmapsetDiscussion`]

    votes: List[:class:`BeatmapsetDiscussionVote`]

    users: List[:class:`UserCompact`]

    cursor: Dict[:class:`str`, :class:`int`]
    """

    discussions: List[BeatmapsetDiscussion]
    votes: List[BeatmapsetDiscussionVote]
    users: List[UserCompact]
    cursor: str


@dataclass
class ReviewsConfig(ResultBase):
    """
    An attribute of :class:`BeatmapsetDiscussionsResult`

    **Attributes**

    max_blocks: :class:`int`
    """

    max_blocks: int


@dataclass
class BeatmapsetDiscussionsResult(ResultBase):
    """
    Result of :func:`osu.Client.get_beatmapset_discussions`

    **Attributes**

    beatmaps: List[:class:`Beatmap`]

    discussions: List[:class:`BeatmapsetDiscussion`]

    included_discussions: List[:class:`BeatmapsetDiscussion`]

    users: List[:class:`UserCompact`]

    reviews_config: :class:`ReviewsConfig`

    cursor: :class:`str`
    """

    beatmaps: List[Beatmap]
    discussions: List[BeatmapsetDiscussion]
    included_discussions: List[BeatmapsetDiscussion]
    users: List[UserCompact]
    reviews_config: ReviewsConfig
    cursor: str


@dataclass
class ChangelogListingSearch(ResultBase):
    """
    Attribute of :class:`ChangelogListingResult`

    **Attributes**

    start: Optional[:class:`str`]
        `start` input

    end: Optional[:class:`str`]
        `end` input

    limit: :class:`int`
        Always 21

    max_id: Optional[:class:`int`]
        `max_id` input

    stream: Optional[:class:`str`]
        `stream` input
    """

    start: Optional[str]
    end: Optional[str]
    limit: int
    max_id: Optional[int]
    stream: Optional[str]


@dataclass
class ChangelogListingResult(ResultBase):
    """
    Result of :func:`osu.Client.get_changelog_listing`

    **Attributes**

    build: List[:class:`Build`]

    streams: List[:class:`Build`]

    search: :class:`ChangelogListingSearch`
    """

    builds: List[Build]
    streams: List[UpdateStream]
    search: ChangelogListingSearch


@dataclass
class CreateNewPmResult(ResultBase):
    """
    Result of :func:`osu.Client.create_new_pm`

    **Attributes**

    channel: :class:`ChatChannel`

    message: :class:`ChatMessage`

    new_channel_id: :class:`int`
        [DEPRECATED] channel id of newly created :class:`ChatChannel`
    """

    channel: ChatChannel
    message: ChatMessage
    new_channel_id: int


@dataclass
class CreateTopicResult(ResultBase):
    """
    Result of :func:`osu.Client.create_topic`

    **Attributes**

    topic: :class:`ForumTopic`

    post: :class:`ForumPost`
        includes body
    """

    topic: ForumTopic
    post: ForumPost


@dataclass
class GetTopicAndPostsResult(ResultBase):
    """
    Result of :func:`osu.Client.get_topic_and_posts`

    **Attributes**

    cursor_string: :class:`str`

    search: :class:`GetTopicAndPostsSearch`
        Parameters used for current request excluding cursor.

    topic: :class:`ForumTopic`

    posts: List[:class:`ForumPost`]
    """

    cursor_string: str
    search: SearchInfo
    topic: ForumTopic
    posts: List[ForumPost]


@dataclass
class SearchResult(ResultBase):
    """
    Result of :func:`osu.Client.search`

    **Attributes**

    user: Optional[List[:class:`UserCompact`]]
        For `all` or `user` mode. Only first 100 results are accessible

    wiki_page: Optional[List[:class:`WikiPage`]]
        For `all` or `wiki_page` mode
    """

    user: Optional[List[UserCompact]]
    wiki_page: Optional[List[WikiPage]]


@dataclass
class NewsSidebar(ResultBase):
    """
    Attribute of :class:`GetNewsListingResult`

    **Attributes**

    current_year: :class:`int`

    news_post: List[:class:`NewsPost`]

    years: List[:class:`int`]
    """

    current_year: int
    news_post: List[NewsPost]
    years: List[int]


@dataclass
class GetNewsListingResult(ResultBase):
    """
    Result of :func:`osu.Client.get_news_listing`

    **Attributes**

    cursor: :class:`str`

    news_posts: List[:class:`NewsPost`]

    news_sidebar: :class:`NewsSidebar`

    search: :class:`SearchInfo`
    """

    cursor: str
    news_posts: List[NewsPost]
    news_sidebar: NewsSidebar
    search: SearchInfo


@dataclass
class GetBeatmapsetEventsResult(ResultBase):
    """
    Result of :func:`osu.Client.get_beatmapset_events`

    **Attributes**

    events: List[:class:`BeatmapsetEvent`]

    reviews_config: :class:`Review`

    users: List[:class:`UserCompact`]
        Includes `groups` attribute
    """

    events: List[BeatmapsetEvent]
    reviews_config: Review
    users: List[UserCompact]


@dataclass
class GetMatchesResult(ResultBase):
    """
    Result of :func:`osu.Client.get_matches`

    **Attributes**

    matches: List[:class:`Match`]

    params: Dict

    cursor: Dict
    """

    matches: List[Match]
    params: Dict
    cursor: Dict


@dataclass
class BeatmapsetSearchResult(ResultBase):
    """
    Result of :func:`osu.Client.search_beatmapsets`

    **Attributes**

    beatmapsets: List[:class:`Beatmapset`]

    cursor: Dict

    search: :class:`SearchInfo`

    recommended_difficulty: Optional[:class:`int`]

    error: Optional[:class:`str`]

    total: :class:`int`
    """

    beatmapsets: List[Beatmapset]
    cursor: Dict
    search: SearchInfo
    recommended_difficulty: Optional[float]
    error: Optional[str]
    total: int


@dataclass
class GetRoomLeaderboardResult(ResultBase):
    """
    Result of :func:`osu.Client.get_room_leaderboard`

    **Attributes**

    leaderboard: List[:class:`UserScoreAggregate`]

    user_score: Optional[:class:`UserScoreAggregate`]
    """

    leaderboard: List[UserScoreAggregate]
    user_score: Optional[UserScoreAggregate]


@dataclass
class GetChannelResult(ResultBase):
    """
    Result of :func:`osu.Client.get_channel`

    **Attributes**

    channel: :class:`ChatChannel`

    users: List[:class:`UserCompact`]
    """

    channel: ChatChannel
    users: List[UserCompact]


@dataclass
class GetAllScoresResult(ResultBase):
    """
    Result of :func:`osu.Client.get_all_scores`

    **Attributes**

    scores: List[:class:`SoloScore`]

    cursor: :class:`str`
    """

    scores: List[SoloScore]
    cursor: str
