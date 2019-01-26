run:
	python app.py

pylint:
	pylint app.py

db:
	alembic upgrade b07cb451ffb4_