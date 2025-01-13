#!/usr/bin/env bash
set -o errexit

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Building TailwindCSS..."
cd node
npm install

if [ ! -f ./static/css/styles.css ]; then
    echo "Error: Input file ./static/css/styles.css does not exist. Please create the file."
    exit 1
fi

npm run tailwind
npm run minify
cd ..

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Applying database migrations..."
python manage.py migrate