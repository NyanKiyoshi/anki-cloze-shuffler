.PHONY: build

build:
	mkdir -p dist
	zip --quiet -r -FS dist/anki-list-shuffler.ankiaddon ./__init__.py manifest.json
