project := parkingfinder

export CLAY_CONFIG=config/development.json

.PHONY: bootstrap
bootstrap: clean upgrade
	pip install -r requirements.txt

.PHONY: bootstrap_db
    python

.PHONY: serve
serve:
	python serve.py

.PHONY: test
test: clean
	echo 'Tests are NotImplemented..'

.PHONY: clean
clean:
	sh scripts/clean.sh

.PHONY: upgrade
upgrade:
    alembic upgrade head

.PHONY: downgrade
downgrade:
    alembic downgrade -1


requirements.txt: requirements.in
	pip-compile --no-index requirements.in
