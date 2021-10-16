# social_app
python version = 3.7.0


1- install the requirement file using "pip install requirements.txt"
2- create .env file in project folder(social_app_project) and set the value of following variables
    - SECRET_KEY=<your_django_secret_key>
    - DATABASE_NAME=<your_db_name>
    - DATABASE_USER=<database_user_name>
    - DATABASE_PASS=<database_password>
    - BASE_API_URL=http://127.0.0.1:8000

3- add the postgress database in seetings.py. e.g
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': env('DATABASE_NAME'),
            'USER': env('DATABASE_USER'),
            'PASSWORD': env('DATABASE_PASS'),
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
