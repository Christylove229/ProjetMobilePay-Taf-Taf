web: sh -c "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn mobilepay.wsgi:application --log-file -"
