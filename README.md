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
- `ADMIN_PASS`: пароль админа


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

## Развертывание Prod
1. Склонировать `backend-service`
2. Перейти в папку deploy-prod
3. Выполнить `./install_archives.sh`
4. Собрать архив deploy-prod.tar.gz `tar -cf deploy-prod.tar.gz deploy-prod`
5. Перенести на сервер `deploy-prod.tar.gz`, распаковать, `cd deploy-prod`
6. Распаковать архив deploy-service.tar.gz `tar -xvf deploy-service.tar.gz` 
7. Открыть `deploy-service/ansible/inventory.yml`, заменить креды от хостовой машины
8. Перейти в deploy-prod, создать архив `tar -cvf deploy-service.tar.gz deploy-service`
9. Запустить `install.sh`
10. Создать папку для лаб `cd ~ && mkdir sqli_labs`
11. Запустить `docker compose -f docker-compose-prod.yml up --build -d`

## Базовые креды 
- `127.0.0.1/` - панель управления admin@admin.com:admin
- `127.0.0.1/monitoring` - grafana admin:admin (заменяется после первого входа)

