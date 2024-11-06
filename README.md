# backend-service
Django API Service 

## Инициализация проекта 
1. docker compose -f docker/docker-compose-dev.yml up --build 
2. python3 manage.py migrate
3. python3 manage.py createsuperuser --noinput --username admin --email ''
4. python3 manage.py runserver


## Переменные окружения
- POSTGRES_HOST: default localhost
- POSTGRES_DB: default sqli_lab
- POSTGRES_USER: default sqli_user
- POSTGRES_PASS: default sqli_pass
- POSTGRES_PORT: default 5432