# ParkingFinder

## Setup Vagrant Environment

```
    # Install VirtualBox from: www.virtualbox.org/wiki/Downloads
    # Install Vagrant from: www.vagrantup.com/downloads.html

    git clone git@github.com:Big-Lemon/ParkingFinder.git
    cd ParkingFinder/
    vagrant box add ubuntu/trusty64

    # boot Vagrant environment
    vagrant up

    # ssh Virtual Machine
    vagrant ssh
```
Vagrant will synchronize ParkingFinder/ to the /vagrant directory
in vm, and it forwards the port 8888 of vm to host's 8888.

## Install
Install dependencies for project in virtual environment
```
    vagrant ssh     # ssh into virtual machine
    # in vm
    cd /vagrant
    virtualenv env
    export CLAY_CONFIG='config/development.json'
    . env/bin/activate  # activate virtualenv
    make bootstrap  	# install dependencies
    make bootstrap_db   # create database and tables
```

## Activate Virtual Environment
Activate the environment before doing anything else because all the 
dependencies are installed in environment
```
    . env/bin/activate
```

## Install New Python Packages
```
    pip install [package]
    pip freeze > requirments.txt
```

## Connect to MySQL
```
    mysql -h localhost/[TABLE_NAME] -P 3306 -u root -p
    # default password: development
```

## DB Migration
```
    # upgrade
    alembic revision -m "REVISION NAME"
    # modify revision file in alembic/version/
    make upgrade_db

    #downgrade
    make downgrade_db
```

# Run Tests
```
    CLAY_CONFIG='config/test.json' make test
```

## Serve
```
    make serve
```
