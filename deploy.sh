#!/usr/bin/env bash

# Run inside project directory
# Don't forget to change the username in myproject.service and myproject_nginx_available
# Don't forget to change the domain name in myproject_nginx_available

# certbot
# sudo certbot --nginx -d your_domain -d www.your_domain
# sudo ufw delete allow 'Nginx HTTP'

# sudo systemctl status myproject
# sudo systemctl status nginx
# sudo ufw status

sudo apt update
sudo apt upgrade
sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
sudo apt install python3-venv nginx certbot python3-certbot-nginx

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
