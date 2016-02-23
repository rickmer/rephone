test:
	py.test tests/
install:
	bash apt.list
	virtualenv --python=python3 .
	bin/pip3 install -r requirements.txt
