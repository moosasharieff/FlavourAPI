# Django REST API Template with Docker & Docker Compose

This repository contains a Django application set up with Docker and 
Docker Compose. You can use this as a template for your own Django 
REST applications. The following instructions guide you through setting up 
the project, managing the database, creating a superuser, and running tests.

## Prerequisites

Ensure you have the following installed on your local machine:

- Docker
- Docker Compose
- GitHub Account
- DockerHub Account

## Setup Instructions

1.  **Create a Folder and Initialize the Git Repository**

    Start by creating a new directory on your local machine for your project. Then, initialize the directory as a Git repository:

    ```bash
    mkdir <your_project_name> &&
    cd <your_project_name> &&
    git init
    ```

    This will create a new empty Git repository.

2.  **Add the DjangoRESTTemplate Repository as a Remote**

    You can use the DjangoRESTTemplate repository as a template for your project. Add it as a remote repository to fetch its contents:

    ```bash
    git remote add template https://github.com/moosasharieff/DjangoRESTTemplate.git
    ```

    This will allow you to fetch the latest changes from the DjangoRESTTemplate repository.

3.  **Merge the Main Branch Changes from the Template**

    To incorporate the latest changes from the main branch of the template repository, use the following commands:

    ```bash
    git fetch template &&
    git merge template/main
    ```

    This will merge the latest changes from the main branch of the DjangoRESTTemplate repository into your current project.

4.  **Build Docker Containers**

    To build the Docker images and services defined in the `docker-compose.yml` file, run the following command:

    ```bash
    docker-compose build
    ```

    This will build the necessary Docker images for your project.

5.  **Start the Containers**

    To start the Docker containers defined in `docker-compose.yml`, use the following command:

    ```bash
    docker-compose up
    ```

    This will start the web service (Django app) and any other services (like a database) defined in the `docker-compose.yml` file.

6.  **Create a Django Superuser**

    To create a superuser for accessing the Django admin panel, run the following command:

    ```bash
    docker-compose run --rm app /bin/sh -c "python manage.py createsuperuser"
    ```

    You will be prompted to enter a username, email, and password for the superuser.

7.  **Run Django Tests**

    To run the tests for your Django app inside the container, use:

    ```bash
    docker-compose run --rm app /bin/sh -c "python manage.py test"
    ```

    This will execute your Django test suite.

8.  **Stop the Containers**

    When you're done, you can stop and remove the containers by running:

    ```bash
    docker-compose down
    ```

9.  **Rebuild the Containers (if needed)**

    If you've made changes to the `Dockerfile` or `docker-compose.yml`, you may need to rebuild the containers. To do so, run:

    ```bash
    docker-compose build
    ```

    Then, start the containers again with:

    ```bash
    docker-compose up
    ```

10. **Configure GitHub Actions for DockerHub (Setup Secrets)**

    -   **Create a DockerHub Access Token:**
        -   Log in to your DockerHub account.
        -   Go to `Account Settings` -> `Personal access tokens`.
        -   Click `Generate new token`.
        -   Give your token a descriptive name (e.g., "GitHub Actions").
        -   Select the expirations date.
        -   Choose relevant access.
        -   Click `Generate`.
        -   Copy the generated `username` and `token`. **This is crucial, as you won't be able to see it again.**
    -   **Create DockerHub Secrets in GitHub:**
        -   Go to your GitHub repository's `Settings` -> `Secrets and variables` -> `Actions` -> `Secrets` -> `Repository secrets`.
        -   Add `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN`. Paste the token you copied from DockerHub in relevant textboxes.
        -   Click `Add secret`.
    -   *Note: This step prepares your GitHub repository with the necessary secrets for DockerHub authentication. You will need to create a GitHub actions workflow to utilize these secrets to push to Dockerhub.*

## Troubleshooting

If you run into issues, try the following:

-   Ensure Docker and Docker Compose are installed and running.
-   Check for any error messages in the logs when running `docker-compose up` or `docker-compose logs`.
-   Verify that your DockerHub credentials in GitHub Secrets are correct.
-   Ensure you copied the entire DockerHub token without any extra spaces.