# 在 mytest/search_indexes.py 文件中

from elasticsearch_dsl import Document, Text
from elasticsearch_dsl.connections import connections
from mytest.models import Book

# 连接到 Elasticsearch
connections.create_connection(hosts=['localhost'])

class BookDocument(Document):
    title = Text()

    class Index:
        name = 'book_index'  # 索引的名称，你可以根据实际情况调整
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    def prepare_title(self, instance):
        return instance.title  # 假设你的 Book 模型有一个 title 字段

    class Django:
        model = Book
