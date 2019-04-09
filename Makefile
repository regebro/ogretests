all: coverage flake

flake:
	flake8 ogretests tests

coverage:
	coverage run setup.py test
	coverage html
	coverage report

test:
	python setup.py test
