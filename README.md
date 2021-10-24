# social_app
python version = 3.7.0
<ol>
<li>1- create virtualenv and activate it.(optional)</li> 
<li>2- install the requirement file using "pip install -r requirements.txt"</li>
<li>3- create a postgres database</li>
<li>4- create .env file in project folder(social_app_project) and set the value of following variables (for the convenience I have given my .env variables values )
    <ul>
        <li>SECRET_KEY=<your_django_secret_key></li>
        <li>DATABASE_NAME=your_db_name</li>
        <li>DATABASE_USER=database_user_name</li>
        <li>DATABASE_USER=database_user_name</li>
        <li>DATABASE_PASS=<database_password></li>
        <li>BASE_API_URL=http://127.0.0.1:8000/api/v1</li>
    </ul>
    <p>You can set the following values of .env varialbles</P>
    SECRET_KEY=django-insecure-y^=0a^iz^@sk37bcuk_a!k&f+_&jxph!#vg%)bfkt#4hep)v(q
    DATABASE_NAME=social_app_db
    DATABASE_USER=postgres
    DATABASE_PASS=admin
    BASE_API_URL=http://127.0.0.1:8000
</li>

<li>5-Add the postgress database in seetings.py. e.g
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': env('DATABASE_NAME'),
            'USER': env('DATABASE_USER'),
            'PASSWORD': env('DATABASE_PASS'),
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }</li>
</ol>

