rm-dist:
	rm -rf dist

build: rm-dist
	python3 -m build

publish-test: build
	python3 -m twine upload  --repository testpypi --verbose dist/*

install-test:
	pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ --upgrade --no-cache-dir sdk_helo_email
