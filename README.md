# Survey system

Simple multi-language survey system written in Django, using Bootrstrap for front-end.  
Created as a college project.

## Table of contents

- [Features](#features)
- [Technologies used](#technologies-used)
  - [Additional modules](#additional-modules)
- [How to use](#how-to-use)
- [License](#license)

## Features

TODO

## Technologies used

- Python 3.7
- Django 3.2
- Bootstrap 4

### Additional modules

- Django reCAPTCHA
- Django Extensions (optional)
- django-crispy-forms
- django-modeltranslation
- Python Decouple

## How to use

1. Install Python 3.7 or above.
2. Install `pip`.
3. Create virtual environment using `venv` and activate it.
4. Clone this repo.
5. Install requirements: `pip install -r requirements.txt`.
6. Prepare the project:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
```

7. Compile the i18n messages: `django-admin compilemessages`.
8. Run the server: `python manage.py runserver`.
9. Open in a browser: `localhost:8000`.

## License

BSD-3-Clause License
