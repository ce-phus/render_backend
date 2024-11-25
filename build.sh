set -o errexit


# Install dependencies
pip install -r requirements.txt

# Run migrations and collect static files
python manage.py collectstatic --no-input
python manage.py migrate

if [[$CREATE_SUPERUSER]];
then 
    python manage.py createsuperuser --no-input
fi

