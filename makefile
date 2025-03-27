.PHONY: tests
init-db: 
	flask --app flaskr init-db

.PHONY: tests
tests:
	 python -m pytest tests