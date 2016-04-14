test:
	py.test tests/
install:
	bash apt.list
	virtualenv --python=python3 .
	bin/pip3 install -r requirements.txt
	sqlite3 app/db.sqlite < init_db.sql
