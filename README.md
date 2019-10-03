## Setting up
* Run make setup from project directory.
* Run poetry install (make sure your local python is > 3.7, use pyenv).
* To run the script run `poetry run thumbgen -d dir1/dir2 dir3`.
* To get script help run `poetry run thumbgen --help`.
* To install it as a package run `poetry build` the install the package generated in dist(.whl file) into your virtual environment. You can use it as a cli tool using `thumbgen -d dir1/dir2 dir3`.
