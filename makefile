.PHONY: env-venv
env-venv:
	@python3 -m venv .flask-app
	@source .flask-app/bin/activate
	@pip install -r requirements.txt

.PHONY: env-pyenv
env-pyenv:
	@pyenv virtualenv 3.12.8 flask-app
	@pyenv activate flask-app
	@pip install -r requirements.txt

.PHONY: requirements
requirements:
	@pip install -r requirements.txt

.PHONY: init-db
init-db: 
	@flask --app flaskr init-db

.PHONY: init-app
init-app:
	@waitress-serve --port 8085 --call 'flaskr.main:get_app' 

.PHONY: init-app-dev
init-app-dev: 
	@flask --app flaskr/main.py run --debug

.PHONY: tests
tests:
	@python -m pytest tests/ -ra

.PHONY: black
black:
	@black -l 100 -q .