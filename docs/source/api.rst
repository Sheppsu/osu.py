Entire API Documentation
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
AuthHandler
^^^^^^^^^^^

.. autoclass:: osu.AuthHandler
    :members:

Client
^^^^^^

.. autoclass:: osu.Client
    :members:

NotificationWebsocket
^^^^^^

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

Failtimes
^^^^^^^^^
.. autoclass:: osu.Failtimes
   :members:

Beatmap
^^^^^^^
.. autoclass:: osu.Beatmap
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

Cursor
^^^^^^
.. autoclass:: osu.Cursor
   :members:

Event
^^^^^
.. autoclass:: osu.Event
   :members:

Achievement
^^^^^^^^^^^
.. autoclass:: osu.Achievement
   :members:

BeatmapPlaycount
^^^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapPlaycount
   :members:

BeatmapsetApprove
^^^^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapsetApprove
   :members:

BeatmapsetDelete
^^^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapsetDelete
   :members:

BeatmapsetRevive
^^^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapsetRevive
   :members:

BeatmapsetUpdate
^^^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapsetUpdate
   :members:

BeatmapsetUpload
^^^^^^^^^^^^^^^^
.. autoclass:: osu.BeatmapsetUpload
   :members:

Rank
^^^^
.. autoclass:: osu.Rank
   :members:

RankLost
^^^^^^^^
.. autoclass:: osu.RankLost
   :members:

UserSupportAgain
^^^^^^^^^^^^^^^^
.. autoclass:: osu.UserSupportAgain
   :members:

UserSupportFirst
^^^^^^^^^^^^^^^^
.. autoclass:: osu.UserSupportFirst
   :members:

UserSupportGift
^^^^^^^^^^^^^^^
.. autoclass:: osu.UserSupportGift
   :members:

UsernameChange
^^^^^^^^^^^^^^
.. autoclass:: osu.UsernameChange
   :members:

EventBeatmap
^^^^^^^^^^^^
.. autoclass:: osu.EventBeatmap
   :members:

EventBeatmapset
^^^^^^^^^^^^^^^
.. autoclass:: osu.EventBeatmapset
   :members:

EventUser
^^^^^^^^^
.. autoclass:: osu.EventUser
   :members:

ForumPost
^^^^^^^^^
.. autoclass:: osu.ForumPost
   :members:

ForumTopic
^^^^^^^^^^
.. autoclass:: osu.ForumTopic
   :members:

Group
^^^^^
.. autoclass:: osu.Group
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

MultiplayerScoresCursor
^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: osu.MultiplayerScoresCursor
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

WikiPage
^^^^^^^^
.. autoclass:: osu.WikiPage
   :members:


Other Information
-----------------
GameMode
^^^^^^^^

Each GameMode has its own api name which is to be used instead of it's actual name

.. csv-table:: GameMode
   :file: _static/GameMode.csv

Timestamp
^^^^^^^^^
Timestamp string in ISO 8601 format.

CommentSort
^^^^^^^^^^^

Available sort types are new, old, top.

.. csv-table:: CommentSort
   :file: _static/CommentSort.csv

MultiplayerScoresSort
^^^^^^^^^^^^^^^^^^^^^

Sort option for multiplayer scores index.

.. csv-table:: MultiplayerScoresSort
   :file: _static/MultiplayerScoresSort.csv

RankingType
^^^^^^^^^^^^^^^^^^^^^

Available ranking types:

.. csv-table:: RankingType
   :file: _static/RankingType.csv
