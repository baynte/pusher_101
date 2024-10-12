
# Django Pusher 

A brief test from a colleague


## Installation
First install the dependency
```bash
  pip install -r requirements.txt
```

Edit the .env
```bash
DATABASE_URL=mysql://<username>:<password>@127.0.0.1:3306/<database_name>
PUSHER_APP_ID = '<app_id>'
PUSHER_APP_KEY = '<app_key>'
PUSHER_APP_SECRET = '<app_secret>'
PUSHER_APP_CLUSTER = '<app_cluster>'
```

Migrate the model in database

```bash
  py .\manage.py migrate
```
    
