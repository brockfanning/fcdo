install:
	cd web && bundle install

build:
	cd web && bundle exec jekyll build

serve: build
	cd web && bundle exec jekyll serve --skip-initial-build
