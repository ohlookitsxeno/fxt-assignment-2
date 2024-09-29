VENV = meowenv

install:
	python3 -m venv meowenv
	./meowenv/bin/pip install -r requirements.txt

run:
	FLASK_APP=app.py FLASK_ENV=development ./meowenv/bin/flask run --port 3000

clean:
	rm -rf meowenv