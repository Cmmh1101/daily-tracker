#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt
npm install

# Build TailwindCSS
npx tailwindcss -i ./static_src/src/styles.css -o ./static_src/css/dist/styles.css

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate
