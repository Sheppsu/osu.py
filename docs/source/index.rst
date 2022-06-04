Welcome to osu.py's documentation!
==================================

Easy to use API wrapper for osu!api written in Python.
This uses osu!api v2, which is still under development.
So some code that was originally working may break overnight.
However, I'll do my best to fix any issues I find as quick as possible.

Getting started
===============
If you're new to osu.py, consider checking out this `guide <guide.html>`_ on how to get started!

Looking for something specific
==============================

There are some examples on the github `here <https://github.com/Sheepposu/osu.py/tree/main/examples>`_ that might help you find what you're looking for. Otherwise here are some common uses for the api that you might be looking for.

* `Get a list of the top player's by score, spotlight, or pp <https://osupy.readthedocs.io/en/latest/api.html#osu.Client.get_ranking>`_
* `Get a beatmap by its id <api.html#osu.Client.get_beatmap>`_ or `Get multiple with one request <api.html#osu.Client.get_beatmaps>`_
* `Get scores on a beatmap <https://osupy.readthedocs.io/en/latest/api.html#osu.Client.get_beatmap_scores>`_
* `Get a user by their id or username <api.html#osu.Client.get_user>`_, `Get multiple with one request (ids only) <api.html#osu.Client.get_users>`_, or `Get the user of the authorization code grant being used <api.html#osu.Client.get_own_data>`_
* `Get a user's score on a beatmap <api.html#osu.Client.get_user_beatmap_score>`_ or `Get all their scores for a beatmap <api.html#osu.Client.get_user_beatmap_scores>`_
* `Get a user's beatmaps (also includes most_played) <api.html#osu.Client.get_user_beatmaps>`_
* `Get top plays or recent plays of a user <api.html#osu.Client.get_user_scores>`_
* `Search users and wiki pages <api.html#osu.Client.search>`_
* `Run Client asynchronously with asyncio <api.html#asynchronousclient>`_
* Get `changelog build <api.html#osu.Client.get_changelog_build>`_ or `changelog listings <api.html#osu.Client.get_changelog_listing>`_
* Get `beatmapset discussion posts <api.html#osu.Client.get_beatmapset_discussion_posts>`_, `beatmapset discussion votes <api.html#osu.Client.get_beatmapset_discussion_votes>`_, or `beatmapset discussions <api.html#osu.Client.get_beatmapset_discussions>`_
* `Get news listings <api.html#osu.Client.get_news_listing>`_ and `news post <api.html#osu.Client.get_news_post>`_

Can't find what you're looking for or need help?
================================================
Join `the discord <https://discord.gg/Z2J6SSRPcE>`_ and feel free to ping me in the osu.py help channel.

Documentation tree
==================

.. toctree::
   :maxdepth: 4

   license.rst
   guide.rst
   api.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
