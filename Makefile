build:
	python3 setup.py sdist

upload:
	python3 -m twine upload dist/*
