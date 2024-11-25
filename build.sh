set -o errexit


# Install dependencies
pip install -r requirements.txt

# Run migrations and collect static files
python manage.py collectstatic --no-input
python manage.py migrate



