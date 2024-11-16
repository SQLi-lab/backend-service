#!/usr/bin/env bash

# Скрипт сборки образов проекта
# Собирает образы backend, backend-migrator, deploy-service, deploy-service-worker, watcher
# Необходимо заранее положить архивы с проектами в папку ./deploy-prod

function check_root() {
  if [ "$EUID" -ne 0 ]; then
    echo "Ошибка: Скрипт должен быть запущен с sudo"
    exit 1
  fi
}

function check_files() {
  required_files=("backend-service.tar.gz" "deploy-service.tar.gz" "watcher-service.tar.gz")
  missing_files=()

  for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
      missing_files+=("$file")
    fi
  done

  if [ ${#missing_files[@]} -ne 0 ]; then
    echo "Ошибка: Отсутствуют следующие файлы:"
    for file in "${missing_files[@]}"; do
      echo "- $file"
    done
    exit 1
  else
    echo "Все необходимые файлы найдены."
  fi
}

function build_backend_service() {
    backend_tar_name="backend-service.tar.gz"
    backend_image_name="sqli-lab-backend:latest"

    tar -xvf $backend_tar_name
    cd backend-service
    docker build -t $backend_image_name -f docker/Dockerfile .
    cd ..
}

function build_backend_migrator() {
    backend_migrator_tar_name="backend-service.tar.gz"
    backend_migrator_image_name="sqli-lab-backend-migrator:latest"

    tar -xvf $backend_migrator_tar_name
    cd backend-service
    docker build -t $backend_migrator_image_name -f docker/Dockerfile .
    cd ..
}

function build_deploy_service() {
    deploy_service_tar_name="deploy-service.tar.gz"
    deploy_service_image_name="sqli-lab-deploy-service:latest"

    tar -xvf $deploy_service_tar_name
    cd deploy-service
    docker build -t $deploy_service_image_name -f docker/Dockerfile .
    cd ..
}

function build_deploy_service_worker() {
    deploy_service_worker_tar_name="deploy-service.tar.gz"
    deploy_service_worker_image_name="sqli-lab-deploy-service-worker:latest"

    tar -xvf $deploy_service_worker_tar_name
    cd deploy-service
    docker build -t $deploy_service_worker_image_name -f docker/Dockerfile .
    cd ..
}

function build_watcher() {
    watcher_tar_name="watcher-service.tar.gz"
    watcher_image_name="sqli-lab-watcher:latest"

    tar -xvf $watcher_tar_name
    cd watcher-service
    docker build -t $watcher_image_name -f docker/Dockerfile .
    cd ..
}

check_root
check_files

build_backend_service
build_backend_migrator
build_deploy_service
build_deploy_service_worker
build_watcher
