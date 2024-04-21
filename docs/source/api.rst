API Reference
=============

This page covers *everything* osu.py is capable of.


Interactive Classes
-------------------

.. autoclass:: osu.Client
    :members:
	
.. autoclass:: osu.AsynchronousClient

.. autoclass:: osu.AuthHandler
    :members:
	
.. autoclass:: osu.AsynchronousAuthHandler
	:members:

.. autoclass:: osu.NotificationWebsocket
    :members:
	
Endpoint results
----------------
Some endpoints return specific responses that don't represent any specific objects.


.. autoclass:: osu.BeatmapsetDiscussionPostsResult
   :members:
   

.. autoclass:: osu.BeatmapsetDiscussionsResult
   :members:
   

.. autoclass:: osu.BeatmapsetDiscussionVotesResult
   :members:
   

.. autoclass:: osu.BeatmapsetSearchResult
   :members:
   

.. autoclass:: osu.ChangelogListingResult
   :members:
   

.. autoclass:: osu.ChangelogListingSearch
   :members:
   

.. autoclass:: osu.CreateNewPmResult
   :members:


.. autoclass:: osu.CreateTopicResult
   :members:


.. autoclass:: osu.GetBeatmapsetEventsResult
   :members:


.. autoclass:: osu.GetMatchesResult
   :members:
   

.. autoclass:: osu.GetNewsListingResult
   :members:
   

.. autoclass:: osu.GetRoomLeaderboardResult
   :members:
   

.. autoclass:: osu.GetTopicAndPostsResult
   :members:
   

.. autoclass:: osu.NewsSidebar
   :members:
   

.. autoclass:: osu.ReviewsConfig
   :members:


.. autoclass:: osu.SearchInfo
   :members:
   

.. autoclass:: osu.SearchResult
   :members:

Objects
-------

.. autoclass:: osu.Achievement
   :members:
   

.. autoclass:: osu.AchievementEvent
   

.. autoclass:: osu.BaseNominations
   :members:


.. autoclass:: osu.Beatmap
   :members:


.. autoclass:: osu.BeatmapCompact
   :members:
   

.. autoclass:: osu.BeatmapDifficultyAttributes
   :members:
   

.. autoclass:: osu.BeatmapPlaycount
   :members:
   

.. autoclass:: osu.BeatmapPlaycountEvent
   :members:


.. autoclass:: osu.BeatmapScores
   :members:
   

.. autoclass:: osu.Beatmapset
   :members:
   

.. autoclass:: osu.BeatmapsetApproveEvent
   :members:
   

.. autoclass:: osu.BeatmapsetAvailability
   :members:
   

.. autoclass:: osu.BeatmapsetCompact
   :members:
   

.. autoclass:: osu.BeatmapsetDeleteEvent
   :members:
   

.. autoclass:: osu.BeatmapsetDiscussion
   :members:
   

.. autoclass:: osu.BeatmapsetDiscussionPermissions
   :members:
   

.. autoclass:: osu.BeatmapsetDiscussionPost
   :members:


.. autoclass:: osu.BeatmapsetDiscussionVote
   :members:


.. autoclass:: osu.BeatmapsetEvent
   :members:
   

.. autoclass:: osu.BeatmapsetEventComment
   :members:
   

.. autoclass:: osu.BeatmapsetEventNominate
   :members:
   

.. autoclass:: osu.BeatmapsetEventRemoveFromLoved
   :members:
   

.. autoclass:: osu.BeatmapsetEventDisqualify
   :members:


.. autoclass:: osu.BeatmapsetEventVote
   :members:


.. autoclass:: osu.BeatmapsetEventKudosuGain
   :members:


.. autoclass:: osu.BeatmapsetEventKudosuLost
   :members:
   

.. autoclass:: osu.BeatmapsetEventKudosuRecalculate
   :members:
   

.. autoclass:: osu.BeatmapsetEventDiscussionLock
   :members:
   

.. autoclass:: osu.BeatmapsetEventNominationReset
   :members:
   

.. autoclass:: osu.BeatmapsetEventNominationResetReceived
   :members:
   

.. autoclass:: osu.BeatmapsetEventGenreEdit
   :members:
   

.. autoclass:: osu.BeatmapsetEventLanguageEdit
   :members:
   

.. autoclass:: osu.BeatmapsetEventNsfwToggle
   :members:
   

.. autoclass:: osu.BeatmapsetEventOffsetEdit
   :members:
   

.. autoclass:: osu.BeatmapsetEventBeatmapOwnerChange
   :members:
   

.. autoclass:: osu.BeatmapsetPermissions
   :members:
   

.. autoclass:: osu.BeatmapsetRequirement
   :members:
   

.. autoclass:: osu.BeatmapsetReviveEvent
   :members:
   

.. autoclass:: osu.BeatmapsetUpdateEvent
   :members:
   

.. autoclass:: osu.BeatmapsetUploadEvent
   :members:
   

.. autoclass:: osu.BeatmapUserScore
   :members:
   

.. autoclass:: osu.Build
   :members:
   

.. autoclass:: osu.ChangelogEntry
   :members:


.. autoclass:: osu.ChatChannel
   :members:
   

.. autoclass:: osu.ChatChannelUserAttributes
   :members:


.. autoclass:: osu.ChatMessage
   :members:


.. autoclass:: osu.Comment
   :members:


.. autoclass:: osu.CommentableMeta
   :members:
   

.. autoclass:: osu.CommentableMetaAttributes
   :members:


.. autoclass:: osu.CommentBundle
   :members:
   

.. autoclass:: osu.Country
   :members:
   

.. autoclass:: osu.Covers
   :members:
   

.. autoclass:: osu.CurrentNomination
   :members:


.. autoclass:: osu.CurrentUserPin
   :members:


.. autoclass:: osu.Event
   :members:


.. autoclass:: osu.EventUser
   :members:


.. autoclass:: osu.EventBeatmap
   :members:


.. autoclass:: osu.EventBeatmapset
   :members:
   

.. autoclass:: osu.Failtimes
   :members:


.. autoclass:: osu.ForumPost
   :members:


.. autoclass:: osu.ForumTopic
   :members:
   

.. autoclass:: osu.FruitsBeatmapDifficultyAttributes
   :members:
   

.. autoclass:: osu.GithubUser
   :members:
   

.. autoclass:: osu.Group
   :members:
   

.. autoclass:: osu.KudosuHistory
   :members:
   

.. autoclass:: osu.LegacyNominations
   :members:
   

.. autoclass:: osu.LegacyScore 
   :members:
   

.. autoclass:: osu.ManiaBeatmapDifficultyAttributes
   :members:
   

.. autoclass:: osu.Match
   :members:
   

.. autoclass:: osu.MatchEvent
   :members:
   

.. autoclass:: osu.MatchExtended
   :members:
   

.. autoclass:: osu.MatchGame
   :members:
   

.. autoclass:: osu.MatchGameScoreInfo
   :members:
   

.. autoclass:: osu.MetadataAttribute
   :members:


.. autoclass:: osu.MultiplayerScores
   :members:


.. autoclass:: osu.MultiplayerScoresAround
   :members:
   

.. autoclass:: osu.NewsPost
   :members:
   

.. autoclass:: osu.Navigation
   :members:
   

.. autoclass:: osu.Nominations
   :members:


.. autoclass:: osu.Notification
   :members:
   

.. autoclass:: osu.OsuBeatmapDifficultyAttributes
   :members:
   

.. autoclass:: osu.PlaylistItem
   :members:
   

.. autoclass:: osu.PlaylistItemStats
   :members:
   

.. autoclass:: osu.Poll
   :members:


.. autoclass:: osu.PollOption
   :members:
   

.. autoclass:: osu.PpWeight
   :members:
   

.. autoclass:: osu.ProfileBanner
   :members:


.. autoclass:: osu.RankEvent
   :members:
   

.. autoclass:: osu.RankHighest
   :members:
   

.. autoclass:: osu.RankHistory
   :members:


.. autoclass:: osu.Rankings
   :members:
   

.. autoclass:: osu.RankLostEvent
   :members:
   

.. autoclass:: osu.ReadNotification
   :members:
   

.. autoclass:: osu.Review
   :members:
   

.. autoclass:: osu.Room
   :members:
   

.. autoclass:: osu.Scope
   :members:
   

.. autoclass:: osu.ScoreDataStatistics
   :members:


.. autoclass:: osu.ScoreStatistics
   :members:
   

.. autoclass:: osu.ScoreUserAttributes
   :members:
   

.. autoclass:: osu.SearchResults
   :members:
   

.. autoclass:: osu.SoloScore
   :members:


.. autoclass:: osu.Spotlight
   :members:


.. autoclass:: osu.Spotlights
   :members:
   

.. autoclass:: osu.SystemDiscussionPostMessage
   :members:
   

.. autoclass:: osu.TaikoBeatmapDifficultyAttributes
   :members:
   

.. autoclass:: osu.TextFormat
   :members:
   

.. autoclass:: osu.UpdateStream
   :members:


.. autoclass:: osu.User
   :members:
   

.. autoclass:: osu.UserCompact
   :members:
   

.. autoclass:: osu.UserCover
   :members:


.. autoclass:: osu.UserAccountHistory
   :members:
   

.. autoclass:: osu.UserAchievement
   :members:


.. autoclass:: osu.UserBadge
   :members:


.. autoclass:: osu.UserGroup
   :members:
   

.. autoclass:: osu.UserKudosu
   :members:


.. autoclass:: osu.UserMonthlyPlaycount
   :members:
   

.. autoclass:: osu.UsernameChangeEvent
   :members:
   

.. autoclass:: osu.UserPreferences
   :members:
   

.. autoclass:: osu.UserRelations
   :members:
   

.. autoclass:: osu.UserReplaysWatchedCount
   :members:


.. autoclass:: osu.UserStatistics
   :members:
   

.. autoclass:: osu.UserStatisticsRulesets
   :members:
   

.. autoclass:: osu.UserStatisticVariant
   :members:
   

.. autoclass:: osu.UserSupportAgain
   :members:
   

.. autoclass:: osu.UserSupportFirst
   :members:
   

.. autoclass:: osu.UserSupportGift
   :members:
   

.. autoclass:: osu.Versions
   :members:


.. autoclass:: osu.VotersSummary
   :members:


.. autoclass:: osu.VotesSummary
   :members:


.. autoclass:: osu.WikiPage
   :members:

Utility
-------

.. autoclass:: osu.BeatmapsetSearchFilter
   :members:
   

.. autoclass:: osu.IdentitiesUtil
   :members:
   

.. autoclass:: osu.NotificationsUtil
   :members:
   

.. autoclass:: osu.PlaylistItemUtil
   :members:
   
Notifications
-------------

.. autoclass:: osu.BeatmapOwnerChangeDetails
   :members:


.. autoclass:: osu.BeatmapsetDiscussionLockDetails
   :members:


.. autoclass:: osu.BeatmapsetDiscussionPostNewDetails
   :members:
   

.. autoclass:: osu.BeatmapsetDiscussionPostNotificationDetails
   :members:


.. autoclass:: osu.BeatmapsetDiscussionQualifiedProblemDetails
   :members:
   

.. autoclass:: osu.BeatmapsetDiscussionReviewNewDetails
   :members:


.. autoclass:: osu.BeatmapsetDiscussionUnlockDetails
   :members:


.. autoclass:: osu.BeatmapsetDisqualifyDetails
   :members:


.. autoclass:: osu.BeatmapsetLoveDetails
   :members:


.. autoclass:: osu.BeatmapsetNominateDetails
   :members:
   

.. autoclass:: osu.BeatmapsetNotificationDetails
   :members:


.. autoclass:: osu.BeatmapsetQualifyDetails
   :members:


.. autoclass:: osu.BeatmapsetRankDetails
   :members:


.. autoclass:: osu.BeatmapsetRemoveFromLovedDetails
   :members:


.. autoclass:: osu.BeatmapsetResetNominationsDetails
   :members:


.. autoclass:: osu.ChannelAnnouncementDetails
   :members:


.. autoclass:: osu.ChannelMessageDetails
   :members:


.. autoclass:: osu.CommentNewDetails
   :members:


.. autoclass:: osu.ForumTopicReplyDetails
   :members:
   

.. autoclass:: osu.Notification
   :members:


.. autoclass:: osu.NotificationsDetailsBase
   :members:


.. autoclass:: osu.ReadNotification
   :members:
   

.. autoclass:: osu.ReviewStats
   :members:


.. autoclass:: osu.UserAchievementUnlockDetails
   :members:


.. autoclass:: osu.UserBeatmapsetNewDetails
   :members:
   

.. autoclass:: osu.UserBeatmapsetReviveDetails
   :members:

Enums
-----

.. autoclass:: osu.BeatmapsetEventSort
   :members:


.. autoclass:: osu.BeatmapsetEventType
   :members:
   

.. autoclass:: osu.BeatmapsetGenre
   :members:
   

.. autoclass:: osu.BeatmapsetLanguage
   :members:
   

.. autoclass:: osu.ChatChannelType
   :members:
   

.. autoclass:: osu.ChatMessageType
   :members:
   

.. autoclass:: osu.ForumTopicType
   :members:


.. autoclass:: osu.GameModeInt
   :members:
   

.. autoclass:: osu.GameModeStr
   :members:
   

.. autoclass:: osu.KudosuAction
   :members:
   

.. autoclass:: osu.MatchEventType
   :members:
   

.. autoclass:: osu.MatchSort
   :members:
   

.. autoclass:: osu.MessageType
   :members:
   

.. autoclass:: osu.Mod
   :members:
   

.. autoclass:: osu.Mods
   :members:
   

.. autoclass:: osu.NotificationCategory
   :members:
   

.. autoclass:: osu.NotificationType
   :members:
   

.. autoclass:: osu.ObjectType
   :members:
   

.. autoclass:: osu.PlaylistQueueMode
   :members:
   

.. autoclass:: osu.RankStatus
   :members:
   

.. autoclass:: osu.RealTimeQueueMode
   :members:
   

.. autoclass:: osu.RoomCategory
   :members:
   

.. autoclass:: osu.RoomFilterMode
   :members:
   

.. autoclass:: osu.RoomSort
   :members:
   

.. autoclass:: osu.RoomType
   :members:
   

.. autoclass:: osu.ScoringType
   :members:
   

.. autoclass:: osu.TeamType
   :members:


.. autoclass:: osu.UserAccountHistoryType
   :members:


.. autoclass:: osu.UserBeatmapType
   :members:
   

.. autoclass:: osu.UserRelationType
   :members:
   

.. autoclass:: osu.UserScoreAggregate
   :members:
   

.. autoclass:: osu.UserScoreType
   :members:
   

.. autoclass:: osu.WikiSearchMode
   :members:
