from typing import Optional


class Path:
    __slots__ = ("method", "path", "scope", "requires_user", "content_type", "accept")

    def __init__(
        self,
        method: str,
        path: str,
        scope: Optional[str],
        requires_user=False,
        content_type="application/json",
        accept="application/json",
    ):
        self.method = method
        self.path = path
        self.scope = scope
        self.requires_user = requires_user
        self.content_type = content_type
        self.accept = accept

    @property
    def requires_auth(self):
        return self.scope is not None

    @classmethod
    def beatmap_lookup(cls):
        return cls("get", "beatmaps/lookup", "public")

    @classmethod
    def user_beatmap_score(cls, beatmap, user):
        return cls("get", f"beatmaps/{beatmap}/scores/users/{user}", "public")

    @classmethod
    def user_beatmap_scores(cls, beatmap, user):
        return cls("get", f"beatmaps/{beatmap}/scores/users/{user}/all", "public")

    @classmethod
    def beatmap_scores(cls, beatmap):
        return cls("get", f"beatmaps/{beatmap}/scores", "public")

    @classmethod
    def lazer_beatmap_scores(cls, beatmap):
        return cls("get", f"beatmaps/{beatmap}/solo-scores", "public")

    @classmethod
    def beatmap(cls, beatmap):
        return cls("get", f"beatmaps/{beatmap}", "public")

    @classmethod
    def beatmaps(cls):
        return cls("get", "beatmaps", "public")

    @classmethod
    def get_beatmap_attributes(cls, beatmap):
        return cls("post", f"beatmaps/{beatmap}/attributes", "public")

    @classmethod
    def get_beatmapset(cls, beatmapset):
        return cls("get", f"beatmapsets/{beatmapset}", "public")

    @classmethod
    def beatmapset_discussion_posts(cls):
        return cls("get", "beatmapsets/discussions/posts", "public")

    @classmethod
    def beatmapset_discussion_votes(cls):
        return cls("get", "beatmapsets/discussions/votes", "public")

    @classmethod
    def beatmapset_discussions(cls):
        return cls("get", "beatmapsets/discussions", "public")

    @classmethod
    def get_changelog_build(cls, stream, build):
        return cls("get", f"changelog/{stream}/{build}", None)

    @classmethod
    def get_changelog_listing(cls):
        return cls("get", "changelog", None)

    @classmethod
    def lookup_changelog_build(cls, changelog):
        return cls("get", f"changelog/{changelog}", None)

    @classmethod
    def get_comments(cls):
        return cls("get", "comments", None)

    @classmethod
    def get_comment(cls, comment):
        return cls("get", f"comments/{comment}", None)

    @classmethod
    def reply_topic(cls, topic):
        return cls("post", f"forums/topics/{topic}/reply", "forum.write", True)

    @classmethod
    def create_topic(cls):
        return cls("post", "forums/topics", "forum.write", True)

    @classmethod
    def get_topic_and_posts(cls, topic):
        return cls("get", f"forums/topics/{topic}", "public")

    @classmethod
    def edit_topic(cls, topic):
        return cls("patch", f"forums/topics/{topic}", "forum.write")

    @classmethod
    def edit_post(cls, post):
        return cls("patch", f"forums/posts/{post}", "forum.write")

    @classmethod
    def search(cls):
        return cls("get", "search", "public")

    @classmethod
    def get_scores(cls, room, playlist):
        return cls("get", f"rooms/{room}/playlist/{playlist}/scores", "public", True)

    @classmethod
    def get_news_listing(cls):
        return cls("get", "news", None)

    @classmethod
    def get_news_post(cls, news):
        return cls("get", f"news/{news}", None)

    @classmethod
    def revoke_current_token(cls):
        return cls("delete", "oauth/tokens/current", "public")

    @classmethod
    def get_ranking(cls, mode, type):
        return cls("get", f"rankings/{mode}/{type}", "public")

    @classmethod
    def get_spotlights(cls):
        return cls("get", "spotlights", "public")

    @classmethod
    def get_own_data(cls, mode=""):
        return cls("get", f"me/{mode}", "identify")

    @classmethod
    def get_user_kudosu(cls, user):
        return cls("get", f"users/{user}/kudosu", "public")

    @classmethod
    def get_user_scores(cls, user, type):
        return cls("get", f"users/{user}/scores/{type}", "public")

    @classmethod
    def get_user_beatmaps(cls, user, type):
        return cls("get", f"users/{user}/beatmapsets/{type}", "public")

    @classmethod
    def get_user_recent_activity(cls, user):
        return cls("get", f"users/{user}/recent_activity", "public")

    @classmethod
    def get_user(cls, user, mode=""):
        return cls("get", f"users/{user}/{mode}", "public")

    @classmethod
    def get_users(cls):
        return cls("get", "users", "public")

    @classmethod
    def lookup_users(cls):
        return cls("get", "users/lookup", "public")

    @classmethod
    def get_wiki_page(cls, locale, path):
        return cls("get", f"wiki/{locale}/{path}", None)

    @classmethod
    def get_score_by_id(cls, mode, score):
        return cls("get", f"scores/{mode}/{score}", "public")

    @classmethod
    def get_score_by_id_only(cls, score):
        return cls("get", f"scores/{score}", "public")

    @classmethod
    def get_beatmapset_events(cls):
        return cls("get", "beatmapsets/events", "public")

    @classmethod
    def get_matches(cls):
        return cls("get", "matches", "public")

    @classmethod
    def get_match(cls, match):
        return cls("get", f"matches/{match}", "public")

    @classmethod
    def get_rooms(cls, mode=""):
        return cls("get", f"rooms/{mode}", "public", True)

    @classmethod
    def get_room(cls, room):
        return cls("get", f"rooms/{room}", "public")

    @classmethod
    def get_room_leaderboard(cls, room):
        return cls("get", f"rooms/{room}/leaderboard", "public", True)

    @classmethod
    def get_seasonal_backgrounds(cls):
        return cls("get", "seasonal-backgrounds", None)

    @classmethod
    def get_replay_data(cls, mode, score):
        return cls("get", f"scores/{mode}/{score}/download", "public", False)

    @classmethod
    def get_replay_data_by_id_only(cls, score):
        return cls("get", f"scores/{score}/download", "public", False)

    @classmethod
    def get_friends(cls):
        return cls("get", "friends", "friends.read", True)

    @classmethod
    def beatmapset_search(cls):
        return cls("get", "beatmapsets/search", "public")

    @classmethod
    def chat_keepalive(cls):
        return cls("post", "chat/ack", "chat.read", True)

    @classmethod
    def create_new_pm(cls):
        return cls("post", "chat/new", "chat.write", True)

    @classmethod
    def get_channel_messages(cls, channel_id):
        return cls("get", f"chat/channels/{channel_id}/messages", "chat.read", True)

    @classmethod
    def send_message_to_channel(cls, channel_id):
        return cls("post", f"chat/channels/{channel_id}/messages", "chat.write", True)

    @classmethod
    def join_channel(cls, channel_id, user_id):
        return cls("put", f"chat/channels/{channel_id}/users/{user_id}", "chat.write_manage", True)

    @classmethod
    def leave_channel(cls, channel_id, user_id):
        return cls("delete", f"chat/channels/{channel_id}/users/{user_id}", "chat.write_manage", True)

    @classmethod
    def mark_channel_read(cls, channel_id, message_id):
        return cls("put", f"chat/channels/{channel_id}/mark-as-read/{message_id}", "chat.read", True)

    @classmethod
    def get_channel_list(cls):
        return cls("get", "chat/channels", "chat.read", True)

    @classmethod
    def create_channel(cls):
        return cls("post", "chat/channels", "chat.write_manage", True)

    @classmethod
    def get_channel(cls, channel_id):
        return cls("get", f"chat/channels/{channel_id}", "chat.read", True)

    @classmethod
    def get_all_scores(cls):
        return cls("get", "scores", "public")

    @classmethod
    def get_forums(cls):
        return cls("get", "forums", "public")

    @classmethod
    def get_forum(cls, forum_id):
        return cls("get", f"forums/{forum_id}", "public")

    @classmethod
    def get_forum_topics(cls):
        return cls("get", "forums/topics", "public")
