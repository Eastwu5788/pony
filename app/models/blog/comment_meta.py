from app.modules.common.redis import Redis
from app.models.blog.comment_like import CommentLike

_CACHE_KEY = "Pony:CommentMeta:"


class CommentMeta(object):

    def __init__(self, comment_id=0, like=0, dislike=0, comment=0):
        self.comment_id = comment_id
        self.like = like
        self.dislike = dislike
        self.comment = comment

    def save(self):
        key = CommentMeta.get_storage_key(self.comment_id)
        Redis.set_model(key, self)

    @staticmethod
    def get(comment_id):
        """
        :rtype: CommentMeta
        """
        key = CommentMeta.get_storage_key(comment_id)
        return Redis.get_model(key)

    @staticmethod
    def get_format_meta(comment_id, visitor_id=0):
        meta = CommentMeta.get(comment_id)
        result = dict()
        result["like"] = meta.like if meta else 0
        result["liked"] = 1 if CommentLike.user_liked(comment_id, visitor_id) else 0
        result["comment"] = meta.comment if meta else 0
        result["dislike"] = meta.dislike if meta else 0
        return result

    @staticmethod
    def get_storage_key(comment_id):
        return _CACHE_KEY + str(comment_id)
