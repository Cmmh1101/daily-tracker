#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Build TailwindCSS in the correct location
echo "Building TailwindCSS..."
cd node
npm install
npm run tailwind # Ensure input/output paths are correct
npm run minify # Confirm what this does and its paths
cd ..

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate