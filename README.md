# backend-service
Django API Service 

## Инициализация проекта 
1. docker compose -f docker/docker-compose-dev.yml up --build 


## Переменные окружения
- `POSTGRES_HOST`: адрес БД; default `localhost`
- `POSTGRES_DB`: имя БД; default `sqli_lab`
- `POSTGRES_PORT`: порт БД; default `5432`
- `POSTGRES_USER`: имя пользователя БД; default `sqli_user`
- `POSTGRES_PASS`: пароль пользователя БД; default `sqli_pass`
