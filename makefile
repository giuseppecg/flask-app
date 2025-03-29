.PHONY: init-db
init-db: 
	flask --app flaskr init-db

.PHONY: init-app
init-app: 
	waitress-serve --port 8085 --call 'flaskr.main:get_app' 

.PHONY: init-app-dev
init-app-dev: 
	flask --app flaskr/main.py run --debug

.PHONY: tests
tests:
	coverage run -m pytest tests | coverage report -m