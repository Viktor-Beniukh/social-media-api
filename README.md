# Social Media API 

"""
API service for social media management written in DRF 
with the opportunity create new posts and comments to them, 
implemented the opportunity managing likes and dislikes, following and unfollowing. 
There's also a possible to create new users and profiles to them.
"""

### Installing using GitHub

Install PostgreSQL and create db

```shell
git clone https://github.com/Viktor-Beniukh/social-media-api.git
cd social-media-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver   
```
You need to create `.env` file and add there the variables with your according values:
- `POSTGRES_DB`: this is databases name;
- `POSTGRES_USER`: this is username for databases;
- `POSTGRES_PASSWORD`: this is username password for databases;
- `POSTGRES_HOST`: this is host name for databases;
- `POSTGRES_PORT`: this is port for databases;
- `SECRET_KEY`: this is Django Secret Key - by default is set automatically when you create a Django project.
                You can generate a new key, if you want, by following the link: `https://djecrety.ir`;
- `CELERY_BROKER_URL` & `CELERY_RESULT_BACKEND`: they're used to create periodic tasks. Have to install Celery & Redis;

  
## Run with docker

Docker should be installed

- Create docker image: `docker-compose build`
- Run docker app: `docker-compose up`


## Getting access

- Create user via /api/users/register/
- Get access token via /api/users/token/


## Features

- Token authentication;
- Admin panel /admin/;
- Documentation is located at /api/doc/swagger/;
- Managing profile of users, posts, comments, votes and following;
- Registering users;
- Creating a token for a user;
- Deleting a token for an authenticated user;
- Creating a user profile;
- Creating posts;
- Creating comments;
- Filtering users and profiles for them, posts, comments.

### How to create superuser
- Run `docker-compose up` command, and check with `docker ps`, that 2 services are up and running;
- Create new admin user. Enter container `docker exec -it <container_name> bash`, and create in from there;

### What do APIs do
- [GET] /api/users/ - obtains a list of users with the possibility of filtering by username;
- [GET] /api/users/<id>/ - obtains a detail of user;
- [POST] /api/users/register/ - creates new users;
- [POST] /api/users/token/ - creates token for user;
- [POST] /api/users/logout/ - deletes token for authenticated user;
- [GET]  /api/users/me/ - get my profile info;
- [PUT]  /api/users/me/ - update my profile info;

- [GET] /api/profiles/ - obtains a list of users profile with the possibility of filtering by owner_id;
- [GET] /api/profiles/<id>/ - obtains a detail of user profile;
- [POST] /api/profiles/ - creates a user profile;
- [PUT] /api/profiles/<id>/ - updates a user profile;
- [DELETE] /api/profiles/<id>/ - deletes a user profile;

- [GET] /posts/ - obtains a list of posts with the possibility of filtering by author_id and by hashtags;
- [GET] /posts/<id>/ - get specific post;
- [POST] /posts/ - creates a post;

- [GET] /api/comments/ - obtains a list of comments to posts;
- [GET] /api/comments/<id>/ - obtains a detail of comment to post;
- [POST] /api/comments/ - creates a comment to post;

- [GET] /api/votes/ - obtains a list of votes to posts;
- [POST] /api/votes/ - creates a vote (like & dislike) to post;


### Checking the endpoints functionality
- You can see detailed APIs at swagger page: via /api/doc/swagger/


## Testing

- Run tests using different approach: `docker-compose run app sh -c "python manage.py test"`;
- If needed, also check the flake8: `docker-compose run app sh -c "flake8"`.


## Check project functionality

Superuser credentials for test the functionality of this project:
- email address: `migrated@admin.com`;
- password: `adminpassword`.


## Create token for user

Token page: `http://127.0.0.1:8000/api/users/token/`

Enter:
- email address: `migrated@admin.com`;
- password: `adminpassword`.
