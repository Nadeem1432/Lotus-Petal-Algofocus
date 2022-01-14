#!/bin/sh

if [ "$DATABASE" = "postgres" ]; then
    echo "waiting for postgres..."

    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
        sleep 0.1
    done

    echo "postgresql started"
fi

echo "making migrations and migrating the database"
python3 manage.py makemigrations --no-input
python3 manage.py migrate --no-input
python3 manage.py collectstatic --no-input

exec "$@"