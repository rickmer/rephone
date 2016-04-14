test:
	py.test tests/
install:
	sudo bash apt.list
	virtualenv --python=python3 .
	bin/pip3 install -r requirements.txt
	sqlite3 app/db.sqlite < init_db.sql
	bin/python3 run.py --generate_captcha
