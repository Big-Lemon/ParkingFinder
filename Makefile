project := parkingfinder
test_folder := tests

export CLAY_CONFIG=config/development.json
export PYTHONPATH=.

.PHONY: bootstrap
bootstrap: clean 
	pip install -r requirements.txt

.PHONY: bootstrap_db
bootstrap_db: drop_db create_db upgrade_db 

.PHONY: drop_db
drop_db:
	python database.py drop
	echo "drop database"

.PHONY: create_db
create_db:
	python database.py create
	echo "create database"

.PHONY: serve
serve:
	python serve.py

.PHONY: test
test: clean bootstrap_db
	py.test --cov=ParkingFinder $(test_folder)

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
