# Setup

This project runs on Python 3.5 so make sure you have it installed first

## Dependencies

Install dependencies into a virtualenv

        $ virtualenv -p `which python3` venv
        $ source venv/bin/activate
        $ pip install -r requirements.txt


## Run migrations

        $ python manage.py migrate

## Start server

        $ python manage.py runserver
