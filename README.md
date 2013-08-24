BOE_API
=======
BOE API, is a REST API for Boletín Oficial del Estado(Official State Bulletin) of Spain. It fetches information from www.boe.es
and stores it in a PostgreSQL DB (Required for performance optimizations).

Requirements
=======

Tested on Ubuntu 12.04.

- PostgreSQL 9.1
- Memcache (optional, if you're not going to use it, delete it from settings)
- Install ```python pip install -r requirements.txt```

Use
=======
Sincronize DB:
```python
python manage.py syncdb
```

To execute the API:
```python
python manage.py runserver
```
Go to your browser and type ```http://localhost:8080/v1/format=json``` and you should see API's endpoints.

To fetch new laws (from BOE.es) you can execute:
```python
python manage.py getNewInfo 
```
and will fetch documents since last day stored on database or since 1960 if the database is empty.

You can pass a date to fetch laws since that date:

```python

python manage.py getNewInfo YYYY  
python manage.py getNewInfo YYYY MM
python manage.py getNewInfo YYYY MM DD

```










