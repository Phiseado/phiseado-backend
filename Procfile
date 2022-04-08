release: sh -c 'cd phishingidentify && python manage.py makemigrations && python manage.py migrate'
web: sh -c 'cd phishingidentify && gunicorn phishingidentify.wsgi --log-file -'