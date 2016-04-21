IMAGE_NAME_APP := ggm8_app
IMAGE_NAME_LB := ggm8_lb
IMAGE_NAME_DB := ggm8_db
DOCKER_HUB_USERNAME := ggm8group
FILES :=        \
    .gitignore  \
    .travis.yml \
    makefile    \
    apiary.apib \
    IDB3.log    \
    models.html \
    app/models.py   \
    app/tests.py    \
    UML.pdf

check:
	@not_found=0;                                 \
    for i in $(FILES);                            \
    do                                            \
        if [ -e $$i ];                            \
        then                                      \
            echo "$$i found";                     \
        else                                      \
            echo "$$i NOT FOUND";                 \
            not_found=`expr "$$not_found" + "1"`; \
        fi                                        \
    done;                                         \
    if [ $$not_found -ne 0 ];                     \
    then                                          \
        echo "$$not_found failures";              \
        exit 1;                                   \
    fi;                                           \
    echo "success";

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

test:
	python3 app/tests.py

init-db:
	docker-compose --file docker-compose-prod.yml run -d --rm --no-deps app python idb.py create_db

docker-build:
	@if [ -z "$$CONTINUE" ]; then \
		read -r -p "Have you sourced the docker.env file for our Carina cluster? (y/n): " CONTINUE; \
	fi ; \
	[ $$CONTINUE = "y" ] || [ $$CONTINUE = "Y" ] || (echo "Exiting."; exit 1;)
	@echo "Building the images..."
	docker login

	docker build -t ${DOCKER_HUB_USERNAME}/${IMAGE_NAME_APP} app
	docker push ${DOCKER_HUB_USERNAME}/${IMAGE_NAME_APP}

	docker build -t ${DOCKER_HUB_USERNAME}/${IMAGE_NAME_LB} lb
	docker push ${DOCKER_HUB_USERNAME}/${IMAGE_NAME_LB}

	docker build -t ${DOCKER_HUB_USERNAME}/${IMAGE_NAME_DB} db
	docker push ${DOCKER_HUB_USERNAME}/${IMAGE_NAME_DB}

docker-push:
	docker-compose --file docker-compose-prod.yml up -d

models.html: app/models.py
	cp app/models.py ./ && cp app/loader.py ./
	pydoc3 -w models
	rm models.py && rm loader.py

log:
	# git log > IDB1.log
	# git log > IDB2.log
	git log > IDB3.log

run:
	python3 app/manage.py runserver

freeze:
	pip freeze > app/requirements.txt

requirements:
	pip install -r app/requirements.txt

loaddb:
	psql ggmate < db/ggmate_search.sql
