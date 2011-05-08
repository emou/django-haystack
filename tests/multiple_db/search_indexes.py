from haystack.indexes import *
from haystack import site
from multiple_db.models import Foo, Bar


class FooIndex(SearchIndex):
    text = CharField(document=True, model_attr='body')


site.register(Foo, FooIndex)
site.register(Bar, db='default')
site.register(Bar, db='db1')
