# ParkingFinder

## Development 
```
    sudo apt-get install git
	git clone https://github.com/Big-Lemon/ParkingFinder.git
	cd ParkingFinder/
	sudo sh setup_env.sh
	virtualenv env
	source env/bin/activate
	export CLAY_CONFIG='config/development.json'
	make bootstrap
```

# Install MySQL
```
    sudo apt-get update
    sudo apt-get install mysql-server-5.6
    sudo mysql_secure_installation
```
After the MySQL root account is created, manually insert the
password and username in /config/development.json
(default password will be 'development')

## Update Python Packages
```
	pip install [package]
	pip freeze > requirments.txt
```

## Connect to MySQL
```
    mysql -h <endpoint>/<db_name> -P 3306 -u <mymasteruser> -p
```

## DB Migration
```
    # upgrade
    alembic revision -m "REVISION NAME"
    alembic upgrade head

    #downgrade
    alembic downgrade -1
```

## Run Tests
```
    make test
```

## Serve
```
    make serve
```
