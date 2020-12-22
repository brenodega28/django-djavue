.ONESHELL:

build:
	python3 setup.py sdist

upload:
	python3 -m twine upload dist/*

test:
	python3 -m unittest djavue.tests

