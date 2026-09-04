.PHONY: install check test build clean

install:
	pip install -e ".[dev]"

check:
	ruff check .
	mypy sdk_helo_email

test:
	pytest -q

clean:
	rm -rf dist

build: clean
	python3 -m build

publish: build
	python3 -m twine upload dist/*
