#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Build TailwindCSS in the correct location
cd static_src/src
npm install
npm run build # This includes the Tailwind build step
cd ../../

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate