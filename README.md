# Desafio Backend tembici

## Django Project Example  
A simple Api to Simulate a Web Store Api  


## Environment

Python 3.8
Django 3.0.5  
[Postman](https://www.postman.com/)

## Installation

Update the SECRET_KEY from file .env (For test you could keep default value)  
To generate a new SECRET_KEY, run command:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy and Paste the SECRET_KEY generated in .env file.

### Using the Docker

Install Docker:  
[Docker](https://docs.docker.com/get-docker/)

Install Docker Compose:  
[DockerCompose](https://docs.docker.com/compose/install/)

```bash
docker-compose up -d
./launch.sh
```

### Run Local

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata viagens/fixtures/inital.json
python manage.py runserver 0.0.0.0:8000
```

## Usage

See Documentation:
[Documentation](https://documenter.getpostman.com/view/3762241/Szf9USGF?version=latest)
