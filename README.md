# ParkingFinder

## Setup Vagrant Environment

```
    # Install VirtualBox from: www.virtualbox.org/wiki/Downloads
    # Install Vagrant from: www.vagrantup.com/downloads.html

	git clone https://github.com/Big-Lemon/ParkingFinder.git
	cd ParkingFinder/
	vagrant box add ubuntu/trusty64

	# boot Vagrant environment
	vagrant up

	# ssh Virtual Machine
	vagrant ssh
```
Vagrant will synchronize ParkingFinder/ to the /vagrant directory
in vm, and it forwards the port 8888 of vm to host's 8888.

## Bootstrap Project
```
    vagrant ssh
    # in vm
    cd /vagrant
    . env/bin/activate
    make bootstrap
```

## Run Tests
```
    make test
```

## Serve
```
    make serve
```

## Install New Python Packages
```
	pip install [package]
	pip freeze > requirments.txt
```

## Connect to MySQL
```
    mysql -h localhost/ParkingFinder -P 3306 -u root -p development
```

## DB Migration
```
    # upgrade
    alembic revision -m "REVISION NAME"
    alembic upgrade head

    #downgrade
    alembic downgrade -1
```

