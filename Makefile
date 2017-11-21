
test:
	. venv/bin/activate; \
	pytest --ignore=venv/

gitlog:
	git log --oneline --graph --decorate --all

install:
	virtualenv -p python3.5 venv
	. venv/bin/activate; \
	pip3.5 install -r requirements.txt
