VENV = meowenv

install:
	python3 -m venv meowenv
	./meowenv/bin/pip install -r requirements.txt

clean:
	rm -rf meowenv