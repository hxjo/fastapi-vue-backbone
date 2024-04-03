#!/bin/bash

# Start the Vue development server
cd /srv/vue
npm run dev -- --host 0.0.0.0 &

# Start the FastAPI server with Uvicorn
cd /srv/fastapi
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Wait for any process to exit
wait -n
