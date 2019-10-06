.PHONY: setup
setup:
	sudo apt install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0


.PHONY: tox
tox:
	PYENV_VERSION=3.5.6 poetry run tox -e py35
	PYENV_VERSION=3.6.9 poetry run tox -e py36
	PYENV_VERSION=3.7.4 poetry run tox -e py37
