run:
	python app.py

pylint:
	pylint app.py > pylint_score.txt

db:
	alembic upgrade b07cb451ffb4_

test:
	coverage run -m pytest
	coverage report app.py > coverage_score.txt