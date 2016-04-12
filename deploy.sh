docker-compose --file docker-compose-dark.yml build
docker-compose --file docker-compose-dark.yml up -d
docker port pythonwebapp_lb 80