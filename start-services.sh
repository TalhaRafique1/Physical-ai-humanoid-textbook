#!/bin/bash

# Start the Python backend in the background
cd /app/backend
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 &

# Start nginx to serve the frontend
cd /app/website
nginx -g "daemon off;"