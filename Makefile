.PHONY: build

build:
	mkdir -p dist
	zip --quiet -r -FS dist/anki-cloze-shuffler.ankiaddon ./__init__.py manifest.json
