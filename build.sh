set -o errexit

echo "Setting DJANGO_SETTINGS_MODULE..."
export DJANGO_SETTINGS_MODULE=hello_tractor.deployment_settings

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate