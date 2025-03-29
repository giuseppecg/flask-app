.PHONY: init-db
init-db: 
	@flask --app flaskr init-db

.PHONY: init-app
init-app: 
	@flask --app flaskr init-db
	@waitress-serve --port 8085 --call 'flaskr.main:get_app' 

.PHONY: init-app-dev
init-app-dev: 
	@flask --app flaskr/main.py run --debug

.PHONY: tests
tests:
	@python -m pytest tests/ -ra