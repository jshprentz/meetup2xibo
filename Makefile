
test:
	. venv/bin/activate; \
	. ./test.config; \
	pytest --ignore=venv/

test-locals:
	. venv/bin/activate; \
	pytest --ignore=venv/ --showlocals

run:
	. venv/bin/activate; \
	. ./run.config; \
	python -m meetup2xibo -w > run.log

debug:
	. venv/bin/activate; \
	. ./run.config; \
	python -m meetup2xibo -v -d > run.log

help:
	. venv/bin/activate; \
	python -m meetup2xibo -h

gitlog:
	git log --oneline --graph --decorate --all

install:
	virtualenv -p python3.5 venv
	. venv/bin/activate; \
	pip3.5 install --upgrade pip setuptools wheel; \
	pip3.5 install -r requirements.txt; \
	pip3.5 install -r requirements-test.txt
