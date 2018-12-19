.PHONY: venv

venv:
	virtualenv venv/
	venv/bin/python setup.py develop
	venv/bin/pip install -r dev-requirements.txt

clean:
	rm -rf *.pyc bugsnag_asgi.egg-info

test:
	tox --tox-pyenv-no-fallback

test_%:
	venv/bin/pytest -vsx tests/ -k $* --pdb

release:
	@-rm dist/*
	venv/bin/python setup.py sdist bdist_wheel
	@read -n 1 -r -p "Release to PyPI? " REPLY; \
	if [ "$$REPLY" == "y" ]; then\
		twine upload dist/*;\
	else\
		echo "Not uploading..";\
	fi
