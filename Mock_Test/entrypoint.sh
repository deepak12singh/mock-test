#!/bin/sh

echo "⏳ Waiting for DB..."
# Optional: wait for database to be ready (for PostgreSQL)
# Uncomment if using Postgres and set DB_HOST and DB_PORT in your env
# until nc -z $DB_HOST $DB_PORT; do
#   echo "Waiting for database..."
#   sleep 1
# done

echo "🚀 Running migrations..."
python manage.py migrate --noinput

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Starting server..."
exec "$@"

