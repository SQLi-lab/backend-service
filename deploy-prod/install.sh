#!/usr/bin/env bash

# Скрипт по установке и настройке системы на ОС Ubuntu / Ubuntu Server
# Перед началом нужно склонировать архив deploy-service в deploy-prod, поменять ansible/inventory.yml,
#   поставить свои креды логин, пароль, путь установки лабораторных

# Собирает образы backend, backend-migrator, deploy-service, deploy-service-worker, watcher
# Необходимо заранее положить архивы с проектами в папку ./deploy-prod

# После успешной установки запустить compose: docker compose -f docker-compo-prod.yml up --build -d

function check_root() {
  if [ "$EUID" -ne 0 ]; then
    echo "Ошибка: Скрипт должен быть запущен с sudo"
    exit 1
  fi
}

function check_files() {
  required_files=("deploy-service.tar.gz" "watcher-service.tar.gz" "dvwa-pharmacy.tar.gz")
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
    backend_service_tar_name="backend-service.tar.gz"
    backend_image_name="sqli-lab-backend:latest"

    tar -xvf $backend_service_tar_name
    cd backend-service
    tar -xvf static.tar.gz
    docker build -t $backend_image_name -f docker/Dockerfile . --no-cache
    cd ..
    rm -rf backend-service
}

function build_deploy_service() {
    deploy_service_tar_name="deploy-service.tar.gz"
    deploy_service_image_name="sqli-lab-deploy-service:latest"

    tar -xvf $deploy_service_tar_name
    cd deploy-service
    docker build -t $deploy_service_image_name -f docker/Dockerfile . --no-cache
    cd ..
    rm -rf deploy-service
}

function build_watcher() {
    watcher_tar_name="watcher-service.tar.gz"
    watcher_image_name="sqli-lab-watcher:latest"

    tar -xvf $watcher_tar_name
    cd watcher-service
    docker build -t $watcher_image_name -f docker/Dockerfile . --no-cache
    cd ..
    rm -rf watcher-service
}

function build_fronts_schemas_pharmacy() {
    pharmacy_tar_name="dvwa-pharmacy.tar.gz"
    pharmacy_front_image_name="dvwa-pharmacy-front:latest"
    pharmacy_back_image_name="dvwa-pharmacy-back:latest"

    tar -xvf $pharmacy_tar_name
    cd dvwa-pharmacy
    docker build -t $pharmacy_front_image_name -f pharmacy-app/Dockerfile.frontend pharmacy-app/ --no-cache
    docker build -t $pharmacy_back_image_name -f pharmacy-back/Dockerfile.backend pharmacy-back/ --no-cache
    cd ..
    rm -rf dvwa-pharmacy
}

function build_fronts_schemas_carshop() {
    carshop_tar_name="dvwa-carshop.tar.gz"
    carshop_front_image_name="dvwa-carshop-front:latest"
    carshop_back_image_name="dvwa-carshop-back:latest"

    tar -xvf $carshop_tar_name
    cd dvwa-carshop
    docker build -t $carshop_front_image_name -f carshop-app/Dockerfile.frontend carshop-app/ --no-cache
    docker build -t $carshop_back_image_name -f carshop-back/Dockerfile.backend carshop-back/ --no-cache
    cd ..
    rm -rf dvwa-carshop
}

function build_fronts_schemas_clotheshop() {
    clotheshop_tar_name="dvwa-clotheshop.tar.gz"
    clotheshop_front_image_name="dvwa-clotheshop-front:latest"
    clotheshop_back_image_name="dvwa-clotheshop-back:latest"

    tar -xvf $clotheshop_tar_name
    cd dvwa-clotheshop
    docker build -t $clotheshop_front_image_name -f clotheshop-app/Dockerfile.frontend clotheshop-app/ --no-cache
    docker build -t $clotheshop_back_image_name -f clotheshop-back/Dockerfile.backend clotheshop-back/ --no-cache
    cd ..
    rm -rf dvwa-clotheshop
}

function build_fronts_schemas_delivery() {
    delivery_tar_name="dvwa-delivery.tar.gz"
    delivery_front_image_name="dvwa-delivery-front:latest"
    delivery_back_image_name="dvwa-delivery-back:latest"

    tar -xvf $delivery_tar_name
    cd dvwa-delivery
    docker build -t $delivery_front_image_name -f delivery-app/Dockerfile.frontend delivery-app/ --no-cache
    docker build -t $delivery_back_image_name -f delivery-back/Dockerfile.backend delivery-back/ --no-cache
    cd ..
    rm -rf dvwa-delivery
}

function build_fronts_schemas_cigarshop() {
    cigarshop_tar_name="dvwa-cigarshop.tar.gz"
    cigarshop_front_image_name="dvwa-cigarshop-front:latest"
    cigarshop_back_image_name="dvwa-cigarshop-back:latest"

    tar -xvf $cigarshop_tar_name
    cd dvwa-cigarshop
    docker build -t $cigarshop_front_image_name -f cigarshop-app/Dockerfile.frontend cigarshop-app/ --no-cache
    docker build -t $cigarshop_back_image_name -f cigarshop-back/Dockerfile.backend cigarshop-back/ --no-cache
    cd ..
    rm -rf dvwa-cigarshop
}

function install_docker() {
    for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done

    sudo apt-get update
    sudo apt-get install -y ca-certificates curl
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc

    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin openssh-server sshpass
    sudo usermod -aG docker $USER
    sudo chmod 777 /var/run/docker.sock
    sudo chmod 777 /run/docker.sock
    docker network create sqli_lab
}


check_root
install_docker
check_files

build_backend_service
build_deploy_service
build_watcher
build_fronts_schemas_pharmacy
build_fronts_schemas_carshop
build_fronts_schemas_clotheshop
build_fronts_schemas_delivery
build_fronts_schemas_cigarshop
