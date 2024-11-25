set -o errexit


# Install dependencies
pip install -r requirements.txt

# Run migrations and collect static files
python manage.py collectstatic --no-input
python manage.py migrate

# if [[ $CREATE_SUPERUSER ]]; then
#     python manage.py createsuperuser \
#         --no-input \
#         --username "$DJANGO_SUPERUSER_USERNAME" \
#         --email "$DJANGO_SUPERUSER_EMAIL" \
#         --first_name "$DJANGO_SUPERUSER_FIRST_NAME" \
#         --last_name "$DJANGO_SUPERUSER_LAST_NAME"
# fi

