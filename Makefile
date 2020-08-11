init:
	pip install .
	pip install -r requirements.txt
	pip install pytest
test:
	python -m pytest tests
ci:
	make test
	make lint
lint:
	python -m flake8 src/masonite/validation/ --ignore=E501,F401,E128,E402,E731,F821,E712,W503
format:
	black src/masonite/validation
coverage:
	python -m pytest --cov-report term --cov-report xml --cov=src/masonite/validation tests/
	python -m coveralls