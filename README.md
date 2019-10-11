## Bugtracker - v0.0.1 - Pre Alpha
This is a bugtracker, it depends on Zathura (https://github.com/p1r-a-t3/zathura), a logger that I wrote few montnhs back. Zathura is still in beta version.

#### Purpose
Final project would be a docker container ready to up and running anywhere you want. Zathura will send the error logs from your apps, or you can write the api if you want. I wrote it to clean up my django skill + I really wanted one of these for my work projects. It's hard to go through logs on production server all the time. 

#### How to setup this project: [Development purpose]

1) Install PostgreSQL.
2) Write the credential in .env file usingn the following key DB_NAME, DB_USER, DB_PASSWORD, DB_URL, DB_PORT
3) Open up a virutalenv
4) Clone the project there.
5) Install all the dependencies from requirements.txt file
6) Run migrate: ```python manage.py migrate```
7) Run the app: ```python manage.py runserver```
