project := parkingfinder
export CLAY_CONFIG=config/development.json


.PHONY: bootstrap
bootstrap: clean
	pip install -r requirements.txt

.PHONY: serve
serve:
	python serve.py

.PHONY: test
test: clean
	echo 'Tests are NotImplemented..'

.PHONY: clean
clean:
	sh scripts/clean.sh


requirements.txt: requirements.in
	pip-compile --no-index requirements.in
