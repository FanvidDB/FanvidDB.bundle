lint:
	status=0;\
make py2lint || status=1;\
make py3lint || status=1;\
exit $$status

py2lint:
	status=0;\
flake8 . || status=1;\
isort -rc . --check || status=1;\
vulture . --min-confidence=100 --exclude=.git,.mypy_cache,.pytest_cache,.venv,__pycache__ || status=1;\
exit $$status

py3lint:
	status=0;\
python3 -m mypy --py2 . || status=1;\
python3 -m black . --check || status=1;\
exit $$status

fmt:
	python3 -m black .
	isort -rc
