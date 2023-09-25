### Heroku
#### 1. Creating the inital Django app
* First follow these steps to create your app:
add to local deployment section: here
* Install Django and gunicorn: `pip3 install django gunicorn`
* Install supporting database libraries dj_database_url and psycopg2 library: `pip3 install dj_database_url psycopg2`
* Install Cloudinary libraries to manage photos: in the terminal window type `pip3 install dj-3-cloudinary-storage`
* Create file for requirements: in the terminal window type `pip freeze --local > requirements.txt`
* Create project: in the terminal window type `django-admin startproject project_name .`
* Create app: in the terminal window type `python3 manage.py startapp app_name`
* Add app to list of `installed apps` in settings.py file: `'app_name'`
* Migrate changes: in the terminal window type `python3 manage.py migrate`
* Run the server to test if the app is installed: in the terminal window type `python3 manage.py runserver`
* If the app has been installed correctly the window will display `The install worked successfully! Congratulations!`

#### 2. Create your Heroku app
* Navigate to the Heroku website
* In the Heroku browser window, create an account by entering your email address and a password
* Activate the account through the authentication email sent to your email account
* Click the new button and select create a new app from the dropdown menu
* Enter a name for the application which must be unique, in this case the app name is 'craftscircle'
* Select a region, in this case Europe
* Click create app

#### 3. Create the Database
* In the Heroku dashboard click on the Resources tab
* Scroll down to Add-Ons, search for and select 'Heroku Postgres'
* In the Settings tab, scroll down to 'Reveal Config Vars' and copy the text in the box beside DATABASE_URL.

#### 4. Set up Environment Variables
* In Gitpod create a new env.py file in the top level directory
* Add env.py to the .gitignore file
* In env.py import the os library
* In env.py add `os.environ["DATABASE_URL"]` = "Paste in the text link copied above from Heroku DATABASE_URL" from step 3
Insert yours here
* In env.py add `os.environ["SECRET_KEY"] = "Make up your own random secret key"`
* In Heroku Settings tab Config Vars enter the same secret key created in env.py by entering 'SECRET_KEY' in the box for 'KEY' and your randomly created secret key in the 'value' box.

#### 5. Connect the environment variables to Django

* In your Django 'settings.py' file type:

 ```
 from pathlib import Path
 import os
 import dj_database_url

 if os.path.isfile("env.py"):
  import env
 ```
* Remove the default insecure secret key in settings.py and replace with the link to the secret key variable i Heroku by typing: `SECRET_KEY = os.environ.get(SECRET_KEY)`
* Comment out the `DATABASES` section in settings.py and replace with:
```
DATABASES = {
  'default': 
  dj_database_url.parse(os.environ.get("DATABASE_URL"))
  }`
```
#### 6. Make migrations
* In the terminal type:
```
python3 manage.py makemigrations`
python3 manage.py migrate`
```

#### 7. Set up Cloudinary for static and media files storage
* Create a Cloudinary account and from the 'Dashboard' in Cloudinary copy your url into the env.py file by typing: `os.environ["CLOUDINARY_URL"] = "cloudinary://<insert-your-url>"`
* In Heroku  add cloudinary url to 'config vars'
* In Heroku config vars add DISABLE_COLLECTSTATIC with value of '1' (note: this must be removed for final deployment)
* Add Cloudinary libraries to installed apps section of `settings.py` in this order: 
 ```
 'cloudinary_storage'
 'django.contrib.staticfiles''
 'cloudinary'
 ```
* Connect Cloudinary to the Django app in `settings.py`:
```
STATIC_URL = '/static'
STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'STATIC')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE =
'cloudinary_storage.storage.MediaCloudinaryStorage'
* Link file to the templates directory in Heroku 
* Place under the BASE_DIR: TEMPLATES_DIR = os.path.join(BASE_DIR,
'templates')
```
* Change the templates directory to TEMPLATES_DIR. Place within the TEMPLATES array: `'DIRS': [TEMPLATES_DIR]`
* Add Heroku Hostname to ALLOWED_HOSTS: ```ALLOWED_HOSTS =
['craftscircle-9727f9958766.herokuapp.com', 'localhost']```

#### 8. Create `media`, `static` and `templates` folders in top level directory
#### 9. Create Procfile in top level directory: 
* In Procfile add: `web: gunicorn craftscircle.wsgi`
#### 10. In terminal add, commit, and push: 
```
git add <filename>
git commit -m “Deployment Commit”
git push
```
#### 11. Heroku Deployment: 
* Click Deploy tab in Heroku
* In the 'Deployment method' section select 'Github' and click the 'connect to Github' button to confirm.
* In the 'search' box enter the Github repository name for the project: craftscircle: https://github.com/AhmadAlmasriDev/crafts-circle

* Click search and then click connect to link the heroku app with the Github repository. The box will confirm that heroku is connected to the repository.

#### 12. Final Deployment
In the IDE: 
* When development is complete change the debug setting to: `DEBUG = False` in `settings.py` 
* In this project the [summernote](https://summernote.org/) editor was used so for this to work in Heroku add: `X_FRAME_OPTIONS = 'SAMEORIGIN'` to settings.py.
* In Heroku settings config vars change the DISABLE_COLLECTSTATIC value to 0
* Because DEBUG must be switched to True for development and False for production it is recommended that only manual deployment is used in Heroku. 
* To manually deploy click the button 'Deploy Branch'. The default 'main' option in the dropdown menu should be selected in both cases. When the app is deployed a message 'Your app was successfully deployed' will be shown. Click 'view' to see the deployed app in the browser. The live deployment of the project can be seen [here](https://github.com/AhmadAlmasriDev/crafts-circle)
