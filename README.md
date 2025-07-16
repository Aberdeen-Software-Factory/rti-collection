# Digital Collection of Artifacts

See detailed setup and usage for each component:

- [Backend](/backend/README.md) – API for managing and converting artifact data
- [Frontend](/frontend/README.md) – Interface for browsing and interacting with artifacts

## Overview

This project is a web application that allows the user to view a collection of artifacts with religthable and still images and metadata information.

It consists of two components the backend and the frontend. The front end is developed in vuew and builds into a static website that can easily be hosted.

For the backend fastAPI is used and local file system serves as the "database" for uploaded artifact images and metadata information.

## Backend

The backend is a bit more complex because it uses hosting servers file system to store images and metadata in regular file system.

For safety only users who know the username password combo set by passing environment variables to backend

API_USERNAME
API_BACKEND

## Frontend

For the frontend to run the correct backend api base url has to be defined in .env.production (.env.development can be different for local testing)

## Development

run backend from /backend
```
fastapi dev app/main.py
```

run frontend from /frontend
```
npm run dev
```

the vite config will redirect urls with api/ to localhost:8000 which is where the fastapi backend should be running.

## Deployment

This setup uses:

A FastAPI backend container
A Vue 3 frontend container served via Nginx
A shared Docker network
Nginx configured to proxy /api requests to the backend
1. Create a Docker network
Create a shared network so containers can communicate:

docker network create webapp-network
2. Build and run the backend container
docker build -t fastapi-backend ./backend

docker run -d \
  --name fastapi-backend \
  --network webapp-network \
  fastapi-backend
This starts FastAPI on http://fastapi-backend:8000 inside the Docker network.
3. Build and run the frontend container (Vue + Nginx)
docker build -t vue-frontend ./frontend

docker run -d \
  --name vue-frontend \
  --network webapp-network \
  -p 80:80 \
  vue-frontend
This serves the frontend at http://localhost.
4. Nginx configuration inside the frontend container
Ensure Nginx is configured to serve the SPA and proxy API calls:

server {
  listen 80;

  location / {
    root /usr/share/nginx/html;
    index index.html;
    try_files $uri $uri/ /index.html;
  }

  location /api/ {
    proxy_pass http://fastapi-backend:8000/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_redirect off;
  }
}
Make sure this config is copied into the container via your Dockerfile.

✅ Result
Access the app at: http://localhost
Frontend requests to /api/... are proxied to the FastAPI backend
FastAPI responds correctly
No CORS setup is needed
No absolute API URLs are required in your frontend code