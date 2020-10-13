BIN=venv/bin/

venv: venv/bin/activate

venv/bin/activate: requirements.txt
	test -d venv || virtualenv -p python3 venv
	. venv/bin/activate; pip install -r requirements.txt
	touch venv/bin/activate

run: venv
	$(BIN)python parser.py

test: venv
	$(BIN)python -m pylint -j 2 parser.py test_parser.py
	$(BIN)python -m pytest

clean:
	find . | grep -E "(venv|.pytest_cache|__pycache__|\.pyc|\.pyo$|)" | xargs rm -rf
        
