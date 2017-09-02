import os
from whoosh.index import open_dir
from whoosh.qparser import QueryParser

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(BASE_DIR, "article_index")


def query_article_by_key(key=""):
    """
    查询文章内容通过key
    """
    if len(key) <= 0:
        return []

    result = list()
    index = open_dir(INDEX_PATH)

    searcher = index.searcher()
    parser = QueryParser("content", schema=index.schema)

    result_list = searcher.search(parser.parse(key))
    for hit in result_list:
        result.append(hit)

    return result

