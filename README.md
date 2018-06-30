# SIGN UP /SIGN IN SNIPPET

This is a snippet for sign up and sign in as part of the beyonic guidelines. It utilises the following

  - Nexmo SMS API
  - Python3
  - Django 2.0+

# Installation
To run the development version :

  - clone this repo
  - navigate into the root folder
  - run the following in terminal
   ```sh
$ pip install -r requirements.txt
$ python3 manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser
```
- Navigate into beyonic_sign_up
- Edit the file settings.py and replace the following with values from [Nexmo](https://www.nexmo.com/)
```python
NEXMO_API_KEY = 'secret_key'
NEXMO_API_SECRET = 'secret_key'
NEXMO_BRAND_NAME = 'your_brand'
```
-Finally run
```sh
$   python manage.py runserver
```
