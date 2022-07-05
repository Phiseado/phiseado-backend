# Phisheado. Tu phishing eliminado.

Phishing detection system using Artificial Intelligence.
Final thesis by María Isabel Ramos Blanco and Javier Vilariño Mayo.

## Deployment

There are different ways to initialize the application. Let's see them!

### To launch the project locally

1. Install Python version 3.7.
2. Install the requirements in the base directory of the project. Just open a console and type:

```sh
    python install -r requirements.txt
```

3. Install and create the PostgreSQL database with the following credentials:
```sh
            HOST : "localhost"
            NAME: "phiseado"
            USER: "postgres"
            PASSWORD: "postgres"
            PORT: "5432"
```

4. Migrate the database:
```sh
            python manage.py makemigrations
```
```sh
            python manage.py migrate
```
5. Launch the application:
```sh
            python manage.py runserver
```

### Run with Docker

This project can be built as a docker image. Just open a console and type:

```sh
docker-compose up
```

### To access with Heroku

```sh
https://phishing-alert-backend.herokuapp.com/swagger/
```
