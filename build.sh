set -o errexit

# Set the DJANGO_SETTINGS_MODULE explicitly for the Gunicorn process
echo "Setting DJANGO_SETTINGS_MODULE..."
export DJANGO_SETTINGS_MODULE=hello_tractor.deployment_settings

# Install dependencies
pip install -r requirements.txt

# Run migrations and collect static files
python manage.py collectstatic --no-input
python manage.py migrate

# Finally, start Gunicorn server with Uvicorn worker
echo "Starting Gunicorn server..."
exec gunicorn hello_tractor.asgi:application -k uvicorn.workers.UvicornWorker --log-level info

