# -*- coding:utf-8 -*-
"""
不同版本的Sphinx的api不互通，所以
"""
from libs.sphinx.sphinxapi import *

client = SphinxClient()
client.SetServer("localhost", 9312)


def query_article_with_sphinx(key=""):
    """
    使用Sphinx进行文本检索
    但是api仅支持到2.x在Python 3.x中无法使用
    """
    result = client.Query(key, "article")
    return response_query_result(result)


def response_query_result(result):
    """
    处理Sphinx的响应处理
    """
    result_list = []
    if "matches" not in result:
        return result_list

    for match in result["matches"]:
        attr = match["attrs"]
        result_list.append(attr)

    return result_list
