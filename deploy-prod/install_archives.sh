function download_archives() {
  git clone git@github.com:SQLi-lab/backend-service.git
  git clone git@github.com:SQLi-lab/deploy-service.git
  git clone git@github.com:SQLi-lab/watcher-service.git
  git clone git@github.com:SQLi-lab/dvwa-delivery.git
  git clone git@github.com:SQLi-lab/dvwa-clotheshop.git
  git clone git@github.com:SQLi-lab/dvwa-cigarshop.git
  git clone git@github.com:SQLi-lab/dvwa-carshop.git
  git clone git@github.com:SQLi-lab/dvwa-pharmacy.git

  tar -cf backend-service.tar.gz backend-service
  tar -cf deploy-service.tar.gz deploy-service
  tar -cf watcher-service.tar.gz watcher-service
  tar -cf dvwa-delivery.tar.gz dvwa-delivery
  tar -cf dvwa-clotheshop.tar.gz dvwa-clotheshop
  tar -cf dvwa-cigarshop.tar.gz dvwa-cigarshop
  tar -cf dvwa-carshop.tar.gz dvwa-carshop
  tar -cf dvwa-pharmacy.tar.gz dvwa-pharmacy

  rm -rf backend-service
  rm -rf deploy-service
  rm -rf watcher-service
  rm -rf dvwa-delivery
  rm -rf dvwa-clotheshop
  rm -rf dvwa-cigarshop
  rm -rf dvwa-carshop
  rm -rf dvwa-pharmacy
}

download_archives