#!/usr/bin/env bash
set -o errexit  # Exit on error

# Debug directory structure
echo "Current Directory: $(pwd)"
echo "Directory Contents:"
ls -R

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
npm install
npm run tailwind
npm run minify

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate