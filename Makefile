lint:
	status=0;\
mypy . || status=1;\
flake8 . || status=1;\
black . --check || status=1;\
isort . --check || status=1;\
vulture . || status=1;\
exit $$status

fmt:
	-command -v black && black .
	-command -v isort && isort .
	-command -v yarn && yarn prettier --write .
