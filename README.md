## Bugtracker - (v0.0.1 - Pre Alpha)
I have written a pypi package, Zathura (https://github.com/p1r-a-t3/zathura) to register the logging. This app (Bugtracker) tracks logs by projects. Projects will be under a specific team. I have designed this to minimize the debugging hustle I have faced at work.

#### Goal
Final project would be a docker container ready to up and running anywhere you want. Zathura will send the error logs from your apps, or you can write the api if you want.

#### How to setup this project: [Development purpose]

1) Install PostgreSQL.
2) Write the credential in .env file usingn the following key DB_NAME, DB_USER, DB_PASSWORD, DB_URL, DB_PORT, SECRET_KEY
3) Open up a virutalenv
4) Clone the project there.
5) Install all the dependencies from requirements.txt file
6) Run migrate: ```python manage.py migrate```
7) Run the app: ```python manage.py runserver```
