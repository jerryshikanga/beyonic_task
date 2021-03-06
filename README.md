# SIGN UP /SIGN IN SNIPPET

This is a snippet for sign up and sign in as part of the beyonic guidelines. It utilises the following

  - Nexmo SMS API
  - Python3
  - Django 2.0+
  - Celery and RabbitMQ

# Installation
To run the development version :

  - clone this repo
  - navigate into the root folder
  - run the following in terminal
   ```sh
$ pip install -r requirements.txt
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$ python3 manage.py collectstatic 
$ python3 manage.py createsuperuser
```
- Edit the file beyonic_sign_up/settings.py and replace the following with values from [Nexmo](https://www.nexmo.com/)
```python
NEXMO_API_KEY = 'secret_key'
NEXMO_API_SECRET = 'secret_key'
NEXMO_BRAND_NAME = 'your_brand'
```
-Finally run
```sh
$   celery -A beyonic_sign_up worker -l info
$   python3 manage.py runserver
```
Visit the site on your browser at [localhost:8000/accounts/register/](http://localhost:8000/accounts/register/)