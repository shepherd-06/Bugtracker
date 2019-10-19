##  Bugtracker - v0.0.1 - pre-alpha
### How Bugtracker works
<b>Step 1:</b> Install postgresql on your server. By default: this will ensure your data integrity from my
                part. Then create a database and user for this app. Give the user permission on the newly created
                database.
                User will need <strong> connect, select, insert, update and delete </strong> permissions on the
                database.
                However, if you are feeling lazy, you may grant <i>
                    all privileges on all tables in the schema</i>, although I don't recommend this.
                Finally, above all else, please don't use <b>root</b> user or grant the new user <u>
                    supseruser</u> permissions. 
                    How to install postgresql database on ubuntu server
                    <a href="https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04"
                        target="_blank"> Click here </a>
                    and
                    <a href="https://stackoverflow.com/a/12721095/6029175" target="_blank">
                        here
                    </a>
                    and
                    <a href="https://tableplus.com/blog/2018/04/postgresql-how-to-grant-access-to-users.html"
                        target="_blank">
                        here!
                    </a>

<strong>Step 2:</strong> Clone the repository from <a href="https://github.com/p1r-a-t3/Bugtracker" target="_blank">
                    github.</a> Create a <a href="https://pypi.org/project/virtualenv/" target="_blank"> virtualenv </a>
                for bugtracker, install <u>all the dependencies</u> from requirements.txt file.

    pip install -r requirements.txt

 <strong>This part is really important, Bugtracker won't work unless you fully install every requirements. </strong>
                    
<strong>Step 3:</strong> create a new .env file using your favorite editor on the project root directory.
      
      vim .env
Fill up the following entry on your .env file. <strong> DB_NAME, DB_USER, DB_PASSWORD, DB_URL, DB_PORT, SECRET_KEY.</strong>

SECRET_KEY could be anything as trivial as 123456 to UUID! I hope you are not using 123456 though.

<strong>Step 4:</strong> Now the moment of truth. I hope everything is all set and done. We are going to run migration.
        
    python3 manage.py migrate

<i> If it fails, please open up an issue on the github repository. </i>

<strong>Step 5:</strong> We would need to manage the static files as well.
       
    python3 manage.py collectstatic
 This will open up a new directory and store all the static files in it. It's already supposed to be there with the repository, however, running this command won't kill anyone!
         
<strong>Step 6:</strong> Now we run this project. I hope you are going to run this project through nginx.
      
    nohup python3 manage.py runserver 0.0.0.0:8000 &
                
This will start the app in background on port 8000. You can change it to anything else! Logs of command will be stored in .nohup.out file.
            
<strong>Step 7:</strong> You can use your webserver (nginx or apache) to forward to traffic to the server. There will be three entries for this. One will direct the traffic to port 8000 (or your defined port), the next will direct the traffic to static files and the another one for Django's admin portal.
Nginx example:
      
      location / {
            rewrite ^/route/?(.*)$ /$1 break;
            proxy_pass  http://0.0.0.0:8000/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_read_timeout 60s;
        }

        location /static/ {
                alias /home/username/project_root_directory/static_bugtracker/;
        }

        location admin/ {
                rewrite ^/route/?(.*)$ /$1 break;
                proxy_pass  http://0.0.0.0:8000/admin/;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_read_timeout 60s;
        }

Step 8: Restart nginx server to take the effect.
    
    sudo service nginx restart
____________________________________________________
That's it! This should keep app running on your server, go ahead and check it out from your browser!
