test:
	py.test tests/
install:
	virtualenv --python=python3 .
	bin/pip3 install -r requirements.txt
