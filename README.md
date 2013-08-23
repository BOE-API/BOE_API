BOE_API
=======
BOE API, is a REST API for Boletín Oficial del Estado(Official State Bulletin) of Spain. It fetches information from www.boe.es
and stores it in a PostgreSQL DB (Required for performance optimizations).

Requirements
=======

Tested on Ubuntu 12.04.

- PostgreSQL 9.2
- Memcache (optional, if you're not going to use it, delete it from settings)
- Install pip install -r requirements.txt

Use
=======

To execute the API:
```python
python manage.py runserver
```
Go to your browser and type http://localhost:8080/v1/format=json and you should see API's endpoints.

To fetch new laws (from BOE.es) you can execute:
```python
python mange.py getNewInfo 
```
and will fetch documents since last day stored on database.










