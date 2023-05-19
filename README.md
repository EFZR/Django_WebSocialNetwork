# Django_WebSocialNetwork

## How to install this app

1. Create a virtual Enviroment out of the __Django_WebSocialNetwork__ clone, with your terminal or whatever method is used to created:
  1. Open the terminal and type _python -m .venv venv_

2. Activate Virtual Enviorment
  1. source .venv/Scripts/Activate

3. Install the next Libraries to work
  1.1. python -m pip install django
  1.2. python -m pip install Faker
  1.3. python -m pip install crispy-bootstrap5
  1.4. python -m pip install django-bootstrap-v5
  1.5. python -m pip install -U channels["daphne"]
  1.6. python -m pip install -U 'Twisted[tls,http2]'

4. Open the __Django_WebSocialNetwork__
  1. cd __Django_WebSocialNetwork__

5. Finally activate server with
  1. python manage.py runserver