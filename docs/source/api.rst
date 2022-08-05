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
Scope
^^^^^
.. autoclass:: osu.Scope
   :members:

BeatmapCompact
^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapCompact
   :members:
   
BeatmapDifficultyAttributes
^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapDifficultyAttributes
   :members:

OsuBeatmapDifficultyAttributes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.OsuBeatmapDifficultyAttributes
   :members:

TaikoBeatmapDifficultyAttributes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.TaikoBeatmapDifficultyAttributes
   :members:

FruitsBeatmapDifficultyAttributes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.FruitsBeatmapDifficultyAttributes
   :members:

ManiaBeatmapDifficultyAttributes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.ManiaBeatmapDifficultyAttributes
   :members:

Failtimes
^^^^^^^^^
.. autoclass:: osu.Failtimes
   :members:

Beatmap
^^^^^^^
.. autoclass:: osu.Beatmap
   :members:

BeatmapPlaycount
^^^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapPlaycount
   :members:

BeatmapScores
^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapScores
   :members:

Score
^^^^^
.. autoclass:: osu.Score
   :members:

ScoreStatistics
^^^^^^^^^^^^^^^
.. autoclass:: osu.ScoreStatistics
   :members:

BeatmapUserScore
^^^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapUserScore
   :members:

BeatmapsetCompact
^^^^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapsetCompact
   :members:

Covers
^^^^^^
.. autoclass:: osu.Covers
   :members:

Beatmapset
^^^^^^^^^^
.. autoclass:: osu.Beatmapset
   :members:

BeatmapsetDiscussion
^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapsetDiscussion
   :members:
   
Build
^^^^^
.. autoclass:: osu.Build
   :members:
   
Versions
^^^^^^^^
.. autoclass:: osu.Versions
   :members:
   
UpdateStream
^^^^^^^^^^^^
.. autoclass:: osu.UpdateStream
   :members:
   
ChangelogEntry
^^^^^^^^^^^^^^
.. autoclass:: osu.ChangelogEntry
   :members:
   
GithubUser
^^^^^^^^^^
.. autoclass:: osu.GithubUser
   :members:

CurrentUserAttributes
^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.CurrentUserAttributes
   :members:

BeatmapsetDiscussionPost
^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapsetDiscussionPost
   :members:

BeatmapsetDiscussionVote
^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapsetDiscussionVote
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

CommentBundle
^^^^^^^^^^^^^
.. autoclass:: osu.CommentBundle
   :members:

CommentableMeta
^^^^^^^^^^^^^^^
.. autoclass:: osu.CommentableMeta
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

ForumPost
^^^^^^^^^
.. autoclass:: osu.ForumPost
   :members:

ForumTopic
^^^^^^^^^^
.. autoclass:: osu.ForumTopic
   :members:

Poll
^^^^
.. autoclass:: osu.Poll
   :members:

PollOption
^^^^^^^^^^
.. autoclass:: osu.PollOption
   :members:

Group
^^^^^
.. autoclass:: osu.Group
   :members:

Description
^^^^^^^^^^^
.. autoclass:: osu.Description
   :members:

KudosuHistory
^^^^^^^^^^^^^
.. autoclass:: osu.KudosuHistory
   :members:

Post
^^^^
.. autoclass:: osu.Post
   :members:

Giver
^^^^^
.. autoclass:: osu.Giver
   :members:

MultiplayerScore
^^^^^^^^^^^^^^^^
.. autoclass:: osu.MultiplayerScore
   :members:

MultiplayerScores
^^^^^^^^^^^^^^^^^
.. autoclass:: osu.MultiplayerScores
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

Details
^^^^^^^
.. autoclass:: osu.Details
   :members:

Rankings
^^^^^^^^
.. autoclass:: osu.Rankings
   :members:

Spotlight
^^^^^^^^^
.. autoclass:: osu.Spotlight
   :members:

Spotlights
^^^^^^^^^^
.. autoclass:: osu.Spotlights
   :members:

UserCompact
^^^^^^^^^^^
.. autoclass:: osu.UserCompact
   :members:

User
^^^^
.. autoclass:: osu.User
   :members:

ProfileBanner
^^^^^^^^^^^^^
.. autoclass:: osu.ProfileBanner
   :members:

UserAccountHistory
^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.UserAccountHistory
   :members:

UserBadge
^^^^^^^^^
.. autoclass:: osu.UserBadge
   :members:

UserMonthlyPlaycount
^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.UserMonthlyPlaycount
   :members:

UserGroup
^^^^^^^^^
.. autoclass:: osu.UserGroup
   :members:

UserStatistics
^^^^^^^^^^^^^^
.. autoclass:: osu.UserStatistics
   :members:
   
UserStatisticsRulesets
^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.UserStatisticsRulesets
   :members:

WikiPage
^^^^^^^^
.. autoclass:: osu.WikiPage
   :members:


Enums
-----

Mods
^^^^
.. autoclass:: osu.Mods
   :members:

RankStatus
^^^^^^^^^^
.. autoclass:: osu.RankStatus
   :members:
   
GameModeStr
^^^^^^^^^^^
.. autoclass:: osu.GameModeStr
   :members:
   
GameModeInt
^^^^^^^^^^^
.. autoclass:: osu.GameModeInt
   :members:
   
WikiSearchMode
^^^^^^^^^^^^^^
.. autoclass:: osu.WikiSearchMode
   :members:

UserBeatmapType
^^^^^^^^^^^^^^^
.. autoclass:: osu.UserBeatmapType
   :members:
