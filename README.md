# social_app
python version = 3.7.0


- install the requirement file using "pip install requirements.txt"
- add the postgress database in seetings.py. e.g
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': '<you_db_name>',
            'USER': '<user>',
            'PASSWORD': '<password>',
            'HOST': '<host>',
            'PORT': '<port>',
        }
    }