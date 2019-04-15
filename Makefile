all: coverage flake

flake:
	flake8 ogretests tests

coverage:
	nosetests --with-coverage --cover-package=ogretests
	coverage html

test:
	nosetests -s
