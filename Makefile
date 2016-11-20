project := parkingfinder
test_folder := tests

export PYTHONPATH=.

.PHONY: bootstrap
bootstrap: clean
	pip install -r requirements.txt
	git clone https://github.com/andymccurdy/redis-py.git; cd redis-py; python setup.py install

.PHONY: bootstrap_db
bootstrap_db: flush_redis drop_db create_db upgrade_db

.PHONY: flush_redis
flush_redis:
	python database.py flush_redis

.PHONY: drop_db
drop_db:
	python database.py drop
	echo "drop database"

.PHONY: create_db
create_db:
	python database.py create
	echo "create database"

.PHONY: serve_redis
	redis-server

.PHONY: serve
serve:
	python serve.py

.PHONY: test
test: clean bootstrap_db
	py.test -v --cov-report term-missing --cov=ParkingFinder $(test_folder)

.PHONY: clean
clean:
	sh scripts/clean.sh

.PHONY: upgrade_db
upgrade_db:
	alembic upgrade head
	echo "upgrade database"

.PHONY: downgrade_db
downgrade_db:
	alembic downgrade -1

requirements.txt: requirements.in
	pip-compile --no-index requirements.in
