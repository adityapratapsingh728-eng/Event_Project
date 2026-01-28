#!/usr/bin/env bash
# Exit on error
set -o errexit

# 1. Install dependencies
pip install -r requirements.txt

# 2. Collect static files
python manage.py collectstatic --no-input

# 3. Run database migrations
python manage.py migrate

# 4. Create Superuser Safely (Modified to prevent duplicate error)
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); \
if not User.objects.filter(username='admin').exists(): \
    User.objects.create_superuser('admin', 'admin@example.com', '123'); \
    print('Superuser created successfully.') \
else: \
    print('Superuser already exists, skipping.')"
