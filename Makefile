all: coverage flake

flake:
	flake8 ogretests tests

coverage:
	nosetests --with-coverage
	coverage html
	coverage report

test:
	nosetests -s
