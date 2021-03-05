install:
	cd web && bundle install

build:
	python scripts/build.py
	cd web && bundle exec jekyll build

serve: build
	cd web && bundle exec jekyll serve --skip-initial-build
