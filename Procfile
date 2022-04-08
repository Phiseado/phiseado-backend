release: sh -c 'python manage.py makemigrations && python manage.py migrate'
web: sh -c 'gunicorn phishingidentify.wsgi --log-file -'