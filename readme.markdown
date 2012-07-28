Lurker
======
Lurker is a tiny mysql wrapper built on the top of python-mySQLdb.

Installation
======
todo

Requirements
======
todo

Configuration options
======
todo

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

# server-side cursor
for person in connection.iterate("SELECT * FROM people"):
    print person
```



Authors
======
Emre Yılmaz - [@emre_yilmaz](http://twitter.com/emre_yilmaz)

License
======
todo

