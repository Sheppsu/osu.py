API Reference
========================

This page covers *everything* osu.py is capable of.


.. note::
    osu.py uses osu!api v2 which is still under development.
    Some functions under Client will say they require lazer scope in which
    case request cannot be made. Some code may stop working overnight
    due to changes done to the osu!api v2. If
    you run into any issues at all, please report it
    `here <https://github.com/Sheepposu/osu.py/issues>`_. I'll try my
    best to fix any issues as quick as possible.


Interactive Classes
-------------------
Client
^^^^^^

.. autoclass:: osu.Client
    :members:

AsynchronousClient
^^^^^^^^^^^^^^^^^^

.. autoclass:: osu.AsynchronousClient

AuthHandler
^^^^^^^^^^^

.. autoclass:: osu.AuthHandler
    :members:

NotificationWebsocket
^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: osu.NotificationWebsocket
    :members:

Objects
-------
Beatmap
^^^^^^^
.. autoclass:: osu.Beatmap
   :members:

BeatmapCompact
^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapCompact
   :members:
   
BeatmapDifficultyAttributes
^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapDifficultyAttributes
   :members:
   
BeatmapPlaycount
^^^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapPlaycount
   :members:

BeatmapScores
^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapScores
   :members:
   
Beatmapset
^^^^^^^^^^
.. autoclass:: osu.Beatmapset
   :members:
   
BeatmapsetCompact
^^^^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapsetCompact
   :members:
   
BeatmapsetDiscussion
^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapsetDiscussion
   :members:
   
BeatmapsetDiscussionPost
^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapsetDiscussionPost
   :members:

BeatmapsetDiscussionVote
^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapsetDiscussionVote
   :members:

BeatmapsetEvent
^^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapsetEvent
   :members:
   
BeatmapsetEventComment
^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapsetEventComment
   :members:
   
BeatmapsetEventNominate
^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapsetEventNominate
   :members:
   
BeatmapsetEventRemoveFromLoved
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapsetEventRemoveFromLoved
   :members:
   
BeatmapsetEventDisqualify
^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapsetEventDisqualify
   :members:

BeatmapsetEventVote
^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapsetEventVote
   :members:

BeatmapsetEventKudosuGain
^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapsetEventKudosuGain
   :members:

BeatmapsetEventKudosuLost
^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapsetEventKudosuLost
   :members:
   
BeatmapsetEventKudosuRecalculate
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapsetEventKudosuRecalculate
   :members:
   
BeatmapsetEventDiscussionLock
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapsetEventDiscussionLock
   :members:
   
BeatmapsetEventNominationReset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapsetEventNominationReset
   :members:
   
BeatmapsetEventNominationResetReceived
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapsetEventNominationResetReceived
   :members:
   
BeatmapsetEventGenreEdit
^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapsetEventGenreEdit
   :members:
   
BeatmapsetEventLanguageEdit
^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapsetEventLanguageEdit
   :members:
   
BeatmapsetEventNsfwToggle
^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapsetEventNsfwToggle
   :members:
   
BeatmapsetEventOffsetEdit
^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapsetEventOffsetEdit
   :members:
   
BeatmapsetEventBeatmapOwnerChange
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapsetEventBeatmapOwnerChange
   :members:
   
BeatmapUserScore
^^^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapUserScore
   :members:
   
Build
^^^^^
.. autoclass:: osu.Build
   :members:
   
ChangelogEntry
^^^^^^^^^^^^^^
.. autoclass:: osu.ChangelogEntry
   :members:

ChatChannel
^^^^^^^^^^^
.. autoclass:: osu.ChatChannel
   :members:

ChatMessage
^^^^^^^^^^^
.. autoclass:: osu.ChatMessage
   :members:

Comment
^^^^^^^
.. autoclass:: osu.Comment
   :members:

CommentableMeta
^^^^^^^^^^^^^^^
.. autoclass:: osu.CommentableMeta
   :members:

CommentBundle
^^^^^^^^^^^^^
.. autoclass:: osu.CommentBundle
   :members:
   
Covers
^^^^^^
.. autoclass:: osu.Covers
   :members:
   
CurrentUserAttributes
^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.CurrentUserAttributes
   :members:
   
Description
^^^^^^^^^^^
.. autoclass:: osu.Description
   :members:
   
Details
^^^^^^^
.. autoclass:: osu.Details
   :members:

Event
^^^^^
.. autoclass:: osu.Event
   :members:

EventUser
^^^^^^^^^
.. autoclass:: osu.EventUser
   :members:

EventBeatmap
^^^^^^^^^^^^
.. autoclass:: osu.EventBeatmap
   :members:

EventBeatmapset
^^^^^^^^^^^^^^^
.. autoclass:: osu.EventBeatmapset
   :members:
   
Failtimes
^^^^^^^^^
.. autoclass:: osu.Failtimes
   :members:

ForumPost
^^^^^^^^^
.. autoclass:: osu.ForumPost
   :members:

ForumTopic
^^^^^^^^^^
.. autoclass:: osu.ForumTopic
   :members:
   
FruitsBeatmapDifficultyAttributes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.FruitsBeatmapDifficultyAttributes
   :members:
   
GithubUser
^^^^^^^^^^
.. autoclass:: osu.GithubUser
   :members:
   
Giver
^^^^^
.. autoclass:: osu.Giver
   :members:
   
Group
^^^^^
.. autoclass:: osu.Group
   :members:
   
KudosuHistory
^^^^^^^^^^^^^
.. autoclass:: osu.KudosuHistory
   :members:
   
LegacyScore
^^^^^^^^^^^
.. autoclas:: osu.LegacyScore 
   :members:
   
ManiaBeatmapDifficultyAttributes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.ManiaBeatmapDifficultyAttributes
   :members:
   
Match
^^^^^
.. autoclass:: osu.Match
   :members:
   
MatchEvent
^^^^^^^^^^
.. autoclass:: osu.MatchEvent
   :members:
   
MatchExtended
^^^^^^^^^^^^^
.. autoclass:: osu.MatchExtended
   :members:

MultiplayerScores
^^^^^^^^^^^^^^^^^
.. autoclass:: osu.MultiplayerScores
   :members:
   
MultiplayerScoreStatistics
^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.MultiplayerScoreStatistics
   :members:

MultiplayerScoresAround
^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.MultiplayerScoresAround
   :members:
   
NewsPost
^^^^^^^^
.. autoclass:: osu.NewsPost
   :members:
   
Navigation
^^^^^^^^^^
.. autoclass:: osu.Navigation
   :members:

Notification
^^^^^^^^^^^^
.. autoclass:: osu.Notification
   :members:
   
OsuBeatmapDifficultyAttributes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.OsuBeatmapDifficultyAttributes
   :members:
   
PlaylistItem
^^^^^^^^^^^^
.. autoclass:: osu.PlaylistItem
   :members:
   
PlaylistItemStats
^^^^^^^^^^^^^^^^^
.. autoclass:: osu.PlaylistItemStats
   :members:
   
PlaylistMod
^^^^^^^^^^^
.. autoclass:: osu.PlaylistMod
   :members:
   
Poll
^^^^
.. autoclass:: osu.Poll
   :members:

PollOption
^^^^^^^^^^
.. autoclass:: osu.PollOption
   :members:

Post
^^^^
.. autoclass:: osu.Post
   :members:
   
ProfileBanner
^^^^^^^^^^^^^
.. autoclass:: osu.ProfileBanner
   :members:

Rankings
^^^^^^^^
.. autoclass:: osu.Rankings
   :members:
   
Room
^^^^
.. autoclass:: osu.Room
   :members:
   
Scope
^^^^^
.. autoclass:: osu.Scope
   :members:
   
ScoreDataStatistics
^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.ScoreDataStatistics
   :members:

ScoreStatistics
^^^^^^^^^^^^^^^
.. autoclass:: osu.ScoreStatistics
   :members:
   
SoloScore
^^^^^^^^^
.. autoclass:: osu.SoloScore
   :members:

Spotlight
^^^^^^^^^
.. autoclass:: osu.Spotlight
   :members:

Spotlights
^^^^^^^^^^
.. autoclass:: osu.Spotlights
   :members:
   
TaikoBeatmapDifficultyAttributes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.TaikoBeatmapDifficultyAttributes
   :members:
   
UpdateStream
^^^^^^^^^^^^
.. autoclass:: osu.UpdateStream
   :members:

User
^^^^
.. autoclass:: osu.User
   :members:
   
UserCompact
^^^^^^^^^^^
.. autoclass:: osu.UserCompact
   :members:

UserAccountHistory
^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.UserAccountHistory
   :members:

UserBadge
^^^^^^^^^
.. autoclass:: osu.UserBadge
   :members:

UserGroup
^^^^^^^^^
.. autoclass:: osu.UserGroup
   :members:

UserMonthlyPlaycount
^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.UserMonthlyPlaycount
   :members:

UserStatistics
^^^^^^^^^^^^^^
.. autoclass:: osu.UserStatistics
   :members:
   
UserStatisticsRulesets
^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.UserStatisticsRulesets
   :members:
   
Versions
^^^^^^^^
.. autoclass:: osu.Versions
   :members:

WikiPage
^^^^^^^^
.. autoclass:: osu.WikiPage
   :members:


Enums
-----
BeatmapsetEventSort
^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapsetEventSort
   :members:

BeatmapsetEventType
^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapsetEventType
   :members:
   
ChatChannelType
^^^^^^^^^^^^^^^
.. autoclass:: osu.ChatChannelType
   :members:
   
ForumTopicType
^^^^^^^^^^^^^^
.. autoclass:: osu.ForumTopicType
   :members:

GameModeInt
^^^^^^^^^^^
.. autoclass:: osu.GameModeInt
   :members:
   
GameModeStr
^^^^^^^^^^^
.. autoclass:: osu.GameModeStr
   :members:
   
MatchEventType
^^^^^^^^^^^^^^
.. autoclass:: osu.MatchEventType
   :members:
   
MatchSort
^^^^^^^^^
.. autoclass:: osu.MatchSort
   :members:
   
Mod
^^^
.. autoclass:: osu.Mod
   :members:
   
Mods
^^^^
.. autoclass:: osu.Mods
   :members:
   
ObjectType
^^^^^^^^^^
.. autoclass:: osu.ObjectType
   :members:
   
PlaylistQueueMode
^^^^^^^^^^^^^^^^^
.. autoclass:: osu.PlaylistQueueMode
   :members:
   
RankStatus
^^^^^^^^^^
.. autoclass:: osu.RankStatus
   :members:
   
RealTimeQueueMode
^^^^^^^^^^^^^^^^^
.. autoclass:: osu.RealTimeQueueMode
   :members:
   
RealTimeType
^^^^^^^^^^^^
.. autoclass:: osu.RealTimeType
   :members:
   
RoomCategory
^^^^^^^^^^^^
.. autoclass:: osu.RoomCategory
   :members:
   
RoomSort
^^^^^^^^
.. autoclass:: osu.RoomSort
   :members:
   
RoomType
^^^^^^^^
.. autoclass:: osu.RoomType
   :members:

UserBeatmapType
^^^^^^^^^^^^^^^
.. autoclass:: osu.UserBeatmapType
   :members:
   
UserScoreAggregate
^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.UserScoreAggregate
   :members:
   
UserScoreType
^^^^^^^^^^^^^
.. autoclass:: osu.UserScoreType
   :members:
   
WikiSearchMode
^^^^^^^^^^^^^^
.. autoclass:: osu.WikiSearchMode
   :members:
