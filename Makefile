#
#
#

-include .env
AWS_DEFAULT_REGION?=ap-northeast-1


deploy: samconfig.toml
	sam build
	sam deploy --region $(AWS_DEFAULT_REGION)

samconfig.toml:
	sam build
	sam deploy --region $(AWS_DEFAULT_REGION) -g --no-execute-changeset

test:
	PYTHONPATH=${PYTHONPAT}:$$(echo ./src/*) python -m pytest tests

make-venv:
	python3 -m venv venv
	source venv/bin/activate; \
	pip install -r requirements.txt; \
	for i in src/*/requirements.txt; do pip install -r $${i}; done
