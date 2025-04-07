# Makefile -> Shell Script for

run: # Runs docker container to launch application
	docker-compose up
format-files: # Check for PEP8 inspired style checks for coding consistency
	docker-compose run --rm app /bin/sh -c 'black .'
	docker-compose run --rm app /bin/sh -c 'isort .'
test: # Runs Django app tests
	docker-compose run --rm app /bin/sh -c 'python manage.py test'
gha: # Runs GitHub Actions Running Locally!
	@echo "####### Running GitHub Actions Locally! #######"
	act push --secret-file .env