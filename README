Lurker
======
Lurker is a tiny mysql wrapper built on the top of python-mySQLdb.

Installation
======
```
git clone git://github.com/emre/lurker.git
python setup.py install
```

Quick Tutorial
======

Connecting to the database
--------

* with Configuration objects. (This could be preferrable for seperating environments like DevConfig, ProdConfig, TestConfig)


``` python
class DatabaseConfig(BaseLurkerConfig):
    host = 'localhost'
    user = 'root'
    passwd = ''
    db = ''

connection = Connection(DbConfig)

```

* without Configuration objects

```python

connection = Connection().quick_connect("mysql_user", "mysql_passwd", "db_name", "host")

```

Sending Queries
--------
``` python
# returns last_id
connection.execute("INSERT INTO table_name (name) VALUES (%s)", ['Selami Sahin', ])

# returns row count
connection.execute("UPDATE table_name SET name = %s", ["Muhittin Bosat", ])

# returns a result set
all_people = connection.get_results("SELECT * FROM people")

# returns a row
one_people = connection.get_row("SELECT * FROM people WHERE id = 1")

# server-side cursor
for person in connection.iterate("SELECT * FROM people"):
    print person
```

Query Caching Support with Redis
--------
* In order to activate caching support, you need to set cache and cache_information variables in your config class.

``` python
from lurker.configuration import BaseLurkerConfig
from lurker.connection import Connection
from lurker.cache.backends.redis_backend import RedisBackend

class DbConfig(BaseLurkerConfig):
    host = 'localhost'
    user = 'root'
    passwd = 'passwd'
    db = 'db_name'
    cache = True
    cache_information = {
        'backend': RedisBackend,
        'args': (),
        'kwargs': {'host': 'localhost', 'port': 6379, 'db': 0},
    }
```

* Usage in get_results and get_row

``` python

print connection.get_row("SELECT * FROM people WHERE id = %s", parameters=(1,), cache=30)
print connection.get_row("SELECT * FROM people WHERE id = %s", parameters=(1,), cache=30)

# output
# DEBUG:root:cache miss: SELECT * FROM people WHERE id = %s
# {'id': 1L, 'name': u'Emre Yilmaz'}
# DEBUG:root:cache hit: SELECT * FROM people WHERE id = %s
# {u'id': 1, u'name': u'Emre Yilmaz'}

```

Maintainer
======
Emre Yılmaz - [@emre_yilmaz](http://twitter.com/emre_yilmaz)

Contributors
=============
Mirat Can Bayrak - [@mirat](http://twitter.com/mirat)

Projects/Scripts powered by lurker
====================================
 - Database Copy: https://gist.github.com/4686232#file-db_copy-py

