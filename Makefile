install:
	cd web && bundle install
	pip install -r scripts/requirements.txt --upgrade

build:
	python scripts/build.py
	cd web && bundle exec jekyll build

serve: build
	cd web && bundle exec jekyll serve --skip-initial-build
