# backend-service
Django сервис проекта лабораторных работ. Панель управления лабораторными работами. 
Через админ-панель позволяет мониторить активность студентов. 


## Переменные окружения
- `DEBUG`: debug режим: default `1`
- `DEPLOY_URL`: URL deploy-service; default `http://deploy-service:8001`
- `DEPLOY_SECRET`: секрет для deploy-service
- `WATCHER_URL`: URL watcher; default `http://watcher:8002`
- `POSTGRES_HOST`: адрес БД; default `localhost`
- `POSTGRES_DB`: имя БД; default `sqli_lab`
- `POSTGRES_PORT`: порт БД; default `5432`
- `POSTGRES_USER`: имя пользователя БД; default `sqli_user`
- `POSTGRES_PASS`: пароль пользователя БД; default `sqli_pass`


## Запуск проекта 
1. Распаковать исходники static: `tar -xvf static.tar.gz`
2. Запуск проекта в docker: `docker compose -f docker/docker-compose.yml up --build `
3. Запуск локально:

```shell
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    docker compose -f docker/docker-compose-dev.yml up --build -d
    python3 manage.py runserver
```

4. Войти по адресу сервера: `admin:admin`