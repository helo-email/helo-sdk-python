build:
	python3 -m build

publish-test:
	rm -rf dist && python3 -m twine upload  --repository testpypi --verbose dist/*