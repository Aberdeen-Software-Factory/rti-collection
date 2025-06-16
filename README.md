# Digital Collection of Artifacts

This project is a web application that allows the user to view a collection of artifacts with religthable and still images and metadata information.

It consists of two components the backend and the frontend. The front end is developed in vuew and builds into a static website that can easily be hosted.

For the backend fastAPI is used and local file system serves as the "database" for uploaded artifact images and metadata information.

## Frontend

For the frontend to run the correct backend api base url has to be defined in .env.production (.env.development can be different for local testing)

## Backend

The backend is a bit more complex because it uses hosting servers file system to store images and metadata in regular file system.

For safety only users who know the username password combo set by passing environment variables to backend

API_USERNAME
API_BACKEND