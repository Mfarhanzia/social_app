# social_app
python version = 3.7.0
<ol>
    <li>Create a virtualenv and activate it.(optional)</li> 
    <li>cd to project folder</li> 
    <li>Install the requirements using "pip install -r requirements.txt"</li>
    <li>Create a postgres database</li>
    <li>Create .env file in project folder(social_app_project) and set the value of following variables (for the convenience I have given my .env variables values )
        <ul>
            <li>SECRET_KEY=<your_django_secret_key></li>
            <li>DATABASE_NAME=your_db_name</li>
            <li>DATABASE_USER=database_user_name</li>
            <li>DATABASE_USER=database_user_name</li>
            <li>DATABASE_PASS=<database_password></li>
            <li>BASE_API_URL=http://127.0.0.1:port</li>
        </ul>
        <p><b>You can set the following values of .env variables</b></P>
        <ul>
            <li>SECRET_KEY=django-insecure-y^=0a^iz^@sk37bcuk_a!k&f+_&jxph!#vg%)bfkt#4hep)v(q</li>
            <li>DATABASE_NAME=you_db_name</li>
            <li>DATABASE_USER=postgres</li>
            <li>DATABASE_PASS=admin</li>
            <li>BASE_API_URL=http://127.0.0.1:8000</li>
        </ul>
    </li>

<li>Add the postgress database in settings.py. e.g<br/>
    DATABASES = {<br/>
        'default': {<br/>
            'ENGINE': 'django.db.backends.postgresql_psycopg2',<br/>
            'NAME': env('DATABASE_NAME'),<br/>
            'USER': env('DATABASE_USER'),<br/>
            'PASSWORD': env('DATABASE_PASS'),<br/>
            'HOST': 'localhost',<br/>
            'PORT': '5432',<br/>
        }<br/>
    }<br/>
</li>
    <li>After connecting the database apply the migrations using "python manage.py migrate" command</li>
    <li>After migrations load dummy data to data using "python manage.py loaddata db_data.json" command.
        <p>Super Admin email: admin@admin.com</p>
        <p>Super Admin Password: Password@1</p>
    </li>
    <li>Last step run the server using "python manage.py runserver" command and access the admin panel at http://127.0.0.1:8000/admin and login using the above given credentials</li>
</ol>

