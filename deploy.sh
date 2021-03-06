#!/usr/bin/env bash

# 1. Önce root olmayan kullanıcı oluştur.
# 2. Daha sonra git clone
# 3. Aşağıdaki sed' li komutları kontrol et, düzenle
# 4. Scripti çalıştır.
# 5. Hello World! Kontrol et.
# 6. SSL sertifikası al.
# 7. Oyunu scp ile static dizinine yükle. "/static/game2101/index.hmtl" gibi bir yapı olacak.

# Run inside project directory
# Don't forget to change the username in myproject.service and myproject_nginx_available
# Don't forget to change the domain name in myproject_nginx_available

# sed 's/sammy/vagrant/' myproject_nginx_available
# sed 's/sammy/vagrant/' myproject.service
# sed 's/your_domain/basoglu.me/g' myproject_nginx_available

# certbot
# sudo certbot --nginx -d your_domain -d www.your_domain
# sudo ufw delete allow 'Nginx HTTP'

# sudo systemctl status myproject
# sudo systemctl status nginx
# sudo ufw status

sudo apt update
sudo apt upgrade -y
sudo apt install -y python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools python3-venv nginx certbot python3-certbot-nginx

python3 -m venv venv
source venv/bin/activate

pip install wheel
pip install uwsgi Flask

sudo cp myproject.service /etc/systemd/system/myproject.service

sudo systemctl start myproject
sudo systemctl enable myproject

sudo ufw allow 'Nginx Full'

sudo cp myproject_nginx_available /etc/nginx/sites-available/myproject
sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx