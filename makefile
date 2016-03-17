setup: requirements.txt
	pyvenv venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r requirements.txt

freeze:
	./venv/bin/pip freeze > requirements.txt
