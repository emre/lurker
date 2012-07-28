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

Connecting to Database
======
``` python
class DatabaseConfig(BaseLurkerConfig):
    host = 'localhost'
    user = 'root'
    passwd = ''
    db = ''

connection = Connection(DbConfig)
```

Sending Queries
======
``` python
# salt query
connection.execute("INSERT INTO table_name (name) VALUES (%s)", ['Selami Sahin', ])

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

