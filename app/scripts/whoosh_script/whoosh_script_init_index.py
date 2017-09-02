"""
use whoosh to search article

this script is designed to build whoosh index from mysql
and it use jieba to support chinese analyzer

this script is based on django context
therefore you can only run this script in django script
you can use django-extensions to help you just like
shell: python manage.py runscript whoosh_script_init_index

or you can run this script in crontab
* 3 * * * /usr/bin/python /path/pony/manage.py runscript whoosh_script_init_index > /dev/null 2>&1
"""
import os

from whoosh.index import create_in
from whoosh.fields import *
from jieba.analyse import ChineseAnalyzer

from pony.settings import BASE_DIR

from app.models.blog.article import BlogArticle

INDEX_PATH = os.path.join(BASE_DIR, "temp", "article_index")


def get_whoosh_writer(path=""):
    """
    创建一个生成分词的写入对象
    """
    analyzer = ChineseAnalyzer()

    schema = Schema(id=NUMERIC(stored=True), title=TEXT(stored=True), content=TEXT(stored=True, analyzer=analyzer))
    if not os.path.exists(path):
        os.mkdir(path)

    index = create_in(path, schema)
    return index.writer()


def run():
    """
    初始化分词索引
    会重新创建完整数据库内容的索引
    """

    # 删除掉旧的索引文件
    if os.path.exists(INDEX_PATH):
        os.remove(INDEX_PATH)

    # 获取写入对象
    writer = get_whoosh_writer(INDEX_PATH)

    # 从数据库读取所有数据
    article_list = BlogArticle.objects.filter(status=1).all()
    for article in article_list:
        writer.add_document(
            id=article.id,
            title=article.title,
            content=article.content
        )

    # 写入完成后，提交数据
    writer.commit()



