#!/bin/bash
set -e
cd "$(dirname "$0")"

echo "Building..."
python3 build.py

echo "Deploying to GitHub Pages..."
cd output
git init
git add .
git commit -m "Deploy $(date '+%Y-%m-%d %H:%M')"
git remote add origin https://github.com/romelikethecity/keynotedata-website.git 2>/dev/null || \
  git remote set-url origin https://github.com/romelikethecity/keynotedata-website.git
git branch -M main
git push -u origin main --force

echo "Done! Live at https://keynotedata.com in ~60 seconds."
