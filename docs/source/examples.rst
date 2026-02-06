========
Examples
========

These examples omit imports and defining ``client`` to reduce repetition.
See the `getting started guide <guide.html>`_ for how to create a client object.

MP Link Finder
^^^^^^^^^^^^^^

This script uses :func:`osu.Client.get_matches` to search for a match
with a title matching some criteria. The function returns a
:class:`osu.results.GetMatchesResult` object. The main object of interest here
is the :class:`osu.objects.Match` object. However, it doesn't contain all the match
information. If you want more information about a match, check out the
:func:`osu.Client.get_match` function.

.. code:: py

    cursor = None
    while True:
        # Get the next 100 matches (cursor tracks where we left off)
        # Using activ=False because we're looking for a match that ended
        result = client.get_matches(cursor=cursor, limit=100, sort=MatchSort.DESCENDING, active=False)
        # update the cursor for the next request
        cursor = result.cursor

        for match in result.matches:
            # Looking for matches with a title starting with "5USC:"
            if match.name.strip().startswith("5USC:"):
                # print the title and link
                print(f"{match.name} | https://osu.ppy.sh/community/matches/{match.id}")

Get User Scores
^^^^^^^^^^^^^^^

This script uses :func:`osu.Client.get_user_scores`, which is used for a user's top scores,
first place scores, recent scores, and pinned scores. The endpoint returns
:class:`osu.objects.SoloScore` objects, but you can also get :class:`osu.objects.LegacyScore`
objects by changing the api version to 20220704 (see :func:`osu.Client.set_api_version`).

.. code:: py

    user_id = 14895608

    # Get a user's top scores
    client.get_user_scores(user_id, UserScoreType.BEST)
    # Get a user's 200th top score
    score = client.get_user_scores(user_id, UserScoreType.BEST, offset=199, limit=1)[0]
    print(score)

    # Get a user's first place scores
    # this time for mania specifically
    client.get_user_scores(user_id, UserScoreType.FIRSTS, mode=GameModeStr.MANIA)

    # Get a user's most recent score
    # including failed scores
    client.get_user_scores(user_id, UserScoreType.RECENT, include_fails=True, limit=1)

    # Get a user's pinned scores
    client.get_user_scores(user_id, UserScoreType.PINNED)

Download Replay
^^^^^^^^^^^^^^^

This script uses :func:`osu.Client.get_user_scores` to get a user's recent score,
checks if the replay is downloadable, and downloads it if so, using
:func:`osu.Client.get_replay_data_by_id_only`. By default,
the function uses the osrparse library. If you want the raw replay data,
specify ``use_osrparse=False``. The code example below uses the osrparse library.

.. code:: py

    # Check the last example for more about this function
    recent_scores = client.get_user_scores(7562902, "recent", limit=1)
    if len(recent_scores) > 0 and recent_scores[0].replay:
        # uses the osrparse library
        # either install osrparse or
        # install osu.py using "osu.py[replay]"
        # or specify use_osrparse=False
        replay_data = client.get_replay_data_by_id_only(recent_scores[0].id)
        replay_data.write_path("replay.osr")
        print("Replay downloaded")
    else:
        print("No scores or no replay")

Get Rankings
^^^^^^^^^^^^

This script uses the :func:`osu.Client.get_ranking` function, which can be
used to get a variety of rankings, depending on the arguments specified.
The first example gets the top 250 players of standard mode by pp and prints
them out.

.. code:: py

    # cursor for pagination
    cursor = None
    for _ in range(5):
        rankings = client.get_ranking(GameModeStr.STANDARD, RankingType.PERFORMANCE, cursor=cursor)
        cursor = rankings.cursor

        # stats: UserStatistics
        for stats in rankings.ranking:
            print(f"#{stats.global_rank}: {stats.user.username}")

This example shows some other possibilities.

.. code:: py

    # US rankings
    client.get_ranking(GameModeStr.STANDARD, RankingType.PERFORMANCE, "US")

    # ranking of countries in mania
    # ranking: CountryStatistics
    client.get_ranking(GameModeStr.MANIA, RankingType.COUNTRY)

    # ranking of teams
    # ranking: UserTeamStatistics
    client.get_ranking(GameModeStr.STANDARD, RankingType.TEAM)

    # other parameters to look at:
    # - filter: filter by friends (requires friends.read scope)
    # - spotlight: specifying a spotlight id
    # - variant: for mania, distinguishing 4k and 7k (only works with RankingType.PERFORMANCE)

Get User Data
^^^^^^^^^^^^^

This script pretty simply gets the data of a user and prints some of it.
It uses the function :func:`osu.Client.get_user` and additionally
:func:`osu.Client.get_own_data`, which is useful when doing user authentication.
There also exists :func:`osu.Client.get_users` and :func:`osu.Client.lookup_users`.

There's lots of data under the :class:`osu.objects.User` object, which you can go check out.

.. code:: py

    user_id = 14895608
    user = client.get_user(user_id)
    print(f"{user.username} [#{user.statistics.global_rank}] {user.statistics.pp}pp | Country: {user.country.name}")
    # Sheppsu [#21923] 7818.91pp | Country: United States

    # can also find by username (don't forget the @)
    # and specify mode
    username = "Sheppsu"
    user = client.get_user("@" + username, mode=GameModeStr.MANIA)

    # if using user authentication use this function
    # to get data for the logged in user
    # (can also specify a mode here)
    client.get_own_data()

Forums
^^^^^^

This code example shows off all the forum endpoints. :func:`osu.Client.get_forums` returns a general overview
of the forums and some subforums. :func:`osu.Client.get_forum` is mostly useful for getting pinned topics,
but also includes some recent topics and forum details. Lastly is :func:`osu.Client.get_forum_topics`, which
can be used to sift through all the topics of a forum, sorting either old or new.

.. code:: py

    # Overview of forums
    result = client.get_forums()
    for forum in result.forums:
        print(forum.name)
        if forum.subforums is not None:
            for subforum in forum.subforums:
                print(f"\t- {subforum.name}")

    tournament_forum_id = 55

    # pinned topics (also contains recent topics and forum info)
    print("Pinned:")
    result = client.get_forum(tournament_forum_id)
    for topic in result.pinned_topics:
        print(f"- {topic.title}")

    # list of topics
    print("Recent topics:")
    cursor = None
    for _ in range(3):
        result = client.get_forum_topics(tournament_forum_id, cursor)
        cursor = result.cursor
        for topic in result.topics:
            print(f"- {topic.title}")

Search Beatmapsets
^^^^^^^^^^^^^^^^^^

This code example shows some examples of searching beatmapsets using
:func:`osu.Client.search_beatmapsets` and :class:`osu.util.BeatmapsetSearchFilter`.
While not shown, there's also a ``page`` argument. Most of the same filters available
on the website are available in :class:`osu.util.BeatmapsetSearchFilter`, and you can
check that class to see all the options.

.. code:: py

    default_search_result = client.search_beatmapsets()
    recently_qualified = client.search_beatmapsets(
        BeatmapsetSearchFilter()
        .set_status(BeatmapsetSearchStatus.QUALIFIED)
    )
    japanese_ranked = client.search_beatmapsets(
        BeatmapsetSearchFilter()
        .set_language(BeatmapsetLanguage.JAPANESE)
        .set_status(BeatmapsetSearchStatus.RANKED)
    )
    russian_rock_loved = client.search_beatmapsets(
        BeatmapsetSearchFilter()
        .set_language(BeatmapsetLanguage.ENGLISH)
        .set_genre(BeatmapsetGenre.METAL)
        .set_status(BeatmapsetSearchStatus.LOVED)
    )
    english_featured_artists_has_video_and_storyboard_including_converts = client.search_beatmapsets(
        BeatmapsetSearchFilter()
        .set_language(BeatmapsetLanguage.ENGLISH)
        .set_generals([BeatmapsetSearchGeneral.FEATURED_ARTISTS, BeatmapsetSearchGeneral.CONVERTS])
        .set_extra([BeatmapsetSearchExtra.VIDEO, BeatmapsetSearchExtra.STORYBOARD])
        .set_status(BeatmapsetSearchStatus.ANY)
    )

    print(f"Default: {default_search_result}\n")
    print(f"Japanese ranked: {japanese_ranked}\n")
    print(f"Russian rock loved: {russian_rock_loved}\n")
    print(f"English featured artists has video and storyboard including converts: {english_featured_artists_has_video_and_storyboard_including_converts}")

Beatmapset Discussion
^^^^^^^^^^^^^^^^^^^^^

This example uses all the beatmapset discussion functions to crawl through some
discussion and print it to text format. :func:`osu.Client.get_beatmapset_discussions`
gets a general overview of discussion on a beatmap. It has many parameters that aren't
utilized in this example. :func:`osu.Client.get_beatmapset_discussion_votes` returns
detailed vote data, and also has many parameters not used in the example.
:func:`osu.Client.get_discussion_posts` can be used to get more detailed information
or posts about a discussion, and also has many parameters.

.. code:: py

    result = client.get_beatmapset_discussions(beatmapset_id=1145452, message_types=[MessageType.PROBLEM, MessageType.REVIEW, MessageType.SUGGESTION])

    # util function
    def get_user(users, user_id):
        return next((user for user in users if user.id == user_id), None)

    for disc in result.discussions:
        post = disc.starting_post
        print("----------------------------------------------------")

        votes_result = client.get_beatmapset_discussion_votes(disc.id)
        votes = votes_result.votes
        user = get_user(result.users, post.user_id)
        print(f"{user.username} created {disc.message_type.value} Post{post.beatmapset_discussion_id} at {post.created_at} (Score: {sum(map(lambda vote: vote.score, votes))}): {post.message}")

        if disc.posts is not None:
            posts = disc.posts
            posts_users = result.users
        else:
            posts_result = client.get_beatmapset_discussion_posts(disc.id)
            posts = posts_result.posts
            posts_users = posts_result.users

        for post in sorted(posts, key=lambda p: p.created_at):
            print("################################################")
            user = get_user(posts_users, post.user_id)
            print(f"{user.username} replied with Post{post.beatmapset_discussion_id} at {post.created_at}: {post.message}")

Comments
^^^^^^^^

:func:`osu.Client.get_comments` and :func:`osu.Client.get_comment` are unique,
because they are the only endpoints that don't require OAuth (you can use it
by doing ``client = Client()``.

.. code:: py

    result = client.get_comments(sort=CommentSort.OLD)
    print(result.comments[0])  # Oldest comment

    result = client.get_comments(commentable_type=ObjectType.Beatmapset, commentable_id=41823)
    print(result.pinned_comments)  # Pinned comments on osu.ppy.sh/beatmapsets/41823
    # replies
    print(result.included_comments)
