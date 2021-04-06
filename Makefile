install:
	cd web && bundle install
	pip install -r scripts/requirements.txt --upgrade

build:
	cd web && bundle exec jekyll build
	python scripts/sdg-build.py

serve: build
	cd web && bundle exec jekyll serve --skip-initial-build

clean:
	rm -fr _build
	rm -fr web/_site
