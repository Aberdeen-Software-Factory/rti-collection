# Digital Collection of Artifacts

## Overview

This project is a web app for digital collection of artifacts mainly consisting of relightable images. This app relies on OpenLIME, and the relight command line tool https://github.com/cnr-isti-vclab/relight

See detailed setup and usage for each component:

- [Backend](/backend/README.md) – API for managing and converting artifact data (FastAPI)
- [Frontend](/frontend/README.md) – Interface for browsing and interacting with artifacts (Vue 3)

## Development

You can take advantage of hot reloads of fastapi and vue by running both services directly on your machine.

Run the backend from /backend
```
fastapi dev app/main.py
```

Run the frontend from /frontend
```
npm run dev
```

The [vite config](/frontend/vite.config.js) will redirect urls with api/ to localhost:8000 which is where the fastapi backend should be running.

## Deployment

Run the app:
```
docker compose up --build -d
```

Stop the app:
```
docker compose down
```

Execute both commands from the project root.

### Manual step-by-step

> [!NOTE]
> You don't have to do this when using docker compose.

This setup uses:

- A FastAPI backend container
- A Vue 3 frontend container served via Nginx
- A shared Docker network Nginx configured to proxy /api requests to the backend

1. Create a shared Docker network so containers can communicate:
    ```
    docker network create webapp-network
    ```

1. Build and run the backend container
    ```
    docker build -t fastapi-backend ./backend
    docker run -d \
      --name fastapi-backend \
      --network webapp-network \
      fastapi-backend
    ```

    This starts FastAPI on http://fastapi-backend:8000 inside the Docker network.

1. Build and run the frontend container (Vue + Nginx)
    ```
    docker build -t vue-frontend ./frontend

    docker run -d \
      --name vue-frontend \
      --network webapp-network \
      -p 80:80 \
      vue-frontend
    ```
    This serves the frontend at http://localhost.

    Ensure Nginx is configured to serve the SPA and proxy API calls:
    ```
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
    ```
    Make sure this config is copied into the container via the [Dockerfile](/frontend/Dockerfile).

Now access the app at: http://localhost

Frontend requests to /api/... are proxied to the FastAPI backend.
No CORS setup is needed.
No absolute API URLs are required in the frontend code.