#!/bin/bash
set -e

# Ensure data directory has correct ownership
sudo chown -R webapp:webapp /var/app/data
sudo chmod -R 775 /var/app/data

# Run migrations as webapp user
source /var/app/venv/*/bin/activate
cd /var/app/current
python manage.py migrate
python manage.py collectstatic --noinput

echo "Database setup and migrations completed successfully"
