if [ "$1" == "mysql" ]; then
	echo -e "\033[01;32mINFO: running 'python app.py create_db' in a new 'app' container so that it inits the running DB container\033[00m"
	docker-compose --file docker-compose-dark.yml run -d --rm --no-deps app python app.py create_db
elif [ "$1" == "sqlite" ]; then
	echo -e "\033[01;33mWARNING: I think you meant to have fixed your containers and deployed the DB to the correct one!\033[00m"
	docker_app_container_id="`docker ps -a | grep gunicorn | awk '{print $1 }' | head -n 1`"
	echo -e "\033[01;32mINFO: running 'python app.py create_db' in container ${docker_app_container_id}!\033[00m"
	docker exec -d ${docker_app_container_id} python app.py create_db
else
	echo -e "\033[01;31mERROR: I think you meant to give me a parameter!"
	echo -e "either \"mysql\" or \"sqlite\"!\033[00m"
fi