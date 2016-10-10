# ParkingFinder

## Development 
```
	git clone https://github.com/Big-Lemon/ParkingFinder.git
	cd ParkingFinder/
	apt-get install virtualenv
	virtualenv env
	source env/bin/activate
	make bootstrap
```

## Update Python Packages
```
	pip install [package]
	pip freeze > requirments.txt
```

## Connect to MySQL
```
    mysql -h <endpoint> -P 3306 -u <mymasteruser> -p
```

## Migration
```
    alembic revision -m "REVISION NAME"
    alembic upgrade head
```
## Alembic downgrade
```
    alembic downgrade -1
```

## Run Service
```
    make serve
```
