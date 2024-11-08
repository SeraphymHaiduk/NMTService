-include .env.local
export

SYSTEM_PYTHON = $(shell which python)
PYTHON = $(or $(wildcard venv/bin/python), $(SYSTEM_PYTHON))

# copy environment variables config template if .env.local does not exist yet
copy-env:
	cp -n .env.template .env.local

dep: copy-env
	sudo apt update
	sudo apt install -y mecab libmecab-dev mecab-ipadic-utf8 unidic-mecab
	sudo apt install -y python3.10 python3.10-venv #python3.10-dev
	python3.10 -m venv venv
	$(PYTHON) -m pip install -r ./app/requirements.txt

run:
	$(PYTHON) -m uvicorn --app-dir 'app' src.main:app --reload --port 5300 --host 0.0.0.0
	