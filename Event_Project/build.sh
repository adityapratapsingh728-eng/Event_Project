#!/usr/bin/env bash
# Exit on error
set -o errexit

# 1. Install dependencies
pip install -r requirements.txt

# 2. Collect static files (Essential for CSS/JS to work)
# This gathers all files into the STATIC_ROOT directory
python manage.py collectstatic --no-input

# 3. Run database migrations
# This ensures your Postgres database has the latest table structures
python manage.py migrate

# 4. (Optional) Create Superuser automatically
# Replace 'admin_user' and 'admin_password' with your preferred credentials
# Or better, use environment variables: os.environ.get('SUPERUSER_PASSWORD')
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin_user').exists() or User.objects.create_superuser('admin', 'admin@example.com', '123')"

# 5. (Optional) Load your initial data
# Only uncomment this if you have pushed your datadump.json to GitHub
# python manage.py loaddata datadump.json
