#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Build TailwindCSS in the correct location
cd node
npm install
npm run tailwind 
npm run minify
cd ..

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate