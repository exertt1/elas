import pytest
from peewee import *

from elasticmapper import PeeweeMapper

db = SqliteDatabase('my_app.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    username = CharField(unique=True)
    is_active = BooleanField(default=True)
    age = SmallIntegerField()
    name_keyword = CharField()


class Post(BaseModel):
    title = CharField()
    author = ForeignKeyField(User, on_delete='CASCADE')


def test_peewee_mapping():
    user_elastic_mapping = PeeweeMapper(
        model=User,
        keyword_fields=['name_keyword'],
    ).load()
    assert user_elastic_mapping['id'] == {'type': 'integer'}
    assert user_elastic_mapping['username'] == {'type': 'text'}
    assert user_elastic_mapping['age'] == {'type': 'short'}
    assert user_elastic_mapping['is_active'] == {'type': 'boolean'}
    assert user_elastic_mapping['name_keyword'] == {'type': 'keyword'}


@pytest.mark.parametrize(
    'follow_nested, excepted_result',
    [
        (False, {'type': 'integer'}),
        (True, {'type': {
            'properties': {
                'id': {'type': 'integer'},
                'username': {'type': 'text'},
                'is_active': {'type': 'boolean'},
                'age': {'type': 'short'},
            },
        }}),
    ]
)
def test_peewee_fk_mapping(follow_nested, excepted_result):
    print(Post._meta.columns.values())

    post_elastic_mapping = PeeweeMapper(
        model=Post,
        follow_nested=follow_nested,
    ).load()
    for field in excepted_result:
        assert field in post_elastic_mapping['author_id']
