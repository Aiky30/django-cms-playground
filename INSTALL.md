# Create a basic install of Django CMS

## Installation

Create a virtual environment
```
pyvenv ~/minimal-cms
```

Change into the project
```
cd ~/minimal-cms/bin
```

Clone this repository
```
git clone git@github.com:Aiky30/django-cms-minimal.git
```

Activate the source
```
source activate
```

Upgrade pip
```
pip install --upgrade pip
```

## For first time project setup

Install Django
```
pip install -r requirements.txt
```

Populate the database
```
python manage.py migrate
```

Create a super user
```
python ./manage.py createsuperuser
```

Check the cms install settings
```
python manage.py cms check
```

Runserver
```
python manage.py runserver
```