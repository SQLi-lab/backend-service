# backend-service
Django API Service 

## Инициализация проекта
1. tar -xvf static.tar.gz
2. docker compose -f docker/docker-compose-dev.yml up --build 
3. войти по адресу сервера: `admin:admin`


## Переменные окружения
- `POSTGRES_HOST`: адрес БД; default `localhost`
- `POSTGRES_DB`: имя БД; default `sqli_lab`
- `POSTGRES_PORT`: порт БД; default `5432`
- `POSTGRES_USER`: имя пользователя БД; default `sqli_user`
- `POSTGRES_PASS`: пароль пользователя БД; default `sqli_pass`
