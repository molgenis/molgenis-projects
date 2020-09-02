# Setup

cp docker/.env.example docker/.env
cd docker/nginx/ssl
./ca_cert.sh localhost
sudo ./ca_system.sh
cp
