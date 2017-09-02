import os
from whoosh.index import open_dir
from whoosh.qparser import QueryParser

from pony.settings import BASE_DIR

INDEX_PATH = os.path.join(BASE_DIR, "temp", "article_index")


def run():
    """
    this script is designed to test search article in shell
    you can easily run this script by the shell below

    shell: python manage.py runscript whoosh_script_test
    """
    index = open_dir(INDEX_PATH)

    searcher = index.searcher()
    parser = QueryParser("content", schema=index.schema)

    result_list = searcher.search(parser.parse("服务器"))
    for hit in result_list:
        print(hit)
