# ElasticMapper
### ElasticSearch mapper for three ORMs - SQLAlchemy, Peewee, DjangoORM.
#### Allows you to easily generate ElasticSearch mappings based on models.

## Installation

```pip install elasticmapper```

## Basic usage
### Peewee example
```python
from peewee import *
from elasticmapper import load, SupportedORMs

db = SqliteDatabase('my_app.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    username = CharField(unique=True)
    is_active = BooleanField(default=True)
    age = IntegerField()

user_elastic_mapping = load(model=User, orm=SupportedORMs.Peewee) 
```

### SQLAlchemy example

```python
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from elasticmapper import load, SupportedORMs

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    is_active = Column(Boolean)
    age = Column(Integer)

user_elastic_mapping = load(model=User, orm=SupportedORMs.SQLAlchemy) 
```

### DjangoORM example

```python
from django.db import models
from elasticmapper import load, SupportedORMs

class User(models.Model):
    username = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    age = models.IntegerField()

user_elastic_mapping = load(model=User, orm=SupportedORMs.DjangoORM) 
```

#### Output for all examples: 

```python
{
    'id': 'int',
    'username': 'text',
    'age': 'int',
    'is_active': 'bool'
}
```

## Documentation

### elasticmapper.load

- model - required param

A model instance.

- orm - required param

One of the SupportedORMs attributes.

- keyword_fields

A collection that contains attribute names. All of them will have ```keyword``` type in the output mapping.

- include

A collection that contains attribute names. Attributes that are not listed in this collection will not be included in the output mapping.

- exclude

A collection that contains attribute names. Attributes that are listed in this collection will not be included in the output mapping.

- alternative_names

A dictionary that contains attribute names and their new names which will be listed in the output mapping.

For example: 

```elasticmapper.load(model=..., orm=..., alternative_names={'id': 'obj_id'})```

Expected output:

```{'obj_id': 'int'}```



## Contributing

PR are welcome! Thank you for your contribution.

## License 

Copyright © 2022 Polina Beskorovaynaya [ihatemilk](https://github.com/nomilkinmyhome)

This project has [MIT License](https://github.com/nomilkinmyhome/elasticmapper/blob/main/LICENSE).