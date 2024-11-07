-include .env
export

SYSTEM_PYTHON = $(shell which python)
PYTHON = $(or $(wildcard venv/bin/python), $(SYSTEM_PYTHON))

dep:
	sudo apt update
	sudo apt install python3.10
	python3.10 -m venv venv
	$(PYTHON) -m pip install -r ./app/requirements.txt
	sudo apt install -y mecab libmecab-dev mecab-ipadic-utf8 unidic-mecab

run:
	$(PYTHON) -m uvicorn --app-dir 'app' src.main:app --reload --port 5300 --host 0.0.0.0
	