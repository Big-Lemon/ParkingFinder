#!/bin/bash

export DEBIAN_FRONTEND=noninteractive

echo "Provision Start"
apt-get update

echo "Installing libmagickwand-dev"
apt-get install libmagickwand-dev -y > /dev/null

echo "Installing virtualenv"
apt-get install python-virtualenv -y > /dev/null

echo "Installing python-dev"
apt-get install python-dev -y > /dev/null

echo "Preparing MySQL"
apt-get install debconf-utils -y > /dev/null

debconf-set-selections <<< "mysql-server-5.5 mysql-server/root_password password development"
debconf-set-selections <<< "mysql-server-5.5 mysql-server/root_password_again password development"
echo "Installing MySQL"
apt-get install mysql-server-5.5 -y > /dev/null

wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
cp src/redis-cli /usr/local/bin/
cp src/redis-server /usr/local/bin/
cd ..
rm redis-stable.tar.gz

echo "Provision End"
