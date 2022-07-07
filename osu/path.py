from .objects import Scope


class Path:
    def __init__(self, path, scope):
        self.path = path
        if type(scope) == str:
            scope = Scope(scope)
        self.scope = scope

    @property
    def requires_auth(self):
        return len(self.scope) != 0

    @classmethod
    def beatmap_lookup(cls):
        return cls("beatmaps/lookup", 'public')

    @classmethod
    def user_beatmap_score(cls, beatmap, user):
        return cls(f"beatmaps/{beatmap}/scores/users/{user}", 'public')

    @classmethod
    def user_beatmap_scores(cls, beatmap, user):
        return cls(f"beatmaps/{beatmap}/scores/users/{user}/all", 'public')

    @classmethod
    def beatmap_scores(cls, beatmap):
        return cls(f"beatmaps/{beatmap}/scores", 'public')

    @classmethod
    def beatmap(cls, beatmap):
        return cls(f"beatmaps/{beatmap}", 'public')

    @classmethod
    def beatmaps(cls):
        return cls("beatmaps", 'public')

    @classmethod
    def get_beatmap_attributes(cls, beatmap):
        return cls(f"beatmaps/{beatmap}/attributes", 'public')

    @classmethod
    def beatmapset_discussion_posts(cls):
        return cls('beatmapsets/discussions/posts', 'public')

    @classmethod
    def beatmapset_discussion_votes(cls):
        return cls('beatmapsets/discussions/votes', 'public')

    @classmethod
    def beatmapset_discussions(cls):
        return cls('beatmapsets/discussions', 'public')

    @classmethod
    def get_changelog_build(cls, stream, build):
        return cls(f"changelog/{stream}/{build}", Scope())

    @classmethod
    def get_changelog_listing(cls):
        return cls('changelog', Scope())

    @classmethod
    def lookup_changelog_build(cls, changelog):
        return cls(f'changelog/{changelog}', Scope())

    @classmethod
    def create_new_pm(cls):
        return cls('chat/new', 'chat.write')

    @classmethod
    def get_updates(cls):
        return cls('chat/updates', 'lazer')

    @classmethod
    def get_channel_messages(cls, channel):
        return cls(f'chat/channels/{channel}/messages', 'lazer')

    @classmethod
    def send_message_to_channel(cls, channel):
        return cls(f'chat/channels/{channel}/messages', 'lazer')

    @classmethod
    def join_channel(cls, channel, user):
        return cls(f'chat/channels/{channel}/users/{user}', 'lazer')

    @classmethod
    def leave_channel(cls, channel, user):
        return cls(f'chat/channels/{channel}/users/{user}', 'lazer')

    @classmethod
    def mark_channel_as_read(cls, channel, message):
        return cls(f'chat/channels/{channel}/mark-as-read/{message}', 'lazer')

    @classmethod
    def get_channel_list(cls):
        return cls('chat/channels', 'lazer')

    @classmethod
    def create_channel(cls):
        return cls('chat/channels', 'lazer')

    @classmethod
    def get_channel(cls, channel):
        return cls(f'chat/channels/{channel}', 'lazer')

    @classmethod
    def get_comments(cls):
        return cls('comments', None)

    @classmethod
    def post_new_comment(cls):
        return cls('comments', 'lazer')

    @classmethod
    def get_comment(cls, comment):
        return cls(f'comments/{comment}', None)

    @classmethod
    def edit_comment(cls, comment):
        return cls(f'comments/{comment}', 'lazer')

    @classmethod
    def delete_comment(cls, comment):
        return cls(f'comments/{comment}', 'lazer')

    @classmethod
    def add_comment_vote(cls, comment):
        return cls(f'comments/{comment}/vote', 'lazer')

    @classmethod
    def remove_comment_vote(cls, comment):
        return cls(f'comments/{comment}/vote', 'lazer')

    @classmethod
    def reply_topic(cls, topic):
        return cls(f'forums/topics/{topic}/reply', 'forum.write')

    @classmethod
    def create_topic(cls):
        return cls('forums/topics', 'forum.write')

    @classmethod
    def get_topic_and_posts(cls, topic):
        return cls(f'forums/topics/{topic}', 'public')

    @classmethod
    def edit_topic(cls, topic):
        return cls(f'forums/topics/{topic}', 'forum.write')

    @classmethod
    def edit_post(cls, post):
        return cls(f'forums/posts/{post}', 'forum.write')

    @classmethod
    def search(cls):
        return cls('search', 'public')

    @classmethod
    def get_user_high_score(cls, room, playlist, user):
        return cls(f'rooms/{room}/playlist/{playlist}/scores/users/{user}', 'lazer')

    @classmethod
    def get_scores(cls, room, playlist):
        return cls(f'rooms/{room}/playlist/{playlist}/scores', 'public')

    @classmethod
    def get_score(cls, room, playlist, score):
        return cls(f'rooms/{room}/playlist/{playlist}/scores/{score}', 'lazer')

    @classmethod
    def get_news_listing(cls):
        return cls('news', Scope())

    @classmethod
    def get_news_post(cls, news):
        return cls(f'news/{news}', Scope())

    @classmethod
    def get_notifications(cls):
        return cls('notifications', 'lazer')

    @classmethod
    def mark_notifications_as_read(cls):
        return cls('notifications/mark-read', 'lazer')

    @classmethod
    def revoke_current_token(cls):
        return cls('oauth/tokens/current', 'public')

    @classmethod
    def get_ranking(cls, mode, type):
        return cls(f'rankings/{mode}/{type}', 'public')

    @classmethod
    def get_spotlights(cls):
        return cls('spotlights', 'public')

    @classmethod
    def get_own_data(cls, mode=''):
        return cls(f'me/{mode}', 'identify')

    @classmethod
    def get_user_kudosu(cls, user):
        return cls(f'users/{user}/kudosu', 'public')

    @classmethod
    def get_user_scores(cls, user, type):
        return cls(f'users/{user}/scores/{type}', 'public')

    @classmethod
    def get_user_beatmaps(cls, user, type):
        return cls(f'users/{user}/beatmapsets/{type}', 'public')

    @classmethod
    def get_user_recent_activity(cls, user):
        return cls(f'users/{user}/recent_activity', 'public')

    @classmethod
    def get_user(cls, user, mode=''):
        return cls(f'users/{user}/{mode}', 'public')

    @classmethod
    def get_users(cls):
        return cls('users', 'lazer')

    @classmethod
    def get_wiki_page(cls, locale, path):
        return cls(f'wiki/{locale}/{path}', None)

    @classmethod
    def get_score_by_id(cls, mode, score):
        return cls(f'scores/{mode}/{score}', 'public')
