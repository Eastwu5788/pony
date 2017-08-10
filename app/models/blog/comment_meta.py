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
    def edit(comment_id=0, metas=list(), increment=True):
        if comment_id == 0:
            return
        if len(metas) == 0:
            return

        meta = CommentMeta.get(comment_id)
        if not meta:
            meta = CommentMeta(comment_id)

        # TODO: 采用for优化
        if "like" in metas:
            if increment:
                meta.like += 1
            else:
                meta.like -= 1

        if "dislike" in metas:
            if increment:
                meta.dislike += 1
            else:
                meta.dislike -= 1

        if "comment" in metas:
            if increment:
                meta.comment += 1
            else:
                meta.comment -= 1

        meta.save()

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
