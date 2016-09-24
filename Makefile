
.PHONY: install publish docs coverage lint graphs tests

install:
	python setup.py install

publish:
	python setup.py sdist upload

coverage:
	nosetests --logging-level=INFO --with-coverage --cover-package=steno3d --cover-html
	open cover/index.html

lint:
	pylint --output-format=html steno3d_surfer > pylint.html

graphs:
	pyreverse -my -A -o pdf -p steno3d-surfer steno3d_surfer/**.py

tests:
	nosetests --logging-level=INFO
